## Description: <br>
Provides agent-facing CreditClaw payment workflows for purchases, checkout pages, encrypted card checkout, wallets, spending guardrails, and owner approvals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to let an agent register with CreditClaw, request spending approval, manage balances, and execute purchases or payment collection through CreditClaw APIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release title and shopping framing may understate the broad CreditClaw spending, card-handling, payment-collection, invoicing, and storefront authority documented by the artifact. <br>
Mitigation: Install only when broad CreditClaw payments authority is intended, and review enabled rails and workflows before use. <br>
Risk: The CreditClaw API key can authorize payment actions and should be treated as sensitive spending authority. <br>
Mitigation: Store CREDITCLAW_API_KEY in a secrets manager, never send it outside creditclaw.com API requests, and rotate it if exposure is suspected. <br>
Risk: Auto-spend, seller, invoice, and payment recipient workflows can move or collect funds without sufficient human review if configured too broadly. <br>
Mitigation: Use ask-for-everything approval by default, verify all recipients and domains, and avoid auto-spend or seller/invoice features unless explicitly needed. <br>
Risk: Encrypted card checkout can expose decrypted card details if run in a logging or persistent-context environment. <br>
Mitigation: Avoid the encrypted-card rail unless checkout can run in an isolated no-log environment with ephemeral handling of decrypted card data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TripleHippo/taxes) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [Main CreditClaw skill file](https://creditclaw.com/amazon/skill.md) <br>
- [CreditClaw checkout guide](https://creditclaw.com/amazon/checkout.md) <br>
- [CreditClaw encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md) <br>
- [CreditClaw spending guide](https://creditclaw.com/amazon/spending.md) <br>
- [CreditClaw Stripe x402 wallet guide](https://creditclaw.com/amazon/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, API calls, guidance] <br>
**Output Format:** [Markdown instructions with curl commands and JSON API payload examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; workflows may involve owner approval, spending guardrails, payment recipient verification, and secret handling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
