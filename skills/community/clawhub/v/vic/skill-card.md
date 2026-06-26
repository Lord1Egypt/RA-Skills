## Description: <br>
VISA Intelligent Commerce compatible payments and wallet guidance for giving agents controlled spending, checkout, wallet, and payment-link capabilities. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and agent operators use this skill to register payment-enabled agents, inspect spending permissions, request owner-approved purchases, manage wallet balances, and create checkout or payment links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent authority to initiate real payments and card-based purchases. <br>
Mitigation: Install only when real payment handling is intended, keep ask-before-everything enabled initially, and set low spending limits. <br>
Risk: Payment credentials, API keys, webhook secrets, or card details could be exposed to downstream agents or logs. <br>
Mitigation: Protect CREDITCLAW_API_KEY and webhook secrets, avoid sharing credentials with spawned agents, and discard decrypted card data immediately after checkout. <br>
Risk: Webhook-triggered fulfillment can release goods or services on forged or unverified events. <br>
Mitigation: Verify webhook signatures before fulfillment and reconcile completed sales or transactions before delivery. <br>
Risk: Draft or private-beta payment rails may be less stable or intentionally unavailable for general use. <br>
Mitigation: Avoid the draft Crossmint flow and private-beta wallet paths unless they are explicitly enabled for the deployment. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jononovo/vic) <br>
- [CreditClaw skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted card checkout guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Wallet management guide](https://creditclaw.com/management.md) <br>
- [Checkout and selling guide](https://creditclaw.com/checkout.md) <br>
- [Heartbeat polling guide](https://creditclaw.com/heartbeat.md) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline JSON and curl examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for live API use.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
