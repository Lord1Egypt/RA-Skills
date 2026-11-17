## Description:

Generates differentiated, SEO-aware product descriptions, listings, translations, and comparison content for foreign-trade products across B2B and e-commerce platforms.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External sellers, export teams, and content marketers use this skill to turn product parameters and optional competitor inputs into localized product-description packages for listings, catalogs, independent stores, and B2B platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product, SEO, and competitor-comparison inputs may be sent to Yunlv's TradeGPT API.

Mitigation: Use only approved input data and configure TRADEGPT_API_KEY deliberately for this third-party service.

Risk: Generated files may contain commercially sensitive product descriptions or comparison content.

Mitigation: Review or delete files under ./data/yunlv-skills/productDesc/ before sharing, committing, or reusing them.

Risk: Broad prompts such as SEO may trigger the skill when it is not relevant.

Mitigation: Confirm that the user needs product-description or listing-content generation before using the skill.

Risk: Generated differentiation claims, certifications, and competitor comparisons can be inaccurate if source inputs are incomplete or unsupported.

Mitigation: Verify product specifications, certificates, platform policy compliance, and competitor claims before publication.

## Reference(s):

- [Yunlv AI Homepage](https://yunlvai.com)
- [Yunlv AI TradeGPT API](https://api.yunlvai.com)
- [Industry Vocabulary](references/industry_vocabulary.md)
- [Differentiation Templates](references/differentiation_templates.md)
- [Platform Guide](references/platform_guide.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Configuration, Guidance]

**Output Format:** [Markdown and JSON-like structured content packages with product titles, descriptions, SEO keywords, specifications, FAQs, competitor comparisons, and recommendations.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY for the Yunlv TradeGPT API and may write generated product-description files under ./data/yunlv-skills/productDesc/.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
