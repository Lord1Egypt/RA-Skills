## Description: <br>
Provides multilingual guidance for WeChat Pay Global product selection, integration setup, API references, launch quality checks, and troubleshooting for overseas acquirer-mode payment deployments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and integration teams use this skill to choose WeChat Pay Global payment products, locate official API guidance, prepare acquirer-mode integration details, check launch quality, and troubleshoot cross-border payment issues. <br>

### Deployment Geography for Use: <br>
Global, with artifact guidance noting direct merchant access only for Hong Kong and acquirer-mode access elsewhere. <br>

## Known Risks and Mitigations: <br>
Risk: Payment integration guidance may be incorrect or outdated for regulated production decisions. <br>
Mitigation: Verify direct-connection eligibility, auto-debit consent requirements, API details, and compliance obligations against current official WeChat Pay Global documentation before production use. <br>
Risk: The skill may be mistaken for an authority on production payment behavior even though the security review classifies it as documentation-only guidance. <br>
Mitigation: Treat outputs as reference guidance, require qualified payment engineering review, and use official WeChat Pay documentation as the production source of truth. <br>
Risk: Content-quality issues or ambiguous integration wording could lead to wrong merchant-mode, routing, or parameter choices. <br>
Mitigation: Cross-check merchant access mode, acquirer/sub-merchant identifiers, callback handling, and launch quality checks with the linked official documentation and internal review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tencent-adm/skills/wechatpay-global-payment1) <br>
- [WeChat Pay Global documentation (English)](https://pay.weixin.qq.com/doc/global/v3/en/) <br>
- [WeChat Pay Global documentation (Chinese)](https://pay.weixin.qq.com/doc/global/v3/zh/) <br>
- [WeChat Pay Global llms.txt](https://pay.weixin.qq.com/doc/global/v3/zh/llms.txt) <br>
- [机构模式 产品选型与产品介绍](references/1-机构/产品选型/产品介绍.md) <br>
- [微信支付境外（跨境）业务世界观](references/1-机构/产品选型/跨境支付通用知识.md) <br>
- [机构模式 开发参数获取](references/1-机构/接入指南/开发参数获取.md) <br>
- [机构模式 签名与验签规则（境外）](references/1-机构/接入指南/签名与验签规则.md) <br>
- [机构模式 回调处理（境外）](references/1-机构/接入指南/回调处理.md) <br>
- [机构上线前接入质量检查（境外）](references/1-机构/接入指南/接入质量检查.md) <br>
- [机构模式 接口索引](references/1-机构/示例代码/接口索引.md) <br>
- [机构模式 排障手册（境外）](references/1-机构/问题排查/排障手册.md) <br>
- [多语言术语表](references/glossary.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with references, checklists, API paths, and official documentation links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include multilingual terminology, routing decisions, integration checklists, and troubleshooting steps.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
