## Description: <br>
XiaomiYe helps agents query Renren Mall operating data and manage products, members, orders, coupons, and free-shipping settings through a user-configured Renren Mall API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jishuweihu](https://clawhub.ai/user/jishuweihu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and ecommerce support agents use this skill to inspect live Renren Mall data, answer operational questions, and prepare or execute confirmed administrative actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access a live ecommerce backend and retrieve sensitive order, member, and operational data. <br>
Mitigation: Install only for trusted users, verify RR_CLAW_BASE_URL points to the intended HTTPS store API, and use the least-privilege API key available. <br>
Risk: Broad member or order queries can expose more customer or transaction data than needed. <br>
Mitigation: Use narrow search terms, pagination, and task-specific filters, and avoid unnecessary bulk member or order dumps. <br>
Risk: Product, order, coupon, and shipping-setting actions can affect live storefront behavior or customer transactions. <br>
Mitigation: Require explicit user confirmation before submitting any product, order, coupon, or shipping-setting change. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jishuweihu/syxx) <br>
- [Renren Mall Homepage](https://www.rrsc.cn) <br>
- [Data Statistics Module](references/statistics.md) <br>
- [Goods Query and Management Module](references/goods.md) <br>
- [Order Query and Management Module](references/order.md) <br>
- [Member Query and Management Module](references/member.md) <br>
- [Sales Campaign Query and Management Module](references/sales.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown, JSON API responses, Python snippets, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include live ecommerce records returned by the configured Renren Mall API.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence; skill frontmatter states 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
