## Description:

Automates TikTok Shop operations including product management, order processing, sales analytics, video publishing, and marketing workflow support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lvjunjie-byte](https://clawhub.ai/user/lvjunjie-byte)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and ecommerce operators can use this skill to prepare CLI-driven TikTok Shop automation for catalog updates, order synchronization, fulfillment workflows, reporting, competitor monitoring, and Feishu notifications. It is suited to sellers who need repeatable operational commands and are prepared to review credential, customer-data, and business-action controls before live use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can handle TikTok Shop credentials, session cookies, and Feishu tokens.

Mitigation: Use test or least-privilege credentials, avoid passing cookies or tokens on the command line, and inspect file permissions for local configuration under ~/.clawhub/tiktok-shop before use.

Risk: Live order fulfillment, refunds, pricing, inventory, customer exports, and Feishu synchronization can affect customers, business records, or external systems.

Mitigation: Keep mock mode enabled during evaluation and require an operator approval process before enabling live business-changing actions or customer-data sync.

Risk: Order synchronization may move customer names, emails, order IDs, amounts, and logistics fields into Feishu.

Mitigation: Confirm data-handling permissions, minimize synced fields, and apply access controls and retention policies in the target Feishu workspace.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lvjunjie-byte/skills/tiktok-shop-publish)
- [Publisher profile](https://clawhub.ai/user/lvjunjie-byte)
- [TikTok Shop Seller Center](https://seller.tiktok.com/)
- [TikTok Shop Partner documentation](https://partner.tiktokshop.com/)
- [TikTok Marketing API](https://business-api.tiktok.com/)
- [Feishu Open Platform](https://open.feishu.cn/)
- [ClawHub TikTok Shop documentation](https://docs.clawhub.com/tiktok-shop)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with CLI commands, configuration examples, JSON responses, and generated report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration and report files and may call TikTok Shop or Feishu APIs when live integrations are enabled.]

## Skill Version(s):

1.0.0 (source: server release metadata, package.json, clawhub.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
