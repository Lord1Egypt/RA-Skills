## Description:

Helps developers integrate WeChat Pay with product selection guidance, Python and Node.js examples, business reference material, quality checks, and troubleshooting for common V3 API payment flows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jie868](https://clawhub.ai/user/jie868)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to choose WeChat Pay payment products, retrieve Python or Node.js integration examples, check callback and signature handling, and troubleshoot payment or refund flows before launch.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payment callback and refund examples can encourage unsafe financial-handling patterns if copied directly into production.

Mitigation: Treat examples as reference material, review them line by line, and validate all payment and refund flows with controlled credentials before deployment.

Risk: Callback handling may be unsafe if verification is incomplete or performed over the wrong request body.

Mitigation: Replace callback verification with real WeChat Pay platform certificate or public-key verification over the raw request body and fail closed on verification or processing errors.

Risk: Duplicate callbacks or mismatched order data can cause incorrect fulfillment or refund behavior.

Mitigation: Use durable database-backed idempotency and validate order, amount, and currency before changing business state.

Risk: Merchant private keys and APIv3 secrets can be exposed if handled like sample credentials.

Mitigation: Protect merchant keys and APIv3 secrets with production secret-management controls and remove unsafe dependency or setup commands before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jie868/skills/wechatpay-skill)
- [Metadata Homepage](https://github.com/wechatpay-apiv3/wechatpay-skills)
- [Python Interface Index](artifact/references/代码示例/接口索引/Python接口索引.md)
- [Node.js Interface Index](artifact/references/代码示例/接口索引/Node.js接口索引.md)
- [Merchant Signature and Verification Rules](artifact/references/商户模式/签名与验签/签名与验签规则.md)
- [Merchant Callback Handling](artifact/references/商户模式/回调处理/回调处理.md)
- [Merchant Integration Quality Checklist](artifact/references/商户模式/接入检查/接入质量检查清单.md)
- [Merchant Troubleshooting Guide](artifact/references/商户模式/排障手册/排障手册.md)
- [Payment Product Comparison](artifact/references/商户模式/支付产品对比/支付产品对比.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown responses with referenced code examples and occasional shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May require curl and user-provided WeChat Pay merchant context before producing specific integration guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
