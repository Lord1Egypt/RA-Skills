## Description:

Waimai takeout decision assistant. Input cuisine, budget, location constraints, merchant candidates, or a takeout link; compare delivery fee, minimum order, discounts, meal fit, timing, and merchant risk. Safe boundary: no login, no order submission, no payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to compare public takeout merchant and promotion signals, including delivery fees, minimum orders, discounts, timing, meal fit, and merchant risk. It supports advisory ordering decisions only and does not log in, submit orders, or initiate payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Advice may be outdated or incomplete because final prices, delivery timing, coupons, and terms can change at checkout.

Mitigation: Recheck final prices, fees, delivery time, coupons, and terms before paying.

Risk: The skill is advisory and should not be treated as an ordering or account-access workflow.

Mitigation: Do not rely on it to place orders, access accounts, submit payment, handle cookies, or perform checkout actions.

## Reference(s):

- [Comparison Guide](references/comparison-guide.md)
- [Output Patterns](references/output-patterns.md)
- [Risk Signals](references/risk-signals.md)

## Skill Output:

**Output Type(s):** [guidance, markdown]

**Output Format:** [Markdown with sections for best option, rationale, caveats, and final advice]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Advisory public takeout comparison; final prices, fees, delivery time, coupons, and terms must be rechecked before paying.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
