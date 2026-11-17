## Description:

Shop YHD.com (1号店) with browser automation for search, daily flash sales, fresh grocery selection, cart operations, and membership benefits while keeping checkout and payment under user control.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to get agent-assisted shopping help on 1号店, including product search, flash-sale review, fresh grocery comparison, cart preparation, coupon checks, delivery-slot review, and order preview. The user remains responsible for login consent, final order review, submission, and payment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can prepare live shopping actions such as cart changes, coupon application, delivery-slot selection, and order previews.

Mitigation: Before cart or order-preview steps, confirm the selected products, quantity, account or session use, address, coupon changes, and delivery slot with the user.

Risk: Payment or final order submission would create a financial commitment.

Mitigation: Stop before payment and final submission; the user must manually review the order and complete payment.

Risk: Live prices, stock, coupons, and delivery windows can change during shopping.

Mitigation: Show current evidence from the shopping session and alert the user before proceeding when price, availability, coupon, or delivery-slot details change.

Risk: Login, CAPTCHA, or account-session steps may expose user account controls.

Mitigation: Ask for explicit consent before login-dependent actions and hand authentication or CAPTCHA steps back to the user.

## Reference(s):

- [YHD ClawHub skill page](https://clawhub.ai/harrylabsj/skills/yhd)
- [Publisher profile](https://clawhub.ai/user/harrylabsj)
- [Browser Workflow Guide](artifact/references/browser-workflow.md)
- [YHD website](https://www.yhd.com/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown and plain-language shopping guidance with optional browser automation steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include product comparisons, cart and coupon summaries, delivery-slot options, and an order preview; payment and final order submission remain user-controlled.]

## Skill Version(s):

2.0.1 (source: server release metadata; artifact frontmatter and package metadata show 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
