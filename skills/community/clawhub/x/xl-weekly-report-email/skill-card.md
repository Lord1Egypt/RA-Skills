## Description:

通用周报收集和邮件推送技能，支持交互式填写周报内容，自动计算周数和日期范围，生成美观的HTML格式邮件。

This skill is ready for commercial/non-commercial use.

## Publisher:

[zq62191161-ai](https://clawhub.ai/user/zq62191161-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Employees and managers use this skill to collect weekly work updates through a guided conversation, generate a styled HTML weekly report, and send it by email through a configured SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SMTP credentials and report contents.

Mitigation: Use an app-specific SMTP password and avoid entering secrets or sensitive internal details in weekly reports.

Risk: Weekly reports are sent to configured and optional recipient lists.

Mitigation: Review the generated preview and verify all recipients and CC addresses before confirming send.

Risk: User report text is rendered into an HTML email body.

Mitigation: Prefer a version that escapes HTML before rendering report content.

Risk: Temporary report cleanup accepts a provided file path.

Mitigation: Prefer a version that restricts deletion to the skill's own memory directory.

Risk: The bundled email dependency may need maintenance.

Mitigation: Review and update nodemailer before production use.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/zq62191161-ai/skills/xl-weekly-report-email)
- [CHANGELOG.md](CHANGELOG.md)
- [Nodemailer Package](https://registry.npmjs.org/nodemailer/-/nodemailer-6.10.1.tgz)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Conversational guidance, Markdown report content, HTML email body, and SMTP send instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user-provided SMTP configuration, report profile fields, recipient addresses, and explicit confirmation before sending.]

## Skill Version(s):

1.0.0 (source: server release; artifact version fields differ)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
