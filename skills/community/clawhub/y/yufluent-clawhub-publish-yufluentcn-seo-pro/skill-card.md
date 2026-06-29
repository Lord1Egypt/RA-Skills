## Description: <br>
Generates structured ecommerce SEO keyword placement reports for Amazon, Shopify, and TikTok Shop from product, seed keyword, competitor keyword, market, and language inputs via Yufluent's cloud service. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[metahuan](https://clawhub.ai/user/metahuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External ecommerce sellers, SEO operators, and agent workflows use this skill to generate keyword research and placement guidance for Amazon A9/backend terms, Shopify on-page and meta fields, and TikTok Shop search and hashtag planning. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends product, seed keyword, competitor keyword, market, language, and TOKENAPI_KEY data to a configured cloud endpoint. <br>
Mitigation: Use the skill only with data approved for Yufluent cloud processing, keep TOKENAPI_KEY private, and set TOKENAPI_BASE_URL only to trusted endpoints. <br>
Risk: Generated SEO keyword reports can be incomplete, incorrect, or unsuitable for a target marketplace or listing. <br>
Mitigation: Review outputs against seller-console data, advertising search terms, platform policies, and product facts before publishing listing changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/metahuan/yufluent-clawhub-publish-yufluentcn-seo-pro) <br>
- [Yufluent console](https://claw.changzhiai.com) <br>
- [Yufluent OpenClaw](https://claw.changzhiai.com/app/openclaw) <br>
- [Artifact README](README.md) <br>
- [Artifact skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, guidance] <br>
**Output Format:** [JSON report, optionally written to a file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Platform-specific keyword structures for Amazon, Shopify, and TikTok Shop; results require human review before use in live listings.] <br>

## Skill Version(s): <br>
1.1.2 (source: server release and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
