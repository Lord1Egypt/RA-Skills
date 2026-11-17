## Description:

跨境电商多平台（亚马逊、Shopify、TikTok Shop）SEO 导向 Listing 生成技能，使用 Yufluent 云端 Harness 生成多语言产品标题、五点描述、详情、搜索关键词和平台特定字段。

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agents use this skill to collect product details and request platform-specific listing copy for Amazon, Shopify, or TikTok Shop. The generated copy is intended for human review before publication.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The reviewed package is not self-contained and can load neighboring Python client code.

Mitigation: Review before installing, verify that yufluent_api.py is present and from the publisher, and avoid shared writable skill or _shared directories.

Risk: The skill uses a TOKENAPI_KEY for cloud execution.

Mitigation: Use a scoped, rotatable TOKENAPI_KEY and avoid committing or sharing the token.

Risk: Submitted product details and identifiers are processed by Yufluent's remote service.

Mitigation: Confirm that sending product information to the remote service is acceptable for the deployment.

Risk: Dependencies are not fully pinned for controlled deployments.

Mitigation: Pin dependencies and review installed packages before production use.

Risk: Generated ecommerce copy may require platform and factual review before use.

Mitigation: Manually review generated listings for accuracy, policy compliance, and seller-term compliance before publishing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/metahuan/skills/yufluentcn-ecommerce-listing)
- [Yufluent listing skill homepage](https://www.changzhiai.com/skills/listing)
- [OpenClaw and Yufluent integration](https://claw.changzhiai.com/app/openclaw)
- [Reference files overview](references/README.md)
- [Amazon Listing 文案规范参考](references/amazon-style-guide.md)
- [亚马逊平台规则库](references/platform-rules-amazon.md)
- [Shopify Best Practices](references/shopify-best-practices.md)
- [TikTok Shop Tips](references/tiktok-shop-tips.md)
- [Pricing Table](references/pricing-table.md)
- [Amazon Style Guide](https://sellercentral.amazon.com/gp/help/external/G200390640)
- [Amazon Listing Quality Dashboard](https://sellercentral.amazon.com/listingquality)

## Skill Output:

**Output Type(s):** [text, markdown, json, files, shell commands, configuration, guidance]

**Output Format:** [Markdown-style listing text or JSON, optionally written to a local text file with run metadata.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TOKENAPI_KEY and sends submitted product details to the Yufluent remote listing service; generated listings require human review before publication.]

## Skill Version(s):

1.3.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
