## Description:

Help users decide whether Vipshop is the best place for branded discount buying, then assist with flash sales, inventory checks, cart preparation, coupon use, and order previews before payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers use this skill to evaluate Vipshop branded-discount purchases, compare sale and member prices, check inventory, and prepare a cart or order preview. It is intended to keep final order submission and payment under user control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may use a logged-in browser session to view cart details, apply coupons, select or confirm delivery information, and prepare an order preview.

Mitigation: Ask for explicit consent before account-based browser automation, keep payment and final order submission manual, and have the user review address, cart, and pricing details.

Risk: Flash-sale inventory, coupon validity, and prices can change before checkout.

Mitigation: Snapshot the current product, stock, coupon, and price details during assistance and alert the user to review the final order before paying.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/vip)
- [Browser Workflow Guide](references/browser-workflow.md)
- [Discount Guide](references/discount-guide.md)
- [Output Patterns](references/output-patterns.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with product comparisons, selected-product details, cart summaries, caveats, and next-step guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include browser action status updates and order preview details, but excludes payment execution or final order submission.]

## Skill Version(s):

1.2.3 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
