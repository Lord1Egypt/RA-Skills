## Description:

Searches Vipshop (vip.com) products by keyword, supports pagination and price filters, and returns structured product details after Vipshop login.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vip](https://clawhub.ai/user/vip)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping assistants use this skill to search Vipshop products, compare prices and discounts, browse result pages, and request details for a selected product.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads the local Vipshop login file and sends account cookies to Vipshop APIs.

Mitigation: Use it only for intended authenticated Vipshop searches, with an account whose access scope and local token storage are acceptable for the environment.

Risk: Generated product links may contain recoverable token data.

Mitigation: Review or disable exchange-token link generation before using the skill with a real account or sharing generated links.

Risk: The skill can install or invoke a separate Vipshop login skill when login state is missing or expired.

Mitigation: Confirm the login skill source and behavior before deployment, and require user confirmation for login setup in managed environments.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vip/skills/vip-product-search)
- [Vipshop](https://www.vip.com/)
- [Vipshop product search API](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/search/product/rank)
- [Vipshop product detail API](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/product/module/list/v2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown or plain text product results formatted from JSON script output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns up to 10 products per page with product IDs, names, images, brand, price, original price, discount, selling points, and product links when available.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
