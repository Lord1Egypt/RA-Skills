## Description:

VISA Virtual Cards helps agents and OpenClaw bots manage CreditClaw-compatible cards, wallets, spending permissions, checkout pages, invoices, and payments.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and their operators use this skill to register and monitor CreditClaw wallets, check spending permissions, request owner-approved purchases through card or x402 rails, and create checkout, invoice, and payment links for receiving funds.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents receive real spending authority and can initiate purchases, payment signatures, invoices, or payment links.

Mitigation: Require review by someone authorized to manage payment risk, keep per-transaction human approval enabled, and confirm spending modes, thresholds, blocked categories, invoice emails, buyer data, and shipping data before deployment.

Risk: Card-handling workflows may expose sensitive payment data during checkout.

Mitigation: Avoid real card details unless the provider can prove a compliant tokenized flow; never store, log, or persist decrypted card details.

Risk: CREDITCLAW_API_KEY authorizes the agent identity and can enable spending if leaked.

Mitigation: Store the key in a secure secret manager and send it only to CreditClaw API endpoints after reviewing all tools and prompts that will run with the skill.

Risk: x402 signing, Crossmint ordering, and remote instruction updates can change what the bot pays for or which data it sends.

Mitigation: Confirm allowed domains, merchants, amounts, recipient addresses, order details, and reviewed artifact version before enabling these flows.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jononovo/skills/visa-virtual-cards)
- [CreditClaw homepage](https://creditclaw.com)
- [CreditClaw main skill reference](https://creditclaw.com/skill.md)
- [Encrypted card checkout guide](https://creditclaw.com/encrypted-card.md)
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md)
- [Wallet management guide](https://creditclaw.com/management.md)
- [Checkout and selling guide](https://creditclaw.com/checkout.md)
- [Heartbeat polling guide](https://creditclaw.com/heartbeat.md)
- [Machine-readable skill metadata](https://creditclaw.com/skill.json)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; outputs may guide API calls that spend money, handle card checkout, sign x402 payments, or create payment collection links.]

## Skill Version(s):

2.3.4 (source: release evidence and artifact/skill.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
