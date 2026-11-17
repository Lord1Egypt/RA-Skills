## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent shop online and manage payment flows through CreditClaw wallets, with owner-controlled spending limits, approvals, and order tracking.

### Deployment Geography for Use:

Global; Amazon Pre-paid Wallet purchases require U.S. shipping addresses where documented.

## Known Risks and Mitigations:

Risk: The skill can authorize real-money spending and payment workflows.

Mitigation: Install only when delegated spending is intended; keep ask-for-everything approval enabled unless explicitly accepted, and set tight merchant, category, and budget limits.

Risk: The skill can create payment links that request money from third parties.

Mitigation: Do not enable or use payment-link creation unless that collection workflow is explicitly desired.

Risk: A leaked CreditClaw API key could allow unauthorized spending through the linked account.

Mitigation: Use a least-privilege CreditClaw key, store it in a secure secrets manager, and send it only to CreditClaw API endpoints.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/samsung)
- [CreditClaw skill definition](https://creditclaw.com/creditcard/skill.md)
- [Shopping guide](https://creditclaw.com/creditcard/shopping.md)
- [Amazon purchase guide](https://creditclaw.com/creditcard/amazon.md)
- [Pre-paid Wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [Self-Hosted Cards guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown with inline shell commands and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata); artifact skill metadata reports 2.3.1

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
