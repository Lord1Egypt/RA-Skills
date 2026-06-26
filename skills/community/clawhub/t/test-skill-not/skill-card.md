## Description: <br>
Guides developers through WeChat Pay delegated-withholding integration for recurring deductions and pay-later flows, including product selection, signing, deduction, refund, reconciliation, callback handling, quality checks, and troubleshooting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yinwuzhe](https://clawhub.ai/user/yinwuzhe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration engineers use this skill to plan, implement, review, and troubleshoot WeChat Pay delegated-withholding flows for merchant or service-provider integrations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment, refund, deduction, and termination examples are production-sensitive. <br>
Mitigation: Use HTTPS callbacks, verify signatures, confirm user and business authorization, and test with safe amounts or sandbox-like flows where available. <br>
Risk: API keys and certificates can be exposed if pasted into prompts or committed with examples. <br>
Mitigation: Keep API keys and certificates outside prompts and source code; use secure secret storage and environment-specific configuration. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/yinwuzhe/test-skill-not) <br>
- [Merchant product introduction](artifact/references/1-商户/产品选型/产品介绍.md) <br>
- [Service-provider product introduction](artifact/references/2-服务商/产品选型/产品介绍.md) <br>
- [Merchant signing and signature verification rules](artifact/references/1-商户/接入指南/签名与验签规则.md) <br>
- [Service-provider signing and signature verification rules](artifact/references/2-服务商/接入指南/签名与验签规则.md) <br>
- [Merchant callback handling](artifact/references/1-商户/接入指南/回调处理.md) <br>
- [Service-provider callback handling](artifact/references/2-服务商/接入指南/回调处理.md) <br>
- [WeChat Pay merchant delegated-withholding product introduction](https://pay.weixin.qq.com/doc/v2/merchant/4011986647.md) <br>
- [WeChat Pay merchant delegated-withholding integration flow](https://pay.weixin.qq.com/doc/v2/merchant/4011986709.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown guidance with retrieved API examples, checklists, and troubleshooting steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Does not install executable code or directly perform payment actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter version: 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
