## Description: <br>
Replit Payments & Wallet gives agents and OpenClaw bots payment, wallet, checkout, spending-control, and financial-management workflows through CreditClaw. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codejika](https://clawhub.ai/user/codejika) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to let an agent register with CreditClaw, receive owner activation, check spending rules, request approvals, make purchases through enabled payment rails, and create checkout or payment collection flows. It is intended for agents that intentionally need controlled access to real spending, wallet, card, invoice, or storefront operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can enable an agent to spend real money, decrypt card details for approved checkout, and operate public commerce features. <br>
Mitigation: Install only for agents that intentionally need payment authority; require explicit human approval, set low spending limits, and enable checkout, invoice, shop, or payment-link features only when needed. <br>
Risk: Leaked CreditClaw API keys or webhook secrets could let another actor impersonate the agent or observe payment workflow events. <br>
Mitigation: Store CREDITCLAW_API_KEY and webhook secrets in a secrets manager, never send them outside creditclaw.com API calls, and keep them out of logs, prompts, and subtasks. <br>
Risk: Decrypted card data could be exposed if retained, logged, or passed to unrelated tools during checkout. <br>
Mitigation: Keep decrypted card data only in memory for the active transaction, discard it immediately after checkout, and prevent logging or downstream task capture of decrypted card fields. <br>
Risk: Automated purchases can exceed owner expectations if merchant, category, or domain constraints are too broad. <br>
Mitigation: Use merchant and domain allowlists, block high-risk categories, check spending permissions before purchases, and keep the default ask-for-everything approval posture unless the owner deliberately changes it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/codejika/replit) <br>
- [CreditClaw skill guide](https://creditclaw.com/skill.md) <br>
- [Encrypted Card guide](https://creditclaw.com/encrypted-card.md) <br>
- [Stripe x402 Wallet guide](https://creditclaw.com/stripe-x402-wallet.md) <br>
- [Management guide](https://creditclaw.com/management.md) <br>
- [Checkout guide](https://creditclaw.com/checkout.md) <br>
- [Heartbeat guide](https://creditclaw.com/heartbeat.md) <br>
- [Skill metadata](https://creditclaw.com/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with curl commands, JSON examples, endpoint tables, and operational guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API calls; registration returns secrets that must be stored securely.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
