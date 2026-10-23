"""Compile submitted C# without trusting student project files or test definitions."""
import argparse, json, os, subprocess, tempfile
from pathlib import Path

def evaluate(source, cases):
    calls='\n'.join(f'Check({json.dumps(c["call"])}, () => Program.{c["call"]}, {c["expected"]});' for c in cases)
    runner='''using System;
using System.Collections.Generic;
using System.Text.Json;
public static class TestRunner {
static int failures;
static void Check<T>(string name, Func<T> fn, T expected) {
 try { T actual=fn(); bool ok;
 if(actual is float a && expected is float b) ok=Math.Abs(a-b)<=0.0001f;
 else ok=EqualityComparer<T>.Default.Equals(actual,expected);
 if(!ok) failures++;
 Console.WriteLine(JsonSerializer.Serialize(new {call=name, passed=ok, expected=expected, actual=actual}));
 } catch(Exception e) {failures++;Console.WriteLine(JsonSerializer.Serialize(new {call=name,passed=false,error=e.GetType().Name+": "+e.Message}));}
}
public static int Main(){
'''+calls+'\nreturn failures==0?0:1;}}'
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp);(p/'Student.cs').write_text(source);(p/'TestRunner.cs').write_text(runner)
        (p/'Check.csproj').write_text('<Project Sdk="Microsoft.NET.Sdk"><PropertyGroup><OutputType>Exe</OutputType><TargetFramework>net10.0</TargetFramework><StartupObject>TestRunner</StartupObject><ImplicitUsings>disable</ImplicitUsings><Nullable>disable</Nullable><EnableNETAnalyzers>false</EnableNETAnalyzers></PropertyGroup></Project>')
        env={**os.environ,'DOTNET_CLI_TELEMETRY_OPTOUT':'1','DOTNET_NOLOGO':'1'}
        try:
            build=subprocess.run(['dotnet','build','--nologo','-v','quiet'],cwd=p,capture_output=True,text=True,timeout=90,env=env)
            if build.returncode:return False,('Compilation error:\n'+build.stdout+build.stderr)[-6000:]
            result=subprocess.run(['dotnet',str(p/'bin/Debug/net10.0/Check.dll')],cwd=p,capture_output=True,text=True,timeout=8,env=env)
            return result.returncode==0,(result.stdout+result.stderr)[-6000:]
        except subprocess.TimeoutExpired:return False,'The program exceeded the time limit. Check for a non-ending loop.'

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--student-root',type=Path,default=Path('.'));parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    if args.self_test:
        assert evaluate('public class Program {public static int Solution(){return 3;}}',[{'call':'Solution()','expected':'3'}])[0]
        assert not evaluate('public class Program {public static int Solution(){return 4;}}',[{'call':'Solution()','expected':'3'}])[0]
        assert not evaluate('this is not C#',[{'call':'Solution()','expected':'3'}])[0]
        course=json.loads((Path(__file__).resolve().parents[1]/'course.json').read_text())
        for unit in course['units']:
            for lesson in unit['lessons']:
                ex=lesson['exercise'];ok,feedback=evaluate(ex['starter'],ex['examples'])
                assert not ok and 'NotImplementedException' in feedback, ex['id']+': '+feedback
        print('Checker verified: correct, incorrect, uncompilable, and all published starter/test contracts.');return
    course=json.loads((Path(__file__).resolve().parents[1]/'course.json').read_text());rows=[]
    for unit in course['units']:
        for lesson in unit['lessons']:
            ex=lesson['exercise'];path=args.student_root/ex['file']
            if not path.is_file():ok,detail=False,'Missing Program.cs'
            else:ok,detail=evaluate(path.read_text(),ex['examples'])
            rows.append({'id':ex['id'],'passed':ok,'feedback':detail});print(ex['id'], 'PASS' if ok else 'NEEDS REVISION');print(detail)
    Path('grading-report.json').write_text(json.dumps(rows,indent=2))
    summary='# C# practice checks\n\n| Exercise | Result |\n|---|---|\n'+''.join(f'| {r["id"]} | {"PASS" if r["passed"] else "Needs revision"} |\n' for r in rows)
    summary+=f'\n{sum(r["passed"] for r in rows)}/{len(rows)} exercises passed. This is practice feedback, not a course grade.\n'
    if os.environ.get('GITHUB_STEP_SUMMARY'):Path(os.environ['GITHUB_STEP_SUMMARY']).write_text(summary)
    raise SystemExit(0 if all(r['passed'] for r in rows) else 1)
if __name__=='__main__':main()
