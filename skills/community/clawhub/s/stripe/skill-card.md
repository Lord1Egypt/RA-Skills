## Description: <br>
With CreditClaw and backed by Stripe, this skill helps an agent use a CreditClaw wallet to request payment approvals, complete guarded purchases, manage wallet activity, and use private-beta Stripe/x402 wallet flows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent operate a CreditClaw financial account under owner controls: registering a wallet, checking balances and limits, requesting purchase approval, completing merchant checkout, creating payment links or checkout pages, and using Stripe/x402 wallet signing when available. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security verdict is suspicious because the skill can let an agent operate a financial account, decrypt card data during checkout, and complete purchases across merchants. <br>
Mitigation: Install only when this financial authority is intended; keep ask-for-everything approval enabled, set strict spending and domain limits, and review each final merchant and order total before card entry or submission. <br>
Risk: CREDITCLAW_API_KEY exposure could allow another party to act as the wallet-linked agent. <br>
Mitigation: Store the API key only in a secure secrets manager or environment variable, and send it only to creditclaw.com API endpoints. <br>
Risk: Webhook callbacks can influence approval and spending workflows if accepted without verification. <br>
Mitigation: Use callback URLs only on domains you control, verify CreditClaw webhook signatures with the webhook secret, and reject invalid or unexpected webhook messages. <br>
Risk: Decrypted card data is sensitive and should not persist beyond a checkout session. <br>
Mitigation: Use the documented ephemeral checkout flow, avoid logging or storing decrypted card details, and discard card data immediately after confirmation or failure. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/jononovo/stripe) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw API base](https://creditclaw.com/api/v1) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [CHECKOUT-GUIDE.md](artifact/CHECKOUT-GUIDE.md) <br>
- [STRIPE-X402-WALLET.md](artifact/STRIPE-X402-WALLET.md) <br>
- [WEBHOOK.md](artifact/WEBHOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, API calls, Configuration] <br>
**Output Format:** [Markdown guidance with inline bash commands, JSON request and response examples, and checkout procedures] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and user-confirmed invocation; normal operation may involve payment approval, encrypted card handling, webhook setup, and platform-specific checkout guides.] <br>

## Skill Version(s): <br>
2.9.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
