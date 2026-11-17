## Description:

Builds and debugs Stripe integrations for payments, subscriptions, Checkout, invoices, webhooks, Connect, disputes, tax, testing, and go-live workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to build, review, and troubleshoot Stripe payment, billing, webhook, Connect, tax, dispute, and reconciliation flows. It helps produce Stripe-aware implementation guidance, API examples, debugging steps, go-live checks, and runbook material.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide live financial changes such as charges, refunds, transfers, payouts, subscription cancellations, and deletions.

Mitigation: Use test mode by default, require explicit confirmation before live writes, and add idempotency keys to state-changing Stripe POST requests before execution.

Risk: The skill may persist Stripe contacts, account references, device or network details, incidents, disputes, and fee history across sessions.

Mitigation: Review the skill before installing if that persistence is not desired, and keep stored data limited to the documented local Clawic paths.

Risk: Stripe credentials, webhook signing secrets, client secrets, card data, or other sensitive values could be exposed if copied into notes or examples.

Mitigation: Keep credentials in environment variables or secret stores, store only secret locators, and never write secret keys, webhook secrets, client secrets, PANs, or CVCs to local notes.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/skills/stripe-api-integration)
- [Clawic Skill Page](https://clawic.com/skills/stripe-api-integration)
- [Skill Definition](artifact/SKILL.md)
- [API Mechanics](artifact/api-mechanics.md)
- [Webhooks](artifact/webhooks.md)
- [Payments](artifact/payments.md)
- [Checkout](artifact/checkout.md)
- [Subscriptions](artifact/subscriptions.md)
- [Connect](artifact/connect.md)
- [Tax](artifact/tax.md)
- [Testing](artifact/testing.md)
- [Go Live](artifact/go-live.md)
- [Memory Template](artifact/memory-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code blocks, Stripe API examples, checklists, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Stripe API requests and local note updates; live state-changing operations require explicit confirmation.]

## Skill Version(s):

1.0.4 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
