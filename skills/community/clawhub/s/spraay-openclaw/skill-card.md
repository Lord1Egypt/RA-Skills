## Description:

Guides agents using the Spraay gateway for Base payments, DeFi quotes and prices, AI inference, and blockchain data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use this skill to prepare and review Base payments, retrieve DeFi and chain data, and request AI inference through the Spraay gateway. Users review and sign any payment transactions themselves.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Payments and payroll can move real funds irreversibly.

Mitigation: Use a low-balance wallet; confirm recipients, amounts, fees, and decoded transactions before the user signs.

Risk: Payment challenges or a changed gateway could redirect funds or incur unexpected charges.

Mitigation: Use the official HTTPS gateway unless the user confirms another one; validate each x402 challenge, price, and destination before one payment attempt.

Risk: Wallet addresses, payroll and invoice details, or AI prompts may be shared with the configured gateway.

Mitigation: Send only required details and keep secrets out of AI prompts.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/plagtech/skills/spraay-openclaw)
- [Spraay documentation](https://docs.spraay.app)
- [BPA 1.0 specification](https://docs.spraay.app/bpa/1.0/)
- [Gateway endpoint catalog](https://gateway.spraay.app/.well-known/x402.json)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with bash and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include gateway JSON and unsigned transaction details for user review.]

## Skill Version(s):

1.0.2 (source: skill frontmatter and server-resolved release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
