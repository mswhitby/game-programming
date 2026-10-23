# Game Programming & Design

Course content for [Ms. Whitby’s Playground](https://www.mswhitby.com/playground/). The shared website lives in `mswhitby/playground`; this repository owns curriculum and C# submissions.

## First two units
1. Unity Essentials companion: Editor, GameObjects, components, prefabs, audio, scripts, and basic numeric rules.
2. Junior Programmer companion: Player Control and introductory Basic Gameplay, movement, boundaries, action gates, and lives.

Eight original lessons, eight C# exercises, two eight-question knowledge checkpoints, and hands-on Unity tasks. Only the concepts explicitly taught in prior/current lessons are required by each exercise. Later Unity missions remain future units.

## Student workflow
Read the lesson in the Playground, follow its Unity Learn link, complete the Unity task, and edit the C# practice starter. Console exercises use no UnityEngine APIs. Run the full Program.cs in OnlineGDB’s C# compiler or a local .NET console project. `Main` prints an example; `Solution` returns the answer. Keep those separate.

Fork this repository, edit `exercises/<lesson-id>/Program.cs`, and open a pull request. The practice check compiles each submitted program and tests published examples. Browser quizzes and self-reported Unity practice are formative practice, not official grades.

## Teacher/developer workflow
`course.json` is the content contract. `exercises/` contains matching editable starters. `scripts/grade.py` runs the same published cases with .NET 10 and writes a report. In PRs the checker is read from the base branch; student code runs on an ephemeral, read-only Actions job without secrets. It is not a hosted code-execution API.

The Playground imports `course.json` into its static build. Content changes appear on the next Playground build or publication. Refer to its README for publishing.

## Attribution and scope
This is original companion curriculum, not copied Unity quiz text. Links and alignment were checked on 2026-10-23. Unity UI and input APIs vary by version; follow the course project’s selected version. Unit 1 samples Essentials skills and Unit 2 begins Player Control/Basic Gameplay. Neither claims to complete an entire official pathway.
