## Description: <br>
Reverse-imports an existing novel, either complete or in progress, into a standard writing-project structure for later long-form or short-form story workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers and writing-workflow agents use this skill to convert existing novel text into a resumable local project with source text, analysis assets, outlines, settings, character material, and tracking files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can create many files, set the active book marker, and overwrite generated reference files for the imported project. <br>
Mitigation: Review the target directory and import destination before invoking the skill, and keep backups of important project files. <br>
Risk: The workflow copies user-provided novel text into local project folders. <br>
Mitigation: Import only content the user is authorized to process and store it in an approved workspace. <br>


## Reference(s): <br>
- [Story Import skill page](https://clawhub.ai/worldwonderer/skills/story-import) <br>
- [OpenClaw source metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [length-routing.md](references/length-routing.md) <br>
- [structure-mapping-long.md](references/structure-mapping-long.md) <br>
- [structure-mapping-short.md](references/structure-mapping-short.md) <br>
- [character-state-reverse.md](references/character-state-reverse.md) <br>
- [format-and-structure.md](references/format-and-structure.md) <br>
- [state-tracking.md](references/state-tracking.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown project files and concise workflow guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local writing-project directories, copied source text, analysis assets, outlines, settings, and tracking files.] <br>

## Skill Version(s): <br>
1.0.9 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
