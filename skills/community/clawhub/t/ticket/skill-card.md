## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External agents and developers use this skill to register guarded payment wallets, check spending permissions, request approvals or top-ups, and make owner-controlled online purchases or x402 payments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill delegates real spending and payment authority to an agent.

Mitigation: Keep per-purchase approval enabled unless tight merchant, category, and spending limits are configured and reviewed.

Risk: CREDITCLAW_API_KEY is a spending credential.

Mitigation: Store the key in a secrets manager or environment variable, and send it only to creditclaw.com API endpoints.

Risk: Live remote Markdown installation can change without local integrity checks.

Mitigation: Prefer a reviewed package or signed and pinned files before deployment.

Risk: Purchases can require personal or shipping information.

Mitigation: Send only the minimum necessary personal, billing, and shipping data for the approved purchase.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/ticket)
- [CreditClaw skill reference](https://creditclaw.com/creditcard/skill.md)
- [Pre-paid Wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [Self-Hosted Card guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [Stripe x402 Wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown guidance with inline shell commands and JSON request examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; outputs may include purchase requests, approval messages, top-up requests, and wallet status summaries.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata; artifact frontmatter reports 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
