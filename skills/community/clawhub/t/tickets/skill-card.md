## Description:

Let your agent shop tickets online with owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and their agents use this skill to register with CreditClaw, check spending permissions, and request owner-approved ticket or online purchases through supported payment rails.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can initiate real financial actions through CreditClaw.

Mitigation: Use it only with a trusted CreditClaw account, keep per-purchase approval enabled, and configure low transaction, daily, and monthly limits.

Risk: CREDITCLAW_API_KEY functions as a spending credential.

Mitigation: Store the key in a secrets manager or protected environment variable and send it only to creditclaw.com API endpoints.

Risk: Remote skill documents may change after installation.

Mitigation: Load remote documents only when their exact versions and hashes have been reviewed and verified.

Risk: Automated purchases may target unwanted merchants or categories.

Mitigation: Set merchant, category, and spending restrictions before use and review owner approval requests before accepting them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/tickets)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md)
- [CreditClaw shopping guide](https://creditclaw.com/creditcard/shopping.md)
- [CreditClaw Amazon guide](https://creditclaw.com/creditcard/amazon.md)
- [CreditClaw pre-paid wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [CreditClaw self-hosted card guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md)
- [CreditClaw skill metadata](https://creditclaw.com/creditcard/skill.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, API calls, Configuration]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and owner-configured spending controls.]

## Skill Version(s):

1.2.5 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
