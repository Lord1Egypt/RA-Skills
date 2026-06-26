## Description: <br>
微信支付分接入解决方案，覆盖创单、确认、完结、扣款、退款、业务规则速查、质量评估和问题排查。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpeng319](https://clawhub.ai/user/zhangpeng319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and payment integration engineers use this skill to navigate WeChat Pay Score merchant or service-provider integration, retrieve maintained Java and Go examples, check signing and callback handling, assess integration quality, and troubleshoot common issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill supports payment integration workflows that require merchant credentials, private keys, API keys, callbacks, refunds, and order state changes. <br>
Mitigation: Use it as reference material, keep secrets out of source control, redact sensitive payment data from logs, and test signing, callback verification, idempotency, and refund flows before production use. <br>
Risk: Sample code and translated cross-language examples may need production hardening before direct use. <br>
Mitigation: Review and adapt examples against official Java or Go references, validate in a test environment, and avoid copying placeholder credentials or broad network bypass rules into production. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zhangpeng319/wechatpay-payscore) <br>
- [Merchant product introduction](references/1-商户/产品选型/产品介绍.md) <br>
- [Service-provider product introduction](references/2-服务商/产品选型/产品介绍.md) <br>
- [Merchant development parameters and business rules](references/1-商户/接入指南/开发参数与业务规则.md) <br>
- [Service-provider development parameters and business rules](references/2-服务商/接入指南/开发参数与业务规则.md) <br>
- [Merchant signing and verification rules](references/1-商户/接入指南/签名与验签规则.md) <br>
- [Service-provider signing and verification rules](references/2-服务商/接入指南/签名与验签规则.md) <br>
- [Merchant callback handling](references/1-商户/接入指南/回调处理.md) <br>
- [Service-provider callback handling](references/2-服务商/接入指南/回调处理.md) <br>
- [Merchant interface index](references/1-商户/示例代码/接口索引.md) <br>
- [Service-provider interface index](references/2-服务商/示例代码/接口索引.md) <br>
- [Merchant troubleshooting manual](references/1-商户/问题排查/排障手册.md) <br>
- [Service-provider troubleshooting manual](references/2-服务商/问题排查/排障手册.md) <br>
- [WeChat Pay Score merchant product documentation](https://pay.weixin.qq.com/doc/v3/merchant/4012587050.md) <br>
- [WeChat Pay Score merchant development guide](https://pay.weixin.qq.com/doc/v3/merchant/4012587166.md) <br>
- [WeChat Pay merchant API documentation](https://pay.weixin.qq.com/doc/v3/merchant/4013287010) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with Java and Go code excerpts, checklists, and troubleshooting guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Prompts for integration mode and required details before providing mode-specific references or examples.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
