## Description:

Control Windows mouse clicks and keyboard inputs via PowerShell scripts, supporting text, shortcuts, and customizable click actions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[scottzhouzhou](https://clawhub.ai/user/scottzhouzhou)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation operators use this skill to generate guidance and PowerShell commands for controlling Windows desktop mouse and keyboard actions, including DingTalk message workflows. Users should review targets and scripts before execution because the actions affect the active desktop and can send real messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented PowerShell automation can control the active Windows desktop and send real DingTalk messages.

Mitigation: Confirm the target window, recipient, and message content before execution, and test in a controlled environment first.

Risk: The documented commands use PowerShell execution-policy bypass.

Mitigation: Verify the exact scripts and remove or justify execution-policy bypass before running commands.

Risk: Security evidence reports missing PowerShell automation scripts referenced by the documentation.

Mitigation: Do not run documented commands until the referenced scripts are present and reviewed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/scottzhouzhou/skills/win-control)
- [Publisher profile](https://clawhub.ai/user/scottzhouzhou)
- [Artifact README](artifact/README.md)
- [Artifact SKILL](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Windows desktop automation commands that affect the active window.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
