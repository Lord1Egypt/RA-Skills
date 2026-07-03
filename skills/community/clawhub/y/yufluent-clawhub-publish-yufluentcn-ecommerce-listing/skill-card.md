## Description: <br>
Generates SEO-oriented, multilingual product listings for Amazon, Shopify, and TikTok Shop through the Yufluent cloud harness. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and ecommerce operators use this skill to generate platform-specific titles, bullet points, descriptions, keywords, Shopify metadata, TikTok hashtags, and short-video hooks for multilingual cross-border product listings. Agents use it by collecting product inputs, invoking the Yufluent cloud endpoint, and returning the generated listing for human review before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends a sensitive Yufluent token and product listing inputs to a configurable API endpoint. <br>
Mitigation: Install only if Yufluent/changzhiai is trusted with that data, set TOKENAPI_BASE_URL only to the intended Yufluent endpoint, and keep TOKENAPI_KEY and .env files private. <br>
Risk: Server errors can cause the client to retry through /agent/turn rather than only the narrower listing endpoint. <br>
Mitigation: Review this fallback behavior before deployment and verify that the configured endpoint is the intended Yufluent service. <br>
Risk: Generated ecommerce copy may contain incorrect, unsupported, or platform-sensitive claims. <br>
Mitigation: Review generated listings against the seller's product evidence and the target marketplace rules before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-ecommerce-listing) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [OpenClaw integration](https://claw.changzhiai.com/app/openclaw) <br>
- [Amazon Listing 文案规范参考](references/amazon-style-guide.md) <br>
- [亚马逊平台规则库](references/platform-rules-amazon.md) <br>
- [Shopify 平台规则库](references/shopify-best-practices.md) <br>
- [TikTok Shop 平台规则库](references/tiktok-shop-tips.md) <br>
- [TokenApi 计费标准](references/pricing-table.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Plain text, formatted listing text, or JSON returned on stdout or written to a user-selected output file.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can include run metadata such as run ID, model used, token count, and validation issues when returned by the Yufluent service.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
