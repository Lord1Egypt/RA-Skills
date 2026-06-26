## Description: <br>
Provides agents with CreditClaw payment wallets, encrypted-card checkout, spending controls, and payment-request workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jononovo](https://clawhub.ai/user/jononovo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to let an agent make owner-authorized purchases, request funds, manage wallet status, and create payment links or checkout pages under spending controls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can authorize real-money purchases and payment requests. <br>
Mitigation: Install only for intended real-money commerce use, keep per-purchase approval enabled at first, and review wallet activity and limits before allowing broader autonomy. <br>
Risk: Leaked CREDITCLAW_API_KEY or webhook secrets can expose spending authority. <br>
Mitigation: Store credentials in a secrets manager and send the API key only to creditclaw.com API endpoints. <br>
Risk: Encrypted-card workflows can expose payment-card material if run in the main agent context or stored carelessly. <br>
Mitigation: Use the ephemeral sub-agent checkout flow, never log decrypted card data, and keep encrypted card files out of shared or synced folders. <br>
Risk: Companion payment-rail documentation may be fetched remotely before use. <br>
Mitigation: Review any remotely fetched Stripe x402 companion file before executing its guidance. <br>


## Reference(s): <br>
- [ClawHub Release Page](https://clawhub.ai/jononovo/venmo) <br>
- [CreditClaw Shopping Skill](https://creditclaw.com/shopping/skill.md) <br>
- [Encrypted Card Guide](https://creditclaw.com/shopping/encrypted-card.md) <br>
- [Spending Permissions Guide](https://creditclaw.com/shopping/spending.md) <br>
- [Checkout and Payment Links Guide](https://creditclaw.com/shopping/checkout.md) <br>
- [Management Guide](https://creditclaw.com/shopping/management.md) <br>
- [Machine-Readable Skill Metadata](https://creditclaw.com/shopping/skill.json) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with curl commands, JSON examples, and operating instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY and may involve webhook secrets, approval polling, and encrypted card files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
