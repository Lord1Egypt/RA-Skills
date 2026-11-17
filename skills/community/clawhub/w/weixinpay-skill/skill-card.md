## Description:

微信支付SKILL接入，实现生成微信支付二维码，完成扫码支付，并提供商户入驻、接口集成、运营和敏感凭证管理指引。

This skill is ready for commercial/non-commercial use.

## Publisher:

[piaoleaf](https://clawhub.ai/user/piaoleaf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and guide WeChat Pay integration, especially Native QR-code payment flows, callbacks, refunds, bill downloads, and merchant onboarding. It is intended for environments where authorized administrators manage WeChat Pay merchant credentials outside ordinary user workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WeChat Pay merchant API keys, signing secrets, certificates, and private keys can expose payment systems if pasted into chat or made available to ordinary users.

Mitigation: Restrict credential configuration to authorized administrators, store secrets in managed vaults or equivalent protected systems, rotate credentials regularly, and never paste payment secrets into conversational workflows.

Risk: Refunds, bill downloads, red-packet campaigns, and marketing disbursements can move funds or expose financial records if performed without adequate authorization.

Mitigation: Require explicit approvals, role-based access controls, audit logs, and confirmation checks before financial operations are executed.

Risk: Payment callbacks and order-status updates can be spoofed or mishandled if signature validation and HTTPS callback configuration are incomplete.

Mitigation: Follow WeChat Pay official API validation requirements, use HTTPS callback endpoints, validate signatures before updating order state, and log only non-sensitive operational results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/piaoleaf/skills/weixinpay-skill)
- [WeChat Pay merchant platform](https://pay.weixin.qq.com)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Configuration instructions]

**Output Format:** [Markdown guidance with procedural steps and operational controls]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Focuses on WeChat Pay QR-code payment integration and credential handling guidance; does not require ordinary users to provide sensitive credentials.]

## Skill Version(s):

1.0.7 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
