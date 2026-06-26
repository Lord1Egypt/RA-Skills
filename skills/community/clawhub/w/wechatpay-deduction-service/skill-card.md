## Description: <br>
微信支付委托代扣接入解决方案，覆盖周期扣款、先享后付、纯签约、支付中签约、申请扣款、预扣费通知、解约、查询、退款、对账、质量评估和问题排查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration engineers use this skill to select and implement WeChat Pay delegated-deduction flows for merchant or service-provider mode, including signing, deduction, callbacks, refunds, reconciliation, quality review, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment-production guidance can affect user consent, deductions, refunds, and reconciliation. <br>
Mitigation: Use the skill only for intentional WeChat Pay delegated-deduction integration work; add clear consent UI, use test templates or minimal-value production tests, and review signing, callbacks, refunds, and reconciliation before launch. <br>
Risk: Payment identifiers, IP addresses, callback payloads, and signing material may be exposed through unnecessary logging or weak handling. <br>
Mitigation: Minimize logs and independently review callback verification, signing, secret handling, and reconciliation flows before deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tencent-adm/wechatpay-deduction-service) <br>
- [Merchant mode product introduction](artifact/references/1-商户/产品选型/产品介绍.md) <br>
- [Service-provider mode product introduction](artifact/references/2-服务商/产品选型/产品介绍.md) <br>
- [Merchant mode signing and verification rules](artifact/references/1-商户/接入指南/签名与验签规则.md) <br>
- [Service-provider mode signing and verification rules](artifact/references/2-服务商/接入指南/签名与验签规则.md) <br>
- [Merchant mode callback handling](artifact/references/1-商户/接入指南/回调处理.md) <br>
- [Service-provider mode callback handling](artifact/references/2-服务商/接入指南/回调处理.md) <br>
- [Merchant mode quality checklist](artifact/references/1-商户/接入指南/接入质量检查.md) <br>
- [Service-provider mode quality checklist](artifact/references/2-服务商/接入指南/接入质量检查.md) <br>
- [Merchant mode troubleshooting manual](artifact/references/1-商户/问题排查/排障手册.md) <br>
- [Service-provider mode troubleshooting manual](artifact/references/2-服务商/问题排查/排障手册.md) <br>
- [WeChat Pay merchant delegated-deduction product documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986647.md) <br>
- [WeChat Pay merchant delegated-deduction integration flow](https://pay.weixin.qq.com/doc/v2/merchant/4011986709.md) <br>
- [WeChat Pay merchant periodic deduction documentation](https://pay.weixin.qq.com/doc/v2/merchant/4011986682.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration] <br>
**Output Format:** [Markdown guidance with API request and response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Documentation-only skill; examples should be reviewed and tested before production payment use.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
