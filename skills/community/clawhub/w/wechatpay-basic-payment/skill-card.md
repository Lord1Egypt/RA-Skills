## Description: <br>
微信支付基础支付解决方案，涵盖支付、退款账单、分账、商户进件、开户意愿确认，提供选型、代码示例、业务速查、质量评估和排障能力。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpeng319](https://clawhub.ai/user/zhangpeng319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers integrating WeChat Pay use this skill to choose payment modes, retrieve Java or Go examples, troubleshoot order, refund, callback, and settlement issues, and assess integration quality for merchant or service-provider modes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles payment integration workflows and may involve sensitive merchant credentials. <br>
Mitigation: Do not paste private keys or APIv3 keys into chat; generate signatures locally and use credentials only for merchant accounts you control. <br>
Risk: Example code and troubleshooting scripts may expose transaction or account details in logs or terminal output. <br>
Mitigation: Redact terminal output before sharing logs and remove raw response logging before production use. <br>
Risk: Payment, refund, settlement, and onboarding examples can affect real financial workflows if copied without review. <br>
Mitigation: Treat examples as reference material, validate them against official WeChat Pay documentation, and complete testing before production use. <br>
Risk: Some receiver-name or business onboarding fields can contain sensitive information. <br>
Mitigation: Encrypt sensitive receiver-name fields and follow WeChat Pay guidance for protected business data. <br>


## Reference(s): <br>
- [支付产品对比](references/3-商户与服务商通用/产品选型/支付产品对比.md) <br>
- [接入模式说明](references/3-商户与服务商通用/接入指南/接入模式说明.md) <br>
- [签名与验签规则](references/3-商户与服务商通用/接入指南/签名与验签规则.md) <br>
- [接入质量检查清单](references/3-商户与服务商通用/接入指南/接入质量检查清单.md) <br>
- [回调通知处理](references/3-商户与服务商通用/接入指南/回调通知处理.md) <br>
- [排障手册](references/3-商户与服务商通用/问题排查/排障手册.md) <br>
- [商户模式接口索引](references/1-商户/示例代码/接口索引.md) <br>
- [服务商模式接口索引](references/2-服务商/示例代码/接口索引.md) <br>
- [WeChat Pay API v3 merchant documentation](https://pay.weixin.qq.com/doc/v3/merchant/4015119334) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Guidance] <br>
**Output Format:** [Markdown responses with retrieved Java or Go code examples and optional local script commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides reference material and troubleshooting steps; script use requires user-controlled merchant credentials and explicit confirmation.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
