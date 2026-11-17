## Description:

Designs tiered quantity-break discounts for DTC skincare and beauty stores, including margin-safe tier tables, PDP and cart copy, implementation guidance, and a measurement plan.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rijoyai](https://clawhub.ai/user/rijoyai)

### License/Terms of Use:

MIT-0

## Use Case:

External DTC skincare and beauty merchants use this skill to plan buy-more-save-more offers that raise AOV while preserving gross margin. It helps define product scope, discount tiers, margin checks, on-site copy, implementation notes, and validation metrics.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Discount recommendations can erode gross margin if unit economics, stacking rules, or promotion constraints are incomplete.

Mitigation: Validate suggested tiers against actual gross margin, minimum margin floors, and platform promotion rules before implementing them.

Risk: A general AOV request may not include enough detail to choose product scope or tier depth confidently.

Mitigation: Collect product scope, gross margin, current units per order, platform, stacking constraints, and campaign goals before finalizing the offer.

## Reference(s):

- [Margin and Tier Guidelines](references/margin_and_tiers.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, configuration]

**Output Format:** [Markdown with tier tables, copy blocks, implementation notes, and measurement plans]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes margin checks and concrete promotion guardrails when pricing and margin inputs are available.]

## Skill Version(s):

0.1.1 (source: ClawHub server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
