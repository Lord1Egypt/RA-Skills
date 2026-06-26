## Description: <br>
Create, update, hide, show, list, and delete Übersicht desktop widgets on macOS. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paranoidearth](https://clawhub.ai/user/paranoidearth) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and macOS users use this skill to install, customize, manage, and remove Übersicht desktop widgets with reusable templates and shell helpers. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can install and start Übersicht, copy files into ~/.claude/skills/widget, and write, move, or delete files in the Übersicht widgets folder. <br>
Mitigation: Run the dry-run check when diagnosing setup, review the target widget path before file operations, and prefer disabling a widget before permanent deletion when the user intent is uncertain. <br>
Risk: The Git activity widget can read local repository names, branches, and recent commit activity for display on the desktop. <br>
Mitigation: Enable or customize the Git widget only where displaying local repository metadata is acceptable. <br>
Risk: The weather widget contacts wttr.in for weather data. <br>
Mitigation: Review or disable the weather template when external weather lookups are not desired. <br>


## Reference(s): <br>
- [Widget reusable patterns](patterns.md) <br>
- [ClawHub Widget release](https://clawhub.ai/paranoidearth/widget) <br>
- [Homebrew](https://brew.sh) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Bash commands and JSX widget code] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create, copy, move, disable, or delete local Übersicht widget files when the user asks for those operations.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
