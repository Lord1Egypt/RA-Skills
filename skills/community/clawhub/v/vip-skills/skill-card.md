## Description: <br>
唯品会技能集 helps agents support Vipshop shopping workflows, including account login, product search, product detail lookup, promotion discovery, and image-based product search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[vip](https://clawhub.ai/user/vip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping agents use this skill to search Vipshop products, inspect product details, browse promotions, authenticate with a Vipshop account, and find visually similar products from a selected image. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill saves and reuses a Vipshop login token locally. <br>
Mitigation: Install only if account-based access is acceptable, and review or remove ~/.vipshop-user-login/tokens.json when retained access is no longer wanted. <br>
Risk: Image search uploads selected local image files to Vipshop. <br>
Mitigation: Upload only images intended for Vipshop image search and avoid submitting sensitive or private images. <br>
Risk: Generated product links may carry login context. <br>
Mitigation: Do not share generated exchange-token links outside the intended session. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/vip/vip-skills) <br>
- [Vipshop User Login API Reference](vipshop-user-login/references/api_reference.md) <br>
- [Vipshop User Login Integration Guide](vipshop-user-login/references/integration_guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown shopping results and guidance based on JSON script output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include product links, login status, promotion data, image-search results, and account-linked exchange-token URLs.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
