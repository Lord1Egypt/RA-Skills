## Description: <br>
Guides developers through WeChat Pay Medical Insurance Payment 2.0 integrations, including product selection, API examples, business rules, quality checks, and troubleshooting for merchant and service-provider modes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhangpeng319](https://clawhub.ai/user/zhangpeng319) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to plan, implement, review, and troubleshoot WeChat Pay medical-insurance payment flows for hospitals, pharmacies, internet hospitals, and service providers. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The examples and guidance handle sensitive payment and medical-related data. <br>
Mitigation: Remove or redact full response bodies and headers from logs, avoid logging plaintext callback payloads, and define retention and access controls for openid, location, authorization, payment, and medical-institution fields. <br>
Risk: The integration requires sensitive credentials such as API private keys and APIv3 keys. <br>
Mitigation: Store credentials with least-privilege access controls, keep production keys out of prompts and logs, and validate key use in a test environment before production rollout. <br>
Risk: Copied sample code may be incomplete or unsafe if reused without adaptation. <br>
Mitigation: Review signing, HTTP, callback decryption, idempotency, and sensitive-field encryption paths before use, and test against official WeChat Pay Java or Go examples. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhangpeng319/wechatpay-medical-insurance-payment) <br>
- [Skill definition](artifact/SKILL.md) <br>
- [Merchant product introduction](artifact/references/1-商户/产品选型/产品介绍.md) <br>
- [Merchant development parameters and business rules](artifact/references/1-商户/接入指南/开发参数与业务规则.md) <br>
- [Merchant API index](artifact/references/1-商户/示例代码/接口索引.md) <br>
- [Merchant troubleshooting manual](artifact/references/1-商户/问题排查/排障手册.md) <br>
- [Service-provider product introduction](artifact/references/2-服务商/产品选型/产品介绍.md) <br>
- [Service-provider development parameters and business rules](artifact/references/2-服务商/接入指南/开发参数与业务规则.md) <br>
- [Service-provider API index](artifact/references/2-服务商/示例代码/接口索引.md) <br>
- [Service-provider troubleshooting manual](artifact/references/2-服务商/问题排查/排障手册.md) <br>
- [WeChat Pay merchant medical-insurance product documentation](https://pay.weixin.qq.com/doc/v3/merchant/4016824672.md) <br>
- [WeChat Pay merchant medical-insurance order API](https://pay.weixin.qq.com/doc/v3/merchant/4016781466.md) <br>
- [WeChat Pay medical-insurance troubleshooting guide](https://pay.weixin.qq.com/doc/v3/merchant/4020401138.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with Java or Go code excerpts, integration guidance, troubleshooting steps, and checklists.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The skill asks for integration mode and relevant context before giving examples; it does not directly modify user projects.] <br>

## Skill Version(s): <br>
1.0.2 (source: release metadata; artifact frontmatter says 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
