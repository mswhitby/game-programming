# Game Programming & Design

Course content for [Ms. Whitby’s Playground](https://www.mswhitby.com/playground/). The shared website lives in `mswhitby/playground`; this repository owns curriculum and C# submissions.

## Course sequence
Six Unity Essentials companion units follow the official educator outline: Editor, 3D, Audio, Programming, 2D, and Publishing. A seventh unit begins Junior Programmer Player Control and Basic Gameplay.

Eleven original lessons and C# exercises, seven knowledge checkpoints (22 questions), and hands-on Unity tasks. The course overview includes the official tutorial outline. These classroom companions do not replace every Unity tutorial or award Unity badges.

## Student workflow
Read the lesson in the Playground, follow its Unity Learn link, complete the Unity task, and edit the C# practice starter. Console exercises use no UnityEngine APIs. Use Run code in the Playground, or run the full Program.cs in OnlineGDB’s C# compiler or a local .NET console project. `Main` prints an example; a descriptive method such as `CalculateScore` returns the answer. Keep those separate.

Use the in-app Run and Check controls for practice. The optional repository workflow also compiles submitted programs against published examples; it reads the function name from each exercise contract. Browser quizzes and self-reported Unity practice are formative practice, not official grades.

## Teacher/developer workflow
`course.json` is the content contract. `exercises/` contains matching editable starters. `scripts/grade.py` runs the same published cases with .NET 10 and writes a report. In PRs the checker is read from the base branch; student code runs on an ephemeral, read-only Actions job without secrets. It is not a hosted code-execution API.

The Playground imports `course.json` into its static build. Content changes appear on the next Playground build or publication. Refer to its README for publishing.

## Attribution and scope
This is original companion curriculum, not copied Unity quiz text. Links and alignment were checked on 2026-10-23. Unity UI and input APIs vary by version; follow the course project’s selected version. Essentials units follow the Unity 6 educator Common Cartridge dated 2025-10-23, retrieved from the official pathway page on 2026-10-23. The supplied UUID outline URL returned 404; the official educator download supplies the mission order. Junior Programmer begins Player Control/Basic Gameplay; neither companion claims completion of the official pathway.
