## Description:

A股/港股实时行情查询、基本面分析、深度报告生成与邮件发送一体化工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitjcl](https://clawhub.ai/user/hitjcl)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to query A-share and Hong Kong stock market data, retrieve fundamentals when JoinQuant credentials are configured, generate Markdown stock analysis reports, and optionally send those reports by email.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email and credential handling need careful review before use.

Mitigation: Run the skill in an isolated environment, review send_email.py before sending reports, provide credentials through environment variables or a secret manager, and avoid passing authorization codes or app passwords as command-line arguments.

Risk: Report contents and recipient details may be sent to external email providers.

Mitigation: Confirm recipients and report contents before sending, and treat QQ Mail or Gmail delivery as external disclosure.

Risk: jq_login.py stores the JoinQuant phone or account identifier locally.

Mitigation: Use environment variables where possible, limit filesystem access to the runtime environment, and clear local JoinQuant configuration when it is no longer needed.

## Reference(s):

- [Report Template](references/report_template.md)
- [Stock Codes Reference](references/stock_codes.md)
- [JoinQuant](https://www.joinquant.com)
- [ClawHub Skill Page](https://clawhub.ai/hitjcl/skills/stock-analyzer-v2)
- [Publisher Profile](https://clawhub.ai/user/hitjcl)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Plain text command output and Markdown reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write a report file and may send report content through configured QQ Mail or Gmail SMTP accounts.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
