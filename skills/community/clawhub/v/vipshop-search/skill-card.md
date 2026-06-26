## Description: <br>
Searches Vipshop products by keyword, retrieves product details, and formats prices, brands, discounts, and product links for the user. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[viphgta](https://clawhub.ai/user/viphgta) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to search Vipshop for products, compare prices and discounts, page through results, and request details for a selected result. The skill requires a Vipshop login token before making authenticated search and detail requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill reads the local Vipshop login token file and uses that token with Vipshop APIs. <br>
Mitigation: Install only on trusted machines, avoid shared environments, and use the skill only for explicit Vipshop searches. <br>
Risk: Generated product links may include account-linked session material. <br>
Mitigation: Do not share generated exchange links and treat them as account-sensitive. <br>
Risk: The workflow may automatically install or invoke related Vipshop skills during login handling. <br>
Mitigation: Review companion skills before allowing install or execution, especially login-related flows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/viphgta/vipshop-search) <br>
- [Vipshop Website](https://www.vip.com/) <br>
- [Vipshop Product Search API Endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/search/product/rank) <br>
- [Vipshop Product Detail API Endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/product/module/list/v2) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [JSON from Python scripts, formatted by the agent as Markdown tables or plain text.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reads a local Vipshop login token and returns up to 10 products per search page.] <br>

## Skill Version(s): <br>
1.0.10 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
