## Description:

查询唯品会商品详情，并返回价格、优惠、图片、评价、品牌和商品链接等结构化信息。

This skill is ready for commercial/non-commercial use.

## Publisher:

[viphgta](https://clawhub.ai/user/viphgta)

### License/Terms of Use:

MIT-0

## Use Case:

External users and shopping agents use this skill to look up Vipshop product details from a product ID or product link after Vipshop login is available. It summarizes product images, pricing, discounts, service tags, authenticity information, reviews, and a product link for user-facing comparison or purchase decisions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated product links can expose a logged-in Vipshop session.

Mitigation: Return ordinary product-detail URLs unless the publisher removes token-bearing auto-login links and prevents session material from being printed or returned.

Risk: The skill can automatically install or run a separate login skill.

Mitigation: Require explicit user approval and a pinned, reviewed login dependency before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/viphgta/skills/vipshop-product-detail)
- [Vipshop product detail main API](https://mapi-pc.vip.com/vips-mobile/rest/shopping/skill/detail/main/v6)
- [Vipshop exchange-token endpoint](https://passport.vip.com/exchangeTokenFromApp)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [JSON from the script, then Markdown or plain text product-detail summary for the user]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes up to three product images and up to two highlighted reviews when returned by the source service.]

## Skill Version(s):

1.0.7 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
