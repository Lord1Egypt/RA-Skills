## Description:

Print files from inbound attachments or local paths on Windows only after a clear, explicit user print request, with optional printer selection, copy count, and process waiting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sqfcyily](https://clawhub.ai/user/sqfcyily)

### License/Terms of Use:

MIT-0

## Use Case:

People using Windows-based agents use this skill to print selected attachments or local files after explicitly confirming the files, printer, and copy count.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may send local files to a physical or network printer.

Mitigation: Use the skill only after the user gives an explicit print request and confirms the file list, printer, and copy count.

Risk: A named printer request may fall back to the default printer if PrintTo fails.

Mitigation: Confirm the selected printer before execution and monitor output when printing to a non-default printer.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/sqfcyily/skills/windows-print)

## Skill Output:

**Output Type(s):** [text, shell commands, guidance]

**Output Format:** [Markdown with inline PowerShell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce Windows print jobs for user-selected files after explicit confirmation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
