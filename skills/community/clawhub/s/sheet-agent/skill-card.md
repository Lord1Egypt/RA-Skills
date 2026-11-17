## Description:

Spreadsheet operations agent for CSV and Excel files: inspect data, detect anomalies, answer business questions, generate reports, and preview edits safely.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, operators, and analysts use this skill to inspect CSV or Excel spreadsheets, answer natural-language business questions, detect anomalies, generate operational reports, and preview requested record edits before confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-selected spreadsheets that may contain sensitive business or personal data.

Mitigation: Install and run it only in environments where spreadsheet access is appropriate, and limit file inputs to data the user intends the agent to inspect.

Risk: Confirmed write operations can modify CSV or Excel files.

Mitigation: Review every change preview before confirming edits, and rely on the backup behavior when recovery is needed.

Risk: Backup files may retain spreadsheet data after an edit.

Mitigation: Manage the backup directory according to the same retention and access controls used for the source spreadsheets.

Risk: Spreadsheet parsing depends on local Python packages.

Mitigation: Prefer pinned dependency installation for pandas and openpyxl when maintaining or deploying this skill.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/harrylabsj/skills/sheet-agent)

## Skill Output:

**Output Type(s):** [Text, Markdown, Files, Guidance]

**Output Format:** [Markdown-style summaries, tables, anomaly lists, report sections, change previews, and confirmed CSV or Excel file updates.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only by default; write operations require confirmation and create backups before updating files.]

## Skill Version(s):

1.0.10 (source: server release evidence and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
