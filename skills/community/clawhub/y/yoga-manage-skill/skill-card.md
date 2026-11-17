## Description:

瑜伽老师专用学员课时管理系统，使用 SQLite 本地存储学员信息、课程套餐和课时扣除日志，并可在扣课后发送邮件记录。

This skill is ready for commercial/non-commercial use.

## Publisher:

[yujintang](https://clawhub.ai/user/yujintang)

### License/Terms of Use:

MIT-0

## Use Case:

Yoga teachers use this skill to manage student contact records, online and offline course packages, lesson deductions, renewal reminders, and email reports from a local command-line or Python workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMTP email credentials are stored locally in plaintext configuration.

Mitigation: Use a dedicated app password or authorization code, keep the skill directory private, and exclude config.json from source control and shared backups.

Risk: Student contact details, notes, course data, and lesson logs are stored in a local SQLite database.

Mitigation: Treat yoga_students.db as sensitive student information and keep it out of source control, shared folders, and unmanaged backups.

Risk: The full-report email can send all student contact details and notes to the configured mailbox.

Mitigation: Confirm the configured recipient before sending full reports and avoid sending reports from shared or untrusted environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yujintang/skills/yoga-manage-skill)
- [Publisher profile](https://clawhub.ai/user/yujintang)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Plain text CLI output, Markdown usage guidance, Python API calls, and local SQLite/JSON configuration files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates a local SQLite database and email configuration file when run; can send lesson records and full reports through user-provided SMTP settings.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
