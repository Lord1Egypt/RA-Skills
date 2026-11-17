## Description:

The release artifacts describe CreditClaw workflows for agent shopping, checkout, payment collection, spending guardrails, owner approval, and wallet management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent guidance for CreditClaw registration, wallet status checks, spending controls, checkout pages, invoices, top-ups, and purchase flows. The artifacts center on real-money commerce workflows that require owner approval and payment guardrails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles real spending and payment-card data.

Mitigation: Keep per-purchase approval enabled, use low spending limits, and configure merchant or domain allowlists before authorizing purchases.

Risk: The artifacts describe server-supplied checkout instructions and remotely delivered decryption code.

Mitigation: Avoid running remotely delivered scripts automatically, and require local user approval plus fixed checkout policy before following payment or decryption steps.

Risk: The CREDITCLAW_API_KEY can authorize wallet and spending actions.

Mitigation: Store the key in a secrets manager and send it only to CreditClaw API endpoints.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/jononovo/skills/sap)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw Amazon skill guide](https://creditclaw.com/amazon/skill.md)
- [CreditClaw checkout guide](https://creditclaw.com/amazon/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md)
- [CreditClaw spending guide](https://creditclaw.com/amazon/spending.md)
- [CreditClaw wallet management guide](https://creditclaw.com/amazon/management.md)
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/amazon/stripe-x402-wallet.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/amazon/heartbeat.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/amazon/crossmint-wallet.md)
- [CreditClaw skill metadata](https://creditclaw.com/amazon/skill.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, JSON API examples, and endpoint references]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and human-configured spending approvals or guardrails for payment workflows.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata claims creditclaw-amazon 2.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
