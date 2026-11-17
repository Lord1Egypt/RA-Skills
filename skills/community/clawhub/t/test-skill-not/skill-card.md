## Description:

Provides WeChat Pay deduction integration guidance for recurring deductions and post-service payment workflows, covering signing, payment collection, pre-deduction notices, cancellations, queries, refunds, reconciliation, quality checks, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinwuzhe](https://clawhub.ai/user/yinwuzhe)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and payment engineers use this skill to choose WeChat Pay deduction integration patterns, retrieve official example payloads, check signing and callback rules, assess integration quality, and troubleshoot deduction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security evidence reports insecure HTTP callback examples in payment workflows.

Mitigation: Require HTTPS callback URLs with valid certificates before using the guidance in production payment systems.

Risk: Payment callback, signing, and replay handling errors can affect funds flow or reconciliation.

Mitigation: Verify callback signatures, enforce idempotency and replay controls, and complete a small-value end-to-end test before launch.

Risk: Troubleshooting payment failures can expose secrets, signatures, personal data, or unnecessary response fields.

Mitigation: Redact secrets, signatures, personal data, and nonessential response fields before sharing logs or examples.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinwuzhe/skills/test-skill-not)
- [Merchant product introduction](artifact/references/1-商户/产品选型/产品介绍.md)
- [Service-provider product introduction](artifact/references/2-服务商/产品选型/产品介绍.md)
- [Merchant API example index](artifact/references/1-商户/示例代码/接口索引.md)
- [Service-provider API example index](artifact/references/2-服务商/示例代码/接口索引.md)
- [Merchant signing and verification rules](artifact/references/1-商户/接入指南/签名与验签规则.md)
- [Service-provider signing and verification rules](artifact/references/2-服务商/接入指南/签名与验签规则.md)
- [Merchant callback handling](artifact/references/1-商户/接入指南/回调处理.md)
- [Service-provider callback handling](artifact/references/2-服务商/接入指南/回调处理.md)
- [Merchant troubleshooting guide](artifact/references/1-商户/问题排查/排障手册.md)
- [Service-provider troubleshooting guide](artifact/references/2-服务商/问题排查/排障手册.md)
- [WeChat Pay merchant deduction product documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986647.md)
- [WeChat Pay merchant deduction integration flow](https://pay.weixin.qq.com/doc/v2/merchant/4011986709.md)
- [WeChat Pay merchant recurring deduction documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986682.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown guidance with referenced XML, JSON, URL, and client SDK code examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires mode-specific context before payment, signing, callback, or troubleshooting guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter version is 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
