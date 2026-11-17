## Description:

Tianmao helps users evaluate and shop through Tmall official-brand channels by comparing flagship stores, prices, reviews, coupons, and preparing carts or order previews before payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping agents use this skill when authenticity, official-store status, 88VIP pricing, and after-sales terms matter on Tmall. It supports product discovery through order preview while leaving final payment to the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can affect cart contents, coupon choices, address selection, and order previews in a logged-in shopping session.

Mitigation: Review every login-gated action before it proceeds, verify the order preview yourself, and complete payment manually.

Risk: Shopping details such as official-store status, prices, coupons, and service guarantees can be stale or misread during browsing.

Mitigation: Confirm store badges, service guarantees, price changes, and coupon effects from the live page before acting on the recommendation.

## Reference(s):

- [Tianmao Skill Page](https://clawhub.ai/harrylabsj/skills/tianmao)
- [Publisher Profile](https://clawhub.ai/user/harrylabsj)
- [Browser Workflow Guide](references/browser-workflow.md)
- [Official Store Guide](references/official-store-guide.md)
- [Output Patterns](references/output-patterns.md)
- [Tmall](https://www.tmall.com/)

## Skill Output:

**Output Type(s):** [text, markdown, guidance, browser automation actions]

**Output Format:** [Markdown shopping comparisons, concise recommendations, cart summaries, and user handoff steps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stops before payment or final order submission; login-gated cart, coupon, address, and order-preview actions require user review.]

## Skill Version(s):

1.2.3 (source: server release metadata; artifact files list 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
