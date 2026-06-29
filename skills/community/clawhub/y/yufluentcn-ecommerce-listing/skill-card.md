## Description: <br>
Cross-border ecommerce sellers use this skill to generate SEO-oriented product listings for Amazon, Shopify, and TikTok Shop in multiple languages through the Yufluent cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External sellers and ecommerce operators use this skill to collect product details, call the Yufluent listing service, and produce platform-specific listing copy for Amazon, Shopify, and TikTok Shop. Agents should review the generated content with the user before publication. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product names, keywords, and related listing details to Yufluent's cloud service using a TOKENAPI_KEY. <br>
Mitigation: Use only the intended Yufluent endpoint, protect the tk-* key like a password, and avoid sending data the user is not comfortable sharing with that service. <br>
Risk: Generated ecommerce listings may contain inaccurate, noncompliant, or unsupported claims. <br>
Mitigation: Review all generated listings against the target marketplace rules and product evidence before publishing. <br>


## Reference(s): <br>
- [ClawHub listing page](https://clawhub.ai/metahuan/yufluentcn-ecommerce-listing) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw guide](https://claw.changzhiai.com/app/openclaw) <br>
- [Amazon listing style guide](references/amazon-style-guide.md) <br>
- [Amazon platform rules](references/platform-rules-amazon.md) <br>
- [Shopify best practices](references/shopify-best-practices.md) <br>
- [TikTok Shop tips](references/tiktok-shop-tips.md) <br>
- [Pricing table](references/pricing-table.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Configuration] <br>
**Output Format:** [Markdown, plain text, or JSON listing content produced by the Yufluent API client] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Output varies by selected platform and may include titles, bullet points, descriptions, keywords, meta fields, hashtags, or hooks.] <br>

## Skill Version(s): <br>
1.3.2 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
