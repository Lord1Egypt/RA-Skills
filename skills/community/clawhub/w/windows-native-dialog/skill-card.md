## Description:

Handles native Windows file picker dialogs from WSL2 using exec and PowerShell.

This skill is ready for commercial/non-commercial use.

## Publisher:

[owlock](https://clawhub.ai/user/owlock)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users use this skill to handle Windows native file picker dialogs from WSL2 when browser automation cannot see or operate the dialog.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad persistent tool permissions can leave more access enabled than the file-dialog task requires.

Mitigation: Restrict permissions where possible and restore tool permissions after completing the task.

Risk: Host PowerShell execution can run local scripts or commands with effects outside browser automation.

Mitigation: Review the exact PowerShell and Python command before execution and use fixed file paths or trusted inputs.

Risk: The publish step may complete an external posting workflow without enough user control.

Mitigation: Require confirmation before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/owlock/skills/windows-native-dialog)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with inline shell and PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides an agent through browser automation, host PowerShell execution, and publish confirmation steps.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
