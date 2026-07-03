## Description: <br>
微信支付（WeChat Pay）接入支持 skill，帮助开发者进行产品选型、官方文档问答、示例代码查找、接入质量评估和 APIv3 排障。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tencent-adm](https://clawhub.ai/user/tencent-adm) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to integrate, validate, and troubleshoot domestic WeChat Pay merchant and service-provider flows. It guides product selection, official-documentation lookup, example-code discovery, payment-code quality review, and APIv3 request signing or query troubleshooting. <br>

### Deployment Geography for Use: <br>
Mainland China domestic merchant scenarios <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting flows can involve live payment API authorization material, signatures, certificate serial numbers, and merchant identifiers. <br>
Mitigation: Use test or least-privilege WeChat Pay credentials where possible, run signing and API calls locally, and share only sanitized status codes, request IDs, and error bodies. <br>
Risk: Payment integration guidance can affect funds movement, reconciliation, callbacks, and customer-facing checkout behavior. <br>
Mitigation: Require developer review and production testing, keep private keys and APIv3 keys out of client code, and verify signature checks, idempotency, fallback queries, and reconciliation before release. <br>
Risk: The skill may ask the user to execute local documentation sync, CLI, signing, or API query commands. <br>
Mitigation: Review commands before execution, use a controlled local environment, and obtain explicit user consent before operations that access credentials, networks, or payment APIs. <br>


## Reference(s): <br>
- [Skill source](artifact/SKILL.md) <br>
- [基础概念及业务介绍](artifact/references/基础概念及业务介绍.md) <br>
- [文档检索与问答](artifact/references/文档检索与问答.md) <br>
- [APIv3 接口动态排障](artifact/references/APIv3接口动态排障.md) <br>
- [接入质量检查清单](artifact/references/接入质量检查清单.md) <br>
- [wechatpay-dev-cli 使用说明](artifact/references/wechatpay-dev-cli使用说明.md) <br>
- [WeChat Pay official documentation knowledge base archive](https://wx.gtimg.com/resource/wechatpay_api/wechatpay-docs.zip) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown responses with code blocks, CLI commands, JSON snippets, and documentation references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sanitized API troubleshooting status, request IDs, and error bodies.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release evidence; artifact frontmatter lists 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
