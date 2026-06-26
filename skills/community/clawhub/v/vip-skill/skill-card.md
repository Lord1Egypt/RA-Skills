## Description: <br>
唯品会技能集 helps an agent log in to Vipshop, search products and promotions, inspect product details, and find similar products from images. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill bundle to complete Vipshop shopping workflows, including account login, keyword search, product detail lookup, promotion browsing, and image-based product search. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires users to log in to Vipshop and stores a reusable local Vipshop session. <br>
Mitigation: Install and use it only when Vipshop account access is intended, and clear ~/.vipshop-user-login/tokens.json when the session should no longer be available. <br>
Risk: Automatic login and install behavior can be triggered during shopping workflows. <br>
Mitigation: Review login prompts and update/install prompts before proceeding, and avoid generic shopping requests unless Vipshop results are desired. <br>


## Reference(s): <br>
- [Vipshop Login API Reference](vipshop-user-login/references/api_reference.md) <br>
- [Vipshop Login Integration Guide](vipshop-user-login/references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries with JSON-backed product, login, promotion, and image-search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product identifiers, prices, promotion details, image links, product links, login status, and next-page tokens.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
