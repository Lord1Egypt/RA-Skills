## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent purchase Shopify and other online products through CreditClaw wallets while checking spending permissions, requesting owner approval, and reporting order status. <br>

### Deployment Geography for Use: <br>
Global, subject to merchant, payment-rail, and shipping availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make or request real payments through CreditClaw. <br>
Mitigation: Install only when this capability is intended, keep ask-for-everything or low spending limits until trust is established, and confirm merchant, item, price, and shipping details before purchases. <br>
Risk: Leaking CREDITCLAW_API_KEY could let another party act as the agent and spend owner funds. <br>
Mitigation: Store the API key in a secrets manager and send it only to CreditClaw API endpoints. <br>
Risk: x402 signing and payment-link workflows move money beyond ordinary checkout flows. <br>
Mitigation: Enable x402 or payment-link workflows only after reviewing those capabilities and the associated owner guardrails. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jononovo/shopify-buy) <br>
- [CreditClaw Skill and API Reference](https://creditclaw.com/creditcard/skill.md) <br>
- [Shopping Guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Amazon Shopping Guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md) <br>
- [Skill Metadata](https://creditclaw.com/creditcard/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown documentation with JSON examples and curl command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; real-money actions are mediated by CreditClaw spending limits, approval modes, and payment-rail availability.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
