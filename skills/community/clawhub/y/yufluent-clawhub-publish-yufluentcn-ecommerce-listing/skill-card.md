## Description:

Generates SEO-oriented multilingual product listing copy for Amazon, Shopify, and TikTok Shop through Yufluent's cloud listing service.

This skill is ready for commercial/non-commercial use.

## Publisher:

[metahuan](https://clawhub.ai/user/metahuan)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, ecommerce operators, and agents use this skill to collect product details and generate platform-specific titles, bullet points, descriptions, keywords, and related listing metadata for Amazon, Shopify, and TikTok Shop.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product names, keywords, optional selling points, and the Yufluent API key are sent to the configured Yufluent service.

Mitigation: Use the official intended Yufluent endpoint, keep TOKENAPI_BASE_URL trusted, and protect TOKENAPI_KEY as a credential.

Risk: Generated listing copy can be inaccurate, overclaim product capabilities, or conflict with marketplace seller rules.

Mitigation: Review every generated listing before publishing and verify claims against platform rules and product evidence.

Risk: Misconfigured TOKENAPI_BASE_URL can route product data and credentials to an unintended service.

Mitigation: Leave TOKENAPI_BASE_URL unset for the expected default during local use or set it only to the official production endpoint.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/metahuan/skills/yufluent-clawhub-publish-yufluentcn-ecommerce-listing)
- [Yufluent Console](https://claw.changzhiai.com)
- [OpenClaw Yufluent Setup](https://claw.changzhiai.com/app/openclaw)
- [Amazon Listing Copy Reference](references/amazon-style-guide.md)
- [Amazon Platform Rules](references/platform-rules-amazon.md)
- [Shopify Best Practices](references/shopify-best-practices.md)
- [TikTok Shop Tips](references/tiktok-shop-tips.md)
- [Pricing Table](references/pricing-table.md)
- [Amazon Style Guide](https://sellercentral.amazon.com/gp/help/external/G200390640)
- [Amazon Listing Quality Dashboard](https://sellercentral.amazon.com/listingquality)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration, guidance]

**Output Format:** [Formatted listing text or JSON, with optional file output from the CLI.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports Amazon, Shopify, TikTok Shop, and json formats; output may include run metadata such as run_id, model, and token count.]

## Skill Version(s):

1.3.2 (source: evidence.release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
