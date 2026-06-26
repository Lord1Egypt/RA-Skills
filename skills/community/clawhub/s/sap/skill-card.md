## Description: <br>
The published artifact describes CreditClaw-powered Amazon shopping for agents using guardrailed wallets, owner approval, and order tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent register with CreditClaw, check spending permissions, request purchases, collect payments, and manage payment rails under owner-defined approval rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Real-money purchasing, selling, and wallet actions can move funds or charge payment instruments. <br>
Mitigation: Use the strictest approval mode, avoid broad auto-approval rules, and review each transaction before allowing funds to move. <br>
Risk: A leaked CREDITCLAW_API_KEY could allow unauthorized spending or collection activity. <br>
Mitigation: Store the API key in a secrets manager and only send it to CreditClaw API endpoints. <br>
Risk: Downloaded card or decrypt artifacts, webhook payloads, buyer PII, and transaction logs may expose sensitive data. <br>
Mitigation: Review or sandbox artifacts before execution and confirm retention and deletion behavior for local files, payloads, PII, and logs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jononovo/sap) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw Amazon skill](https://creditclaw.com/amazon/skill.md) <br>
- [CreditClaw Amazon skill metadata](https://creditclaw.com/amazon/skill.json) <br>
- [Checkout guide](https://creditclaw.com/amazon/checkout.md) <br>
- [Encrypted card guide](https://creditclaw.com/amazon/encrypted-card.md) <br>
- [Spending permissions guide](https://creditclaw.com/amazon/spending.md) <br>
- [Wallet management guide](https://creditclaw.com/amazon/management.md) <br>
- [Stripe x402 wallet guide](https://creditclaw.com/amazon/stripe-x402-wallet.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration, API calls] <br>
**Output Format:** [Markdown with curl examples, JSON request and response examples, and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY for authenticated CreditClaw API requests.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata); artifact metadata reports 2.3.0 <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
