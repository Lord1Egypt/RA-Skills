## Description: <br>
跨平台电商比价与优惠券聚合工具。当用户询问商品价格、查找优惠券、解析商品链接、寻找今日好价或本地生活优惠时调用。返回多个电商平台的同款商品价格对比和可用券信息。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cheese9102](https://clawhub.ai/user/cheese9102) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and shopping assistants use this skill to compare prices, find coupons, parse shopping links, discover daily deals, and surface local-life discounts across supported Chinese ecommerce and local services. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Shopping queries and pasted product links are sent to an external service, which can expose shopping interests, referral tokens, IP address logs, or account-specific URL details. <br>
Mitigation: Use the skill only for explicit shopping and coupon tasks, avoid private account-specific URLs, and review pasted links before sending them. <br>
Risk: Purchase links may be external affiliate-style redirects that can open platform apps or bind coupons to a user account. <br>
Mitigation: Treat '领券购买' links as external redirects and verify the destination, price, coupon terms, and account impact before acting. <br>
Risk: Prices, coupons, and product matches are time-sensitive and can be misleading when results include accessories or stale offers. <br>
Mitigation: Display freshness notes, avoid claiming guaranteed lowest price, and prompt users to refine keywords when the result appears to match an accessory or unsupported item. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cheese9102/xiaxiayouhui-deals) <br>
- [xiaxiayouhui.xyz homepage](https://xiaxiayouhui.xyz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown shopping results with tables, links, status notes, and concise fallback guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Calls read-only external shopping APIs and renders time-sensitive prices, coupons, product links, and deal summaries.] <br>

## Skill Version(s): <br>
1.6.1 (source: release evidence and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
