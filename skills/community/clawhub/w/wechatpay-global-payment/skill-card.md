## Description:

Guides developers and payment-integration teams through WeChat Pay Global product selection, API integration, quality checks, and troubleshooting for overseas cross-border payment scenarios.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and payment-integration teams use this skill to select WeChat Pay Global products, understand institution and sub-merchant integration requirements, locate official examples, run go-live checks, and troubleshoot cross-border payment issues.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment-operation evidence can expose sensitive data if raw logs, screenshots, credentials, Authorization headers, private keys, callback payloads, customer identifiers, transaction IDs, or production code are shared during go-live review.

Mitigation: Use only sanitized evidence, redact sensitive fields, and independently verify the support channel before sharing operational material.

Risk: The artifact contains conflicting direct-connection eligibility guidance for WeChat Pay Global onboarding.

Mitigation: Confirm direct-connection eligibility against current official WeChat Pay documentation before advising an integration mode.

## Reference(s):

- [微信支付境外接入指引](SKILL.md)
- [机构模式 产品选型与产品介绍（境外微信支付）](references/1-机构/产品选型/产品介绍.md)
- [微信支付境外（跨境）业务世界观](references/1-机构/产品选型/跨境支付通用知识.md)
- [机构模式 开发参数获取](references/1-机构/接入指南/开发参数获取.md)
- [机构模式 签名与验签规则（境外）](references/1-机构/接入指南/签名与验签规则.md)
- [机构模式 回调处理（境外）](references/1-机构/接入指南/回调处理.md)
- [查单逻辑设计指引（境外机构）](references/1-机构/接入指南/查单设计指引.md)
- [境外网络接入指引](references/1-机构/接入指南/网络问题指引.md)
- [API 版本对比与升级指引（境外机构）](references/1-机构/接入指南/API版本对比.md)
- [机构上线前接入质量检查（境外）](references/1-机构/接入指南/接入质量检查.md)
- [机构模式 接口索引](references/1-机构/示例代码/接口索引.md)
- [机构模式 排障手册（境外）](references/1-机构/问题排查/排障手册.md)
- [基础支付常见问题](references/1-机构/问题排查/基础支付常见问题.md)
- [扩展能力常见问题（境外机构）](references/1-机构/问题排查/扩展能力常见问题.md)
- [多语言术语表（Glossary）](references/glossary.md)
- [WeChat Pay Global Documentation (English)](https://pay.weixin.qq.com/doc/global/v3/en/)
- [WeChat Pay Global Documentation (Chinese)](https://pay.weixin.qq.com/doc/global/v3/zh/)
- [Official Partner Search](https://pay.weixin.qq.com/index.php/public/wechatpay_en/partner_search#/)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with checklists, tables, official-document pointers, and inline commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Chinese, English, Japanese, Korean, French, Spanish, Portuguese, Russian, and Arabic terminology.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
