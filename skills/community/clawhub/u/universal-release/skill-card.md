## Description: <br>
Universal release workflow. Auto-detects version files and changelogs. Supports Node.js, Python, Rust, Claude Plugin, and generic projects. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zoopools](https://clawhub.ai/user/Zoopools) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and release maintainers use this skill to prepare project releases by detecting version files and changelogs, analyzing changes since the last tag, proposing version bumps, generating multilingual changelog entries, and preparing release commits and tags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can convert vague push or release requests into repository edits, commits, tags, and remote pushes beyond the user's intent. <br>
Mitigation: Use dry-run first, review proposed file edits and commits before execution, and avoid using this skill as the default handler for vague push requests. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zoopools/universal-release) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and release summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose file edits, commits, tags, and remote pushes as part of a release workflow.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
