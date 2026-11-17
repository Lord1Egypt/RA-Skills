## Description:

Monitors Outlook and other webmail inboxes through a persistent Edge profile, processes new messages in a detached local background workflow, captures screenshots and attachments, and writes structured Excel rows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jizhidemu52](https://clawhub.ai/user/jizhidemu52)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to run and manage a Windows webmail monitor that turns inbox messages, screenshots, and attachments into a local Excel tracking workbook.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill would run a persistent local background process with ongoing access to a logged-in mailbox and local copies of email data.

Mitigation: Use only with an approved mailbox, confirm the monitor is expected to keep running, and review local storage and retention for screenshots, attachments, workbook rows, and logs before deployment.

Risk: The artifact describes PowerShell launch scripts, dependency installation, and automatic software installation, but the artifact contains only SKILL.md.

Mitigation: Require the publisher to include and review the referenced scripts, pin dependencies, and document exact install and storage behavior before execution.

Risk: The documented start command uses ExecutionPolicy Bypass.

Mitigation: Remove or explicitly justify the bypass and require user approval before running setup, installation, or persistent monitoring commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jizhidemu52/skills/webmail-email-monitor-skill)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Code, Configuration, Files]

**Output Format:** [Markdown with PowerShell command blocks and file-output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The described workflow writes an Excel workbook, message screenshots, downloaded attachments, and a runtime log to local storage.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
