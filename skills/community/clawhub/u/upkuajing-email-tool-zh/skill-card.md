## Description:

支持发送个性化邮件，自动追踪邮件打开、点击及回复数据，助力企业高效开展跨境客户触达与海外营销推广，适用于外贸开发、客户跟进与跨境私域运营。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

External sales, marketing, and export teams use this skill to send personalized bulk email through Upkuajing and review task, delivery, open, click, read, and reply status for follow-up analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends email through the Upkuajing API and some actions can incur usage charges.

Mitigation: Confirm recipients, content, and expected cost before sending email or creating a recharge order; use the pricing reference or price information command for current pricing.

Risk: The skill uses UPKUAJING_API_KEY and may store it under ~/.upkuajing.

Mitigation: Prefer a restricted runtime or secret manager, avoid passing API keys as command-line arguments, and do not print or paste .env contents.

Risk: Error reports may include request context for troubleshooting.

Mitigation: Review report contents before approval and submit reports only after user confirmation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-email-tool-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [Email send API reference](references/email-send-api.md)
- [Email task list API reference](references/email-task-list-api.md)
- [Email task record list API reference](references/email-task-record-list-api.md)
- [Skill error report API reference](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python and UPKUAJING_API_KEY; email sending can incur usage charges.]

## Skill Version(s):

1.0.4 (source: SKILL.md frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
