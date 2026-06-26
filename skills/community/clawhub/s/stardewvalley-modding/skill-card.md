## Description: <br>
Helps an agent create Stardew Valley Content Patcher or SMAPI mods, including project structure, JSON content, NPC/event/dialogue additions, validation, and SMAPI build steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[YizeGe](https://clawhub.ai/user/YizeGe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and mod authors use this skill to scaffold and validate Stardew Valley Content Patcher and SMAPI mod projects. It is intended for creating mod files, JSON data, C# entry points, and shell commands for local tool checks or builds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unsafe mod or author names may cause generated files to be written outside the intended project folder. <br>
Mitigation: Use only trusted simple names without slashes, path segments, or markup, and review the target path before allowing files to be created or overwritten. <br>
Risk: Generated build and project files may include unescaped user input. <br>
Mitigation: Inspect generated JSON, C# project files, and source files before running dotnet build or installing the mod. <br>


## Reference(s): <br>
- [Stardew Modding Quick Reference](references/quickref.md) <br>
- [Stardew Valley Modding Wiki](https://stardewvalleywiki.com/Modding:Index) <br>
- [SMAPI](https://smapi.io/) <br>
- [Content Patcher](https://smapi.io/mods/1915) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with JSON, C#, Python, and shell command snippets; helper scripts may create files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate Stardew Valley mod project files for Content Patcher or SMAPI workflows.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
