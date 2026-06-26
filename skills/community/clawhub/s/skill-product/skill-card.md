## Description: <br>
Generates differentiated, localized product descriptions for foreign-trade listings, B2B platforms, catalogs, and SEO-focused product pages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and business teams use this skill to create multilingual product content, differentiated selling points, SEO titles, platform-specific descriptions, specifications, FAQs, and competitor comparisons for export and B2B sales channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a YunlvAI TradeGPT API key and sends product-content generation requests to an external API. <br>
Mitigation: Use a dedicated API key, scope or rotate it where possible, and avoid submitting confidential unreleased product or competitor information unless the provider is trusted. <br>
Risk: Generated certifications, customs descriptions, SEO claims, and competitor comparisons may be inaccurate or unsuitable for publication. <br>
Mitigation: Fact-check certification details, customs language, SEO claims, and comparison data before using generated content in public listings or marketing materials. <br>
Risk: Generated outputs may be saved locally in the product description data folder. <br>
Mitigation: Review ./data/yunlv-skills/productDesc/ for saved outputs and remove sensitive drafts when they are no longer needed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skill-product) <br>
- [YunlvAI Homepage](https://yunlvai.com) <br>
- [YunlvAI TradeGPT API](https://api.yunlvai.com) <br>
- [Industry Vocabulary](references/industry_vocabulary.md) <br>
- [Differentiation Templates](references/differentiation_templates.md) <br>
- [Platform Guide](references/platform_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown or structured JSON-style product-content packages with titles, keywords, descriptions, selling points, tables, FAQs, scores, and recommendations.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY and may save generated product content under ./data/yunlv-skills/productDesc/.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
