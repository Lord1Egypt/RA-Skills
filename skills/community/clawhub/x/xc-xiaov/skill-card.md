## Description:

唯品会专属 AI 购物助手“小v”。当用户提及购物、穿搭建议、时尚趋势或特定商品搜索时，小v 会动态调用内部子技能提供商品推荐、详情查询及促销活动。

This skill is ready for commercial/non-commercial use.

## Publisher:

[bfkkkd](https://clawhub.ai/user/bfkkkd)

### License/Terms of Use:

MIT-0

## Use Case:

External shopping users use this agent skill to search Vipshop products, inspect product details, browse promotions, and receive formatted shopping recommendations after login.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can require a global installation of the Vipshop CLI package before shopping or promotion queries.

Mitigation: Install only after confirming trust in the package, or use a sandboxed and pre-vetted local CLI environment.

Risk: The skill can initiate Vipshop account login flows and expose QR login links or local QR image paths in chat.

Mitigation: Confirm before login, avoid sharing QR login links or local image paths in persistent chat logs, and verify login completion through the CLI status or poll response.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/bfkkkd/skills/xc-xiaov)
- [Vipshop product detail API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/detail/main/v6)
- [Vipshop product search API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/pc/search/product/rank)
- [Vipshop product module API endpoint](https://mapi-pc.vip.com/vips-mobile/rest/shopping/pc/product/module/list/v2)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown tables or plain text summaries with inline shell commands when login or CLI actions are needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Product search results are structured around product identifiers, names, prices, discounts, brands, product links, promotion links, and login status messages.]

## Skill Version(s):

1.0.5 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
