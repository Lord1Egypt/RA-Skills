## Description:

Provides payment wallets, checkout flows, and spending controls that let an agent buy online or request payment through CreditClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let agents register with CreditClaw, check balances and spending permissions, make owner-controlled purchases, and create payment links, invoices, or checkout pages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The API key functions as a spending credential.

Mitigation: Protect CREDITCLAW_API_KEY in a secure secret store, use a dedicated low-limit CreditClaw account, and send the key only to creditclaw.com endpoints.

Risk: The skill asks agents to follow server-provided checkout and card-decryption steps in a real-money flow.

Mitigation: Keep approval set to ask for every purchase unless limited autonomous spending is intentional, validate checkout steps before execution, and isolate checkout work from broad shell, filesystem, and network access.

Risk: Remote skill files or decryption scripts could change after installation.

Mitigation: Verify the exact artifact files or hashes before installing updates, and do not run remotely delivered scripts or free-form instructions without review.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/jononovo/skills/venmo)
- [CreditClaw shopping skill](https://creditclaw.com/shopping/skill.md)
- [CreditClaw checkout guide](https://creditclaw.com/shopping/checkout.md)
- [CreditClaw encrypted card guide](https://creditclaw.com/shopping/encrypted-card.md)
- [CreditClaw spending permissions guide](https://creditclaw.com/shopping/spending.md)
- [CreditClaw wallet management guide](https://creditclaw.com/shopping/management.md)
- [CreditClaw heartbeat guide](https://creditclaw.com/shopping/heartbeat.md)
- [CreditClaw Crossmint wallet guide](https://creditclaw.com/shopping/crossmint-wallet.md)
- [CreditClaw skill metadata](https://creditclaw.com/shopping/skill.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, API calls]

**Output Format:** [Markdown instructions with inline shell commands, JSON examples, and API endpoint guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; outputs may include purchase, wallet, checkout, invoice, and webhook handling steps.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
