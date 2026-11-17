## Description:

帮助开发者选择微信支付产品、查找官方接入资料与示例、实现和检查支付集成，并排查接口问题。

This skill is ready for commercial/non-commercial use.

## Publisher:

[tencent-adm](https://clawhub.ai/user/tencent-adm)

### License/Terms of Use:

MIT-0

## Use Case:

开发者和工程团队用它为境内商户选择微信支付接入方案、查阅接口文档、编写或审查支付代码，以及排查交易和验签问题。

### Deployment Geography for Use:

Mainland China (domestic merchants only)

## Known Risks and Mitigations:

Risk: The skill requests network access and can automatically replace its own files with an unsigned remote update.

Mitigation: Review updates and their source before allowing the updater to run; restrict network access to necessary domains.

Risk: Payment credentials, merchant identifiers, certificates, signatures, and authorization headers could appear in chats, commands, or logs.

Mitigation: Keep secrets out of prompts and logs; use placeholders where possible and protect any credentials needed for local tests.

Risk: Live payment API calls or generated integration code can affect financial transactions.

Mitigation: Confirm the target environment and scope before executing calls; review and test code before production use.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/tencent-adm/skills/wechatpay-payment-integration)
- [微信支付接入质量检查清单](artifact/references/接入质量检查清单.md)
- [产品、角色、API 版本与验签方式的确认](artifact/references/产品角色版本与验签方式的确认.md)
- [APIv3 签名验签本地测试](artifact/references/APIv3签名验签本地测试.md)
- [wechatpay-dev-cli 使用说明](artifact/references/wechatpay-dev-cli使用说明.md)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Analysis]

**Output Format:** [Markdown with code and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include integration checklists and test findings.]

## Skill Version(s):

1.0.7 (source: ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
