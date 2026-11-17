## Description:

自动整理周报工具，支持从 GitHub、飞书文档、日历和手动输入汇总工作内容，生成 Markdown 周报并可导出或发送。

This skill is ready for commercial/non-commercial use.

## Publisher:

[carson1012](https://clawhub.ai/user/carson1012)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, individual contributors, and team leads use this skill to consolidate weekly work activity from repositories, Feishu documents, calendars, and manual notes into a structured status report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles GitHub, Feishu, Google Calendar, and SMTP credentials.

Mitigation: Use narrowly scoped tokens and avoid passing secrets as command-line arguments or storing them in shell history.

Risk: Generated reports can be sent outside the local environment through email or Feishu documents.

Mitigation: Verify recipients, document IDs, and workspace targets before sending or writing reports.

Risk: Automated cron execution can send or write reports without a final human check.

Mitigation: Do not enable scheduled automation until confirmation steps are added for external delivery actions.

Risk: Untrusted report content may be converted to HTML or email without sanitization, and local file paths are accepted for export and history actions.

Mitigation: Sanitize report content before HTML/email export and validate output paths before writing files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/carson1012/skills/weekly-report-ai)

## Skill Output:

**Output Type(s):** [Markdown, Files, Shell commands, Configuration guidance]

**Output Format:** [Markdown report text, optional HTML/PDF files, and JSON status from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include GitHub, Feishu, calendar, and manual-input summaries; optional delivery paths include SMTP email and Feishu documents.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
