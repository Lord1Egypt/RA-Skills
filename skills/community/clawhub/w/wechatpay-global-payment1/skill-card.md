## Description:

微信跨境支付接入Skill helps agents guide WeChat Pay Global product selection, integration, quality checks, troubleshooting, and multilingual terminology for overseas payment scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, payment engineers, and support teams use this skill to plan and review overseas WeChat Pay integrations, including product selection, API version choices, callback handling, signing, quality checks, and troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment work may expose raw logs, screenshots, Authorization headers, APIv3 keys, private keys, callback payloads, OpenIDs, identity data, or customer and payment records.

Mitigation: Redact sensitive values, use test data where possible, and avoid sending sensitive payment material through email or chat.

Risk: Incorrect direct-connection eligibility or network choices could create unsafe or nonfunctional payment deployments.

Mitigation: Verify direct-connection eligibility, callback firewall rules, and network configuration against current official WeChat Pay documentation before implementation.

Risk: Weak retry, idempotency, or callback handling can lead to incorrect payment state decisions.

Mitigation: Review order retry behavior, idempotency design, asynchronous callback processing, and query-order fallback before production use.

Risk: Auto-debit flows can continue incorrectly if notices or cancellation events are mishandled.

Mitigation: Validate auto-debit notice and cancellation handling against official documentation and stop subsequent debits when cancellation is confirmed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/wechatpay-global-payment1)
- [WeChat Pay Global documentation](https://pay.weixin.qq.com/doc/global/v3/en/)
- [WeChat Pay Global documentation (Chinese)](https://pay.weixin.qq.com/doc/global/v3/zh/)
- [机构模式 产品选型与产品介绍（境外微信支付）](references/1-机构/产品选型/产品介绍.md)
- [微信支付境外（跨境）业务世界观](references/1-机构/产品选型/跨境支付通用知识.md)
- [机构模式 签名与验签规则（境外）](references/1-机构/接入指南/签名与验签规则.md)
- [境外网络接入指引](references/1-机构/接入指南/网络问题指引.md)
- [接入质量检查](references/1-机构/接入指南/接入质量检查.md)
- [排障手册](references/1-机构/问题排查/排障手册.md)
- [多语言术语表（Glossary）](references/glossary.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown responses with links, checklists, tables, and official-example navigation.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Multilingual replies in Chinese, English, Japanese, Korean, French, Spanish, Portuguese, Russian, and Arabic.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.6)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
