## Description: <br>
Fetch Amazon market data through the SellerSprite API for product research, keyword analysis, competitor lookup, ASIN details, and Blue Ocean Index scoring. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[boyd4y](https://clawhub.ai/user/boyd4y) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketplace analysts, and Amazon sellers use this skill to run SellerSprite-backed Amazon product, keyword, ASIN, competitor, market, and quota research from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research inputs such as product plans, private ASIN lists, keywords, or market terms may be sent to SellerSprite through the configured API key. <br>
Mitigation: Use this skill only when SellerSprite-backed research is intended and avoid submitting confidential research inputs unless they are approved for sharing with SellerSprite. <br>
Risk: A SellerSprite Open API key is required for authenticated API calls. <br>
Mitigation: Provide the key through SELLERSPRITE_SECRET_KEY or the documented CLI config path, and avoid exposing the key in prompts, shared logs, or generated artifacts. <br>


## Reference(s): <br>
- [API Endpoints](artifact/references/api-endpoints.md) <br>
- [Marketplace Codes](artifact/references/marketplace-codes.md) <br>
- [Error Handling](artifact/references/error-handling.md) <br>
- [SellerSprite Open API](https://open.sellersprite.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional text or JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Bun, @teamclaw/sellersprite-cli, and a SellerSprite Open API key.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
