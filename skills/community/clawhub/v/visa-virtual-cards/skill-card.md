## Description: <br>
VISA Virtual Cards helps agents and OpenClaw bots manage compatible cards, wallets, payments, spending permissions, checkout pages, and payment rails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to let an agent register with CreditClaw, check wallet and spending status, request owner-approved purchases, sign x402/USDC payments, and create checkout pages, invoices, and payment links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill enables real payments, checkout links, invoices, public shop listings, and other money-moving workflows. <br>
Mitigation: Install only when real payment authority is intended, keep ask-for-everything approval enabled where possible, set strict spend limits and category or domain rules, and review payment links, invoices, and shops before sending or publishing. <br>
Risk: CREDITCLAW_API_KEY, webhook secrets, and decrypted card data are sensitive and could expose owner funds if mishandled. <br>
Mitigation: Store secrets in a secrets manager or protected environment variables, send the API key only to creditclaw.com API endpoints, verify webhooks, and never store, log, or persist decrypted card details. <br>
Risk: Draft Crossmint-style merchant ordering can involve sharing shipping details and authorizing physical purchases. <br>
Mitigation: Avoid enabling that flow unless the owner has explicitly approved physical purchases, delivery details, and merchant-specific spending limits. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/jononovo/visa-virtual-cards) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [Main skill documentation](https://creditclaw.com/skill.md) <br>
- [Encrypted card guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Checkout and selling guide](https://creditclaw.com/checkout.md) <br>
- [Management guide](https://creditclaw.com/management.md) <br>
- [Heartbeat guide](https://creditclaw.com/heartbeat.md) <br>
- [Machine-readable skill metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown guidance with curl/bash examples and JSON request/response examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls.] <br>

## Skill Version(s): <br>
2.3.4 (source: server release evidence and skill.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
