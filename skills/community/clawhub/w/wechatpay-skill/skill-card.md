## Description: <br>
Helps developers integrate WeChat Pay V3 flows with product selection guidance, Python and Node.js examples, signing and callback handling notes, quality checks, and troubleshooting references. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jie868](https://clawhub.ai/user/jie868) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to choose appropriate WeChat Pay products, retrieve payment and refund code examples, understand signing and callback requirements, assess integration readiness, and troubleshoot common payment issues. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment callback and refund examples may be copied into production before they are made safe for real credentials and money movement. <br>
Mitigation: Treat examples as reference material, replace placeholder or stub verification with official WeChat Pay signature verification, and reject invalid callbacks before business processing. <br>
Risk: Improper retry handling can duplicate payment fulfillment or refund actions. <br>
Mitigation: Handle callbacks and refund retries idempotently, reuse stable merchant order and refund identifiers, and test duplicate notifications in a non-production environment. <br>
Risk: Merchant private keys, APIv3 keys, or payment data can be exposed through code or logs. <br>
Mitigation: Load secrets from environment variables or a key management service, avoid committing credentials, and redact sensitive values from logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jie868/wechatpay-skill) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/jie868) <br>
- [Metadata homepage: wechatpay-skills](https://github.com/wechatpay-apiv3/wechatpay-skills) <br>
- [Python API index](references/代码示例/接口索引/Python接口索引.md) <br>
- [Node.js API index](references/代码示例/接口索引/Node.js接口索引.md) <br>
- [Merchant signing and verification rules](references/商户模式/签名与验签/签名与验签规则.md) <br>
- [Merchant callback handling](references/商户模式/回调处理/回调处理.md) <br>
- [Merchant integration quality checklist](references/商户模式/接入检查/接入质量检查清单.md) <br>
- [Merchant troubleshooting guide](references/商户模式/排障手册/排障手册.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with code blocks, checklists, tables, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are intended as reference material and should be reviewed before use with real merchant credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
