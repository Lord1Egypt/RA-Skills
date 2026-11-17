## Description:

XiaomiYe helps authorized Renren store administrators query ecommerce operations data and manage products, members, orders, coupons, and shipping rules through configured APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jishuweihu](https://clawhub.ai/user/jishuweihu)

### License/Terms of Use:

MIT-0

## Use Case:

Store operators and ecommerce support teams use this skill to inspect live Renren store metrics, products, members, orders, coupons, and shipping settings. It is intended for authorized administrative contexts where API credentials are already configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles live store credentials and customer data.

Mitigation: Install only in an authorized store-admin context, use HTTPS for RR_CLAW_BASE_URL, and keep the API key least-privileged.

Risk: Business-changing actions can alter product availability, order state, coupons, or shipping rules.

Mitigation: Require explicit user confirmation before every business-changing POST action.

Risk: Customer names, phone numbers, addresses, balances, and order details may be exposed in responses.

Mitigation: Mask customer data unless there is a clear business need to display it.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jishuweihu/skills/syxx)
- [Renren Store Homepage](https://www.rrsc.cn)
- [Data Statistics Module](references/statistics.md)
- [Goods Query and Management Module](references/goods.md)
- [Member Query and Management Module](references/member.md)
- [Order Query and Management Module](references/order.md)
- [Sales Activity Query and Management Module](references/sales.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with API request examples, JSON response handling, and Python client snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce live store API requests when credentials and RR_CLAW_BASE_URL are configured.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence); artifact frontmatter states 2.0.0

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
