## Description:

购物助手 is a shopping assistant that helps an agent look up coupons, compare prices across Taobao, JD, and Pinduoduo, review price history, and suggest lower-cost purchase options.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wuhaichao87](https://clawhub.ai/user/wuhaichao87)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping agents use this skill to evaluate product links, find available coupons, compare marketplace prices, and produce purchase suggestions. It is most useful when users want concise shopping guidance across Chinese e-commerce platforms.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may silently rewrite shopping links into affiliate-tracked links that can generate commissions.

Mitigation: Label affiliate links clearly, ask for opt-in consent before conversion, and offer a direct-link mode when users do not want tracking.

Risk: Affiliate credentials are requested in a shared OpenClaw environment file.

Mitigation: Store credentials in a scoped secret store or a locked-down file with least-privilege access rather than a broadly shared environment file.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wuhaichao87/skills/shopping-assistant)
- [Taobao](https://www.taobao.com)
- [JD.com](https://www.jd.com)
- [Pinduoduo](https://www.pinduoduo.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and structured coupon, price comparison, and purchase recommendation summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returned prices, coupons, and product availability may be time-sensitive; purchase links may be affiliate-tracked.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
