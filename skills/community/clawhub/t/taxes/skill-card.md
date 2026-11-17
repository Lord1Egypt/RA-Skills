## Description:

Let your agent shop on Amazon with guardrailed wallets and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[triplehippo](https://clawhub.ai/user/triplehippo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent register with CreditClaw, check spending permissions, request owner-approved Amazon purchases, track wallet state, and create checkout or payment flows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real spending and card data.

Mitigation: Use a tightly sandboxed agent, a scoped CreditClaw API key, and explicit owner approval for purchases; treat decrypted card output, webhook payloads, buyer data, and shipping data as highly sensitive.

Risk: Server-delivered instructions and code can influence checkout execution.

Mitigation: Do not execute remotely delivered decrypt scripts or follow free-form remote instructions; use integrity-checked and version-pinned skill files.

Risk: A main-agent card decryption fallback could expose decrypted card details in the main context.

Mitigation: Use an ephemeral checkout sub-agent for card decryption and checkout, and do not store or log decrypted card data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/triplehippo/skills/taxes)
- [CreditClaw Amazon skill](https://creditclaw.com/amazon/skill.md)
- [CreditClaw checkout guide](https://creditclaw.com/amazon/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md)
- [CreditClaw spending permissions](https://creditclaw.com/amazon/spending.md)
- [CreditClaw wallet management](https://creditclaw.com/amazon/management.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/amazon/heartbeat.md)
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/amazon/stripe-x402-wallet.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/amazon/crossmint-wallet.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with curl examples and JSON request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may handle highly sensitive card, webhook, buyer, and shipping data.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
