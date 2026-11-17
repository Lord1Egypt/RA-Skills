## Description:

人人商城龙虾助手 helps operators query Renren Mall operations, goods, members, orders, coupons, and shipping-promotion settings using user-provided store API credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[imdake](https://clawhub.ai/user/imdake)

### License/Terms of Use:

MIT-0

## Use Case:

External Renren Mall merchants and authorized store operators use this skill to inspect store performance, search products, members, and orders, and prepare confirmed changes such as taking products offline, closing unpaid orders, stopping coupons, or disabling full-amount free-shipping rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live Renren Mall API credentials and can send them to the configured base URL.

Mitigation: Install only for stores you control, configure an HTTPS merchant API URL that you trust, and use a least-privileged, revocable API key.

Risk: Responses may include customer phone numbers, addresses, balances, birthdays, order details, and other sensitive store data.

Mitigation: Display or log personal and order data only when the operator is authorized and the data is necessary for the requested task.

Risk: Some supported POST actions change live commerce state, including taking products offline, closing orders, stopping coupons, and disabling free-shipping rules.

Mitigation: Require explicit operator confirmation before executing business-changing actions and summarize the target object and expected effect before submission.

Risk: The security verdict is suspicious because URL and privacy safeguards are insufficient.

Mitigation: Review the configured endpoint and privacy handling before deployment, and rotate credentials if they may have been sent to an untrusted or plaintext endpoint.

## Reference(s):

- [Renren Mall homepage](https://www.rrsc.cn)
- [ClawHub skill page](https://clawhub.ai/imdake/skills/renren-claw)
- [数据统计模块](references/statistics.md)
- [商品查询管理模块](references/goods.md)
- [订单查询管理模块](references/order.md)
- [会员查询管理模块](references/member.md)
- [营销活动查询管理模块](references/sales.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline JSON, Python, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include live store data summaries and proposed business actions; destructive actions require explicit operator confirmation.]

## Skill Version(s):

1.0.8 (source: server release metadata; artifact frontmatter reports 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
