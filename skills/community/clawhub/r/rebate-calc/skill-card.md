## Description:

精确计算商品返利后真实到手价的计算工具，支持多种优惠叠加场景，帮助用户在下单前算清每一分钱。

This skill is ready for commercial/non-commercial use.

## Publisher:

[fangshan101-coder](https://clawhub.ai/user/fangshan101-coder)

### License/Terms of Use:

MIT-0

## Use Case:

Shoppers and shopping-assistant agents use this skill to calculate final out-of-pocket prices after stacked discounts, coupons, rebates, red packets, and platform subsidies. It is useful for comparing purchase options and explaining the savings calculation before checkout.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Incorrect arithmetic, rebate terms, or discount stacking assumptions could mislead purchase decisions.

Mitigation: Verify the calculation, stacking order, merchant thresholds, coupon conditions, and rebate terms before checkout.

Risk: Broad shopping-related trigger phrases may activate the skill for requests where a rebate calculation is not intended.

Mitigation: Confirm that the user wants a final-price or rebate calculation before applying the workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/fangshan101-coder/skills/rebate-calc)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown calculation summary with itemized price, discount, rebate, final-price, and savings details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Users should verify arithmetic, discount stacking order, merchant thresholds, and rebate terms before purchasing.]

## Skill Version(s):

0.1.0 (source: frontmatter and ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
