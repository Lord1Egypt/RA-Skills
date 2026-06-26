## Description: <br>
Install and initialise Tribunal - the Claude Code quality enforcement plugin for setting up TDD enforcement, secret scanning, quality gates, and project checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[koshaji](https://clawhub.ai/user/koshaji) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and AI-assisted coding teams use this skill to install and initialise Tribunal in a project so Claude Code workflows can add quality enforcement, secret scanning, TDD checks, and related project configuration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tribunal initialization changes project Claude Code configuration and enables ongoing quality hooks. <br>
Mitigation: Use the skill only for projects where those configuration changes are intended, then inspect `.claude/tribunal.json` and `.claude/settings.json` after initialization. <br>
Risk: The installation commands retrieve a third-party Tribunal package. <br>
Mitigation: Pin or review the package source before installation in sensitive or production projects. <br>


## Reference(s): <br>
- [Tribunal Homepage](https://tribunal.dev) <br>
- [Tribunal Repository](https://github.com/thebotclub/tribunal) <br>
- [ClawHub Skill Page](https://clawhub.ai/koshaji/tribunal-install) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
