## Description:

Use when a buyer just paid Spec72 (Lint/Catalog/Audit/Sprint) or needs the post-pay intake fields for https://spec72.dev/thanks/. Collect pack, repo URL, what breaks, handoff owner, email, tx/receipt - then point humans to Gumroad SKUs. Free pointer skill; Spec72 does the paid work.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hkarlsson00-spec](https://clawhub.ai/user/hkarlsson00-spec)

### License/Terms of Use:

MIT-0

## Use Case:

External buyers and agents use this skill to gather Spec72 post-payment intake details and route users to the correct checkout and handoff links for Spec72 service packs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may include secrets, private credentials, or unnecessary sensitive repository details in the repo URL or problem description.

Mitigation: Ask users to omit secrets and unnecessary sensitive information before sharing intake details with Spec72.

Risk: Incorrect prices or checkout destinations could misroute a buyer.

Mitigation: Use the listed Spec72 checkout links and stated prices, and do not invent SKUs, discounts, or alternate primary checkout providers.

## Reference(s):

- [Spec72](https://spec72.dev)
- [Spec72 Intake](https://spec72.dev/thanks/)
- [Canonical Skill](https://spec72.dev/SKILL.md)
- [Spec72 llms.txt](https://spec72.dev/llms.txt)
- [Lint Checkout](https://karlsson02.gumroad.com/l/lint)
- [Catalog Checkout](https://karlsson02.gumroad.com/l/vtacaw)
- [Audit Checkout](https://karlsson02.gumroad.com/l/enainx)
- [Sprint Checkout](https://karlsson02.gumroad.com/l/sprint)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or plain text intake checklist with service links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute code, submit forms, or persist data; it asks for intake details and points humans to checkout and handoff links.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
