## Description:

Let your agent shop online with guardrailed wallets, multiple payment methods, and owner approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let agents purchase Shopify products and other online goods through CreditClaw wallets while applying owner-set spending limits, approvals, and order-status checks.

### Deployment Geography for Use:

United States for physical shipping flows; Global for non-shipping payment flows where the selected merchant and payment rail support them.

## Known Risks and Mitigations:

Risk: The skill gives an agent authority to initiate real purchases and payment flows.

Mitigation: Install only when that authority is intended; keep ask-for-everything approval enabled, set low spending limits, and restrict merchants, categories, and domains.

Risk: CREDITCLAW_API_KEY functions as a spending credential.

Mitigation: Store it in a secrets manager or protected environment variable and use it only with CreditClaw endpoints.

Risk: Payment-link and x402 flows can move funds through additional payment mechanisms.

Mitigation: Review those flows separately before enabling them, especially where the x402 rail is marked private beta.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/shopify-buy)
- [CreditClaw Skill Reference](https://creditclaw.com/creditcard/skill.md)
- [CreditClaw Shopping Guide](https://creditclaw.com/creditcard/shopping.md)
- [CreditClaw Pre-paid Wallet Guide](https://creditclaw.com/creditcard/prepaid-wallet.md)
- [CreditClaw Self-Hosted Card Guide](https://creditclaw.com/creditcard/self-hosted-card.md)
- [CreditClaw Stripe x402 Wallet Guide](https://creditclaw.com/creditcard/stripe-x402-wallet.md)
- [CreditClaw Heartbeat Guide](https://creditclaw.com/creditcard/heartbeat.md)
- [CreditClaw Machine-Readable Skill Metadata](https://creditclaw.com/creditcard/skill.json)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration, API calls]

**Output Format:** [Markdown guidance with JSON examples and bash curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires CREDITCLAW_API_KEY; outputs purchase, wallet, approval, and status-check request patterns.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 2.3.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
