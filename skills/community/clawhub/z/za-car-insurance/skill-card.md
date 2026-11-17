## Description:

智能车险报价引擎，引导用户通过手机号授权、验证码登录、车辆报价、方案确认、核保支付和出单查询完成车险自助投保流程。

This skill is ready for commercial/non-commercial use.

## Publisher:

[henry4c](https://clawhub.ai/user/henry4c)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this agent to complete a ZhongAn car-insurance quote and purchase workflow, including authorization, quote retrieval, coverage adjustment, payment-link generation, and policy issuance lookup. The skill is intended for Chinese car-insurance self-service scenarios that require live API responses and user confirmation at each step.

### Deployment Geography for Use:

China

## Known Risks and Mitigations:

Risk: The skill handles phone numbers, identity details, vehicle data, and API credentials during live insurance workflows.

Mitigation: Review and harden sensitive-data handling before using the skill with real customer data; avoid printing secrets or full request bodies in logs or chat output.

Risk: Payment QR-code construction may expose the API key if credentials are placed in URLs.

Mitigation: Remove API keys from query strings and pass credentials only through protected headers or trusted session mechanisms.

Risk: Local authorization storage can retain user phone numbers on disk.

Mitigation: Secure, minimize, or eliminate local phone-number storage and provide a clear deletion path for user authorization records.

Risk: Temporary request-body files can contain personal information used for quote, underwriting, and policy issuance calls.

Mitigation: Use safe temporary-file creation, restrictive permissions, and reliable cleanup for any transient files containing customer data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/henry4c/skills/za-car-insurance)
- [Publisher profile](https://clawhub.ai/user/henry4c)
- [ZhongAn car insurance gateway](https://car.zhongan.com)
- [Authentication workflow](artifact/auth.md)
- [Quote workflow](artifact/quote.md)
- [Underwriting, payment, and policy issuance workflow](artifact/proposal.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, API Calls, Guidance]

**Output Format:** [Chinese conversational text with Markdown templates, Bash command patterns, and live API response fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs depend on live ZhongAn API responses, user-provided vehicle and identity data, and payment or policy-status results.]

## Skill Version(s):

1.0.4 (source: server release metadata; artifact frontmatter reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
