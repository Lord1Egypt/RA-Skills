## Description:

Use when a user needs to generate differentiated product descriptions for foreign trade, B2B platforms, e-commerce sites, catalogs, international localization, and SEO-optimized product content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External business users and marketing teams use this skill to turn product parameters, target markets, platform needs, and optional competitor descriptions into differentiated B2B product content. It supports product descriptions, SEO titles and keywords, selling points, specifications, FAQs, competitor comparisons, and multilingual or platform-specific adaptations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product details, draft listings, or competitor descriptions may be sent to YunlvAI's TradeGPT API.

Mitigation: Use the skill only for explicit B2B or export product-description work, avoid sensitive proprietary inputs unless external API sharing is acceptable, and confirm TRADEGPT_API_KEY use before invocation.

Risk: Generated product claims, certifications, SEO terms, and competitor comparisons may be inaccurate, unverifiable, or platform-sensitive.

Mitigation: Review generated content against product records, certificates, platform policies, and competitor evidence before publication.

Risk: Local generated output or logs may retain product content.

Mitigation: Review and manage the local data folders used for generated descriptions, SEO content, product imports, and logs according to retention expectations.

## Reference(s):

- [Yunlv Homepage](https://yunlvai.com)
- [Yunlv TradeGPT API](https://api.yunlvai.com)
- [Industry Vocabulary](references/industry_vocabulary.md)
- [Differentiation Templates](references/differentiation_templates.md)
- [Platform Guide](references/platform_guide.md)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or JSON content packages with product copy, SEO fields, selling points, comparison tables, adaptation guidance, and optional CLI command output.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May call YunlvAI TradeGPT API when TRADEGPT_API_KEY is configured; local helper commands can emit structured JSON.]

## Skill Version(s):

1.1.0 (source: server release and clawhub.yaml; SKILL.md frontmatter lists 1.0.4)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
