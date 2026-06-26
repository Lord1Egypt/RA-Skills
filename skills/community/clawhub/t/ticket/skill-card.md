## Description: <br>
Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to make online purchases through CreditClaw wallets, including ticket-oriented shopping when configured by the owner. The artifact evidence also covers broader shopping, payment-link, and x402 payment workflows beyond the ticket-focused listing name. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The listing is ticket-focused, but the artifacts describe broad real-money shopping, payment-link, and x402 payment authority. <br>
Mitigation: Install only when broad CreditClaw spending authority is intended, keep owner approval required for every purchase, and set low limits plus merchant or category allowlists. <br>
Risk: CREDITCLAW_API_KEY functions as a spending credential. <br>
Mitigation: Store it only in a secure secrets manager or protected environment variable, and never send it outside creditclaw.com API requests. <br>
Risk: Payment-link and x402 workflows can move funds or authorize on-chain settlement. <br>
Mitigation: Review and explicitly enable those workflows only after confirming owner limits, approval thresholds, and domain or merchant rules. <br>
Risk: The skill points agents to remote guide files that may influence payment behavior. <br>
Mitigation: Review remote guide files before allowing an agent to follow them in a spending-enabled environment. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/jononovo/ticket) <br>
- [Publisher profile](https://clawhub.ai/user/jononovo) <br>
- [CreditClaw homepage](https://creditclaw.com) <br>
- [CreditClaw skill guide](https://creditclaw.com/creditcard/skill.md) <br>
- [Pre-paid Wallet guide](https://creditclaw.com/creditcard/prepaid-wallet.md) <br>
- [Self-Hosted Card guide](https://creditclaw.com/creditcard/self-hosted-card.md) <br>
- [Stripe x402 Wallet guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md) <br>
- [Heartbeat guide](https://creditclaw.com/creditcard/heartbeat.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls, Markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and owner-controlled payment guardrails.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 2.3.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
