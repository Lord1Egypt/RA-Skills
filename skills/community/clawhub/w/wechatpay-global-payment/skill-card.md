## Description: <br>
微信支付境外（跨境）平台接入解决方案，覆盖产品选型、接入指南、质量评估、问题排查和多语言术语一致性支持。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, payment engineers, and implementation teams use this skill to plan and troubleshoot WeChat Pay Global integrations for overseas merchant and institution scenarios. It helps route questions to product selection, API parameters, signing, callbacks, order queries, network checks, quality review, and troubleshooting references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment integration guidance may become incorrect if direct-connection eligibility, auto-debit consent, notification requirements, or production API behavior changes. <br>
Mitigation: Verify operational decisions against current official WeChat Pay documentation or a Tencent/WeChat Pay contact before production use. <br>
Risk: The skill concerns flows that require sensitive merchant credentials, certificates, OAuth tokens, wallet access, and financial authority. <br>
Mitigation: Keep credentials out of prompts and logs, follow the official signing and callback verification guidance, and review credential handling before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/wechatpay-global-payment) <br>
- [WeChat Pay Global documentation (English)](https://pay.weixin.qq.com/doc/global/v3/en/) <br>
- [WeChat Pay Global documentation (Chinese)](https://pay.weixin.qq.com/doc/global/v3/zh/) <br>
- [WeChat Pay Global llms.txt](https://pay.weixin.qq.com/doc/global/v3/zh/llms.txt) <br>
- [Product introduction](references/1-机构/产品选型/产品介绍.md) <br>
- [Cross-border payment general knowledge](references/1-机构/产品选型/跨境支付通用知识.md) <br>
- [Development parameters](references/1-机构/接入指南/开发参数获取.md) <br>
- [Signing and signature verification rules](references/1-机构/接入指南/签名与验签规则.md) <br>
- [Callback handling](references/1-机构/接入指南/回调处理.md) <br>
- [Order query design guide](references/1-机构/接入指南/查单设计指引.md) <br>
- [Integration quality checklist](references/1-机构/接入指南/接入质量检查.md) <br>
- [Troubleshooting manual](references/1-机构/问题排查/排障手册.md) <br>
- [Glossary](references/glossary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Configuration instructions] <br>
**Output Format:** [Markdown guidance with official documentation references and configuration-oriented integration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Multilingual responses are expected to preserve payment API identifiers, domains, paths, and error codes.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
