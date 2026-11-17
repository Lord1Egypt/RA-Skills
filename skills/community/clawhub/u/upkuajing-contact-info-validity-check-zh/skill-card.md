## Description:

核验邮箱、手机号及其余联系方式的真实有效性，在开展客户触达前筛选无效数据，提升联系信息准确度，降低消息无效发送概率，服务外贸获客、CRM 数据清洗和销售线索核验工作。

This skill is ready for commercial/non-commercial use.

## Publisher:

[upkuajing](https://clawhub.ai/user/upkuajing)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams, recruiters, traders, CRM operators, and procurement users use this skill to validate emails, phone numbers, WhatsApp status, and domains before outreach, candidate screening, supplier checks, or mailing-list cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill submits contact data and uses a paid API key with Upkuajing services.

Mitigation: Use it only when Upkuajing is an approved processor for the submitted data and keep the API key in a protected secret store or restricted `~/.upkuajing/.env` file.

Risk: Validation, account, recharge, and error-report actions can reveal account information or create billable activity.

Mitigation: Require explicit user confirmation before paid validation, account lookup, recharge-order creation, or platform error reporting.

Risk: Printing or inspecting local environment files could expose the API key.

Mitigation: Do not display `.env` contents in agent responses, and avoid logging request data that includes sensitive contact records or credentials.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/upkuajing/skills/upkuajing-contact-info-validity-check-zh)
- [Upkuajing homepage](https://www.upkuajing.com)
- [Upkuajing OpenAPI pricing](https://www.upkuajing.com/web/openapi/price.html)
- [电话有效性检测 API](references/phone-api.md)
- [邮件有效性检测 API](references/email-api.md)
- [域名有效性检测 API](references/domain-api.md)
- [Agent调用Skill异常上报 API 参考](references/skill-error-report-api.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, API validation results]

**Output Format:** [Markdown guidance and formatted JSON results from Python scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Validation outputs may include result lists, fee information, balances, and request IDs.]

## Skill Version(s):

1.0.4 (source: server evidence and SKILL.md metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
