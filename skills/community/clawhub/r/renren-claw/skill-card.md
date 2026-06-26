## Description: <br>
人人商城龙虾助手 helps agents query Renren Shop operations, products, members, orders, coupons, and shipping settings using the user's configured API credentials. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[imdake](https://clawhub.ai/user/imdake) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External store operators and ecommerce support agents use this skill to inspect Renren Shop operational data, products, members, orders, coupons, and shipping settings. The skill can also guide confirmed order, product, coupon, and shipping changes against a live store API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access live ecommerce store data, including customer, member, phone-number, and order details. <br>
Mitigation: Install only for trusted users, use the least-privileged API key available, and limit customer or phone-number lookups to real business needs. <br>
Risk: Configured order, product, coupon, and shipping actions can change live store state and cause business impact. <br>
Mitigation: Manually review every mutating action and require explicit user confirmation before sending POST requests. <br>
Risk: A wrong RR_CLAW_BASE_URL could send credentials or requests to an unintended endpoint. <br>
Mitigation: Verify RR_CLAW_BASE_URL before use and avoid pasting API credentials into chat. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/imdake/renren-claw) <br>
- [人人商城 homepage](https://www.rrsc.cn) <br>
- [Data statistics API reference](references/statistics.md) <br>
- [Goods API reference](references/goods.md) <br>
- [Member API reference](references/member.md) <br>
- [Order API reference](references/order.md) <br>
- [Sales and marketing API reference](references/sales.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, JSON, Configuration] <br>
**Output Format:** [Markdown guidance with API endpoint mappings and JSON API responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires RR_CLAW_API_KEY and RR_CLAW_BASE_URL; mutating POST actions require explicit user confirmation.] <br>

## Skill Version(s): <br>
1.0.8 (source: server release evidence; artifact frontmatter reports 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
