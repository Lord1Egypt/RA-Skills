## Description: <br>
Lets an agent shop online through CreditClaw wallets, payment rails, and owner approval controls. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TripleHippo](https://clawhub.ai/user/TripleHippo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent request purchases, check spending permissions, poll wallet or order status, and route payments through CreditClaw payment methods under owner-set guardrails. <br>

### Deployment Geography for Use: <br>
Global; Amazon and pre-paid wallet shipping flows documented in the artifact require US addresses. <br>

## Known Risks and Mitigations: <br>
Risk: The release label suggests Samsung shopping, but the security evidence says the artifact grants broad CreditClaw spending, payment-signing, and payment-link authority. <br>
Mitigation: Install only when broad CreditClaw payment capability is intended; review the full payment scope with the user before enabling the skill. <br>
Risk: The skill can initiate real-money purchase and payment workflows using CREDITCLAW_API_KEY. <br>
Mitigation: Use a dedicated API key, keep auto-approval disabled or tightly capped, and set strict merchant, category, domain, per-transaction, daily, and monthly limits. <br>
Risk: Payment links and x402 signing expand the skill beyond ordinary shopping flows. <br>
Mitigation: Do not enable payment links or x402 signing unless those capabilities are explicitly required for the deployment. <br>
Risk: Payment API keys, payment headers, and shipping details are sensitive. <br>
Mitigation: Store credentials in a secrets manager and avoid logging API keys, shipping addresses, or payment authorization headers. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/TripleHippo/samsung) <br>
- [CreditClaw Skill Entry Point](https://creditclaw.com/creditcard/skill.md) <br>
- [CreditClaw API Base](https://creditclaw.com/api/v1) <br>
- [General Shopping Guide](https://creditclaw.com/creditcard/shopping.md) <br>
- [Amazon Shopping Guide](https://creditclaw.com/creditcard/amazon.md) <br>
- [Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with curl examples and JSON request and response snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata; bundled skill metadata reports CreditClaw version 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
