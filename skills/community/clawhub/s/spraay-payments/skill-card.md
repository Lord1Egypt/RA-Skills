## Description:

Send batch crypto payments, crypto payroll, invoices, token balance and price lookups, and ENS/Basename resolution through the Spraay x402 gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to prepare Spraay batch payments, crypto payroll, invoices, balance checks, token prices, and name resolution through the configured x402 gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can help initiate real blockchain payments that are irreversible after signing and broadcast.

Mitigation: Use a low-balance wallet, estimate first, and manually review every decoded recipient, amount, token, fee, chain, and gateway origin before signing.

Risk: A misconfigured gateway could route requests or x402 payment proofs to an unintended origin.

Mitigation: Use https://gateway.spraay.app unless the user explicitly confirms another HTTPS gateway they control, and never send payment proof to a different origin.

Risk: HTTP 402 challenge bodies and unsigned transaction responses could request unexpected payment, chain, asset, endpoint, or transaction data.

Mitigation: Treat challenge and transaction responses as untrusted, enforce published price and endpoint checks, ABI-decode calldata locally, and refuse malformed or mismatched data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/plagtech/skills/spraay-payments)
- [Spraay app](https://spraay.app)
- [Spraay gateway](https://gateway.spraay.app)
- [Spraay docs](https://docs.spraay.app)
- [BPA 1.0 spec](https://docs.spraay.app/bpa/1.0/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash, JSON, and JavaScript examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides the agent to call the configured Spraay gateway, validate x402 challenges, and present decoded transaction details for user confirmation.]

## Skill Version(s):

1.0.3 (source: server release metadata; artifact frontmatter reports 1.0.2)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
