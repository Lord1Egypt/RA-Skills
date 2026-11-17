## Description:

Taobao price and competitor comparison assistant. Input a Taobao title/link or product need; compare JD, PDD, and Vipshop using browser-visible evidence, normalize prices, score same-item confidence, and output where to buy. Safe boundary: no login, no order submission, no payment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

External shoppers and shopping assistants use this skill to compare a Taobao product against JD, Pinduoduo, and Vipshop visible listings, normalize prices and promo conditions, and decide whether to buy, wait, avoid, or stay with Taobao.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Visible marketplace prices, coupons, stock, shipping, warranty, and return terms can change or depend on account or address.

Mitigation: Use the skill's output as a comparison aid and recheck final payable price, coupon eligibility, stock, delivery, warranty, and returns before buying.

Risk: A lower listing price may reflect a different specification, package count, seller channel, promo condition, or near-match rather than the same item.

Mitigation: Require visible title, price, spec or version, and URL, normalize by unit and promo conditions, and downgrade recommendations when match or channel evidence is incomplete.

Risk: Marketplace pages may show login walls, CAPTCHA, app-only flows, or other access limits.

Mitigation: Do not log in, solve CAPTCHA, enter personal details, submit orders, or pay; report access limits and use only visible public evidence.

## Reference(s):

- [Category Playbooks](references/category-playbooks.md)
- [Site Notes](references/site-notes.md)
- [Taobao Price Compare on ClawHub](https://clawhub.ai/harrylabsj/skills/taobao-competitor-analyzer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown verdict block, comparison table, and concise risk notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses browser-visible or user-provided marketplace evidence and may include Chinese field labels.]

## Skill Version(s):

2.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
