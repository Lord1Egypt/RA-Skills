## Description:

Guides agents through validating, estimating, and executing multi-recipient USDC payouts on Base through the Spraay Protocol batch payment gateway.

This skill is ready for commercial/non-commercial use.

## Publisher:

[plagtech](https://clawhub.ai/user/plagtech)

### License/Terms of Use:

MIT-0

## Use Case:

External merchants, commerce operators, and agent developers use this skill to prepare batch payouts for affiliates, creators, suppliers, vendors, referral commissions, and revenue splits. It helps validate recipient data, estimate fees and gas, and execute confirmed USDC payouts through the Spraay gateway.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: On-chain USDC payouts are irreversible after signing and submission.

Mitigation: Validate the batch in-session, show recipient count, total amount, protocol fee, and gas estimate, then require explicit user confirmation before execution.

Risk: Duplicate, malformed, or anomalous recipient entries can misdirect funds or create incorrect payout totals.

Mitigation: Check validation errors, surface warnings, compare totals against the source data, and flag duplicate addresses or disproportionate payments before execution.

Risk: Private-key or seed-phrase handling would create custody and credential exposure risk.

Mitigation: Never request or process private keys or seed phrases; rely on the user's wallet signing flow for non-custodial execution.

## Reference(s):

- [Spraay Protocol](https://spraay.app)
- [Spraay Documentation](https://docs.spraay.app)
- [Batch Payment API 1.0](https://docs.spraay.app/bpa/1.0/)
- [Spraay x402 Gateway Metadata](https://gateway.spraay.app/.well-known/x402.json)
- [Spraay x402 MCP Server](https://smithery.ai/servers/Plagtech/Spraay-x402-mcp)
- [ClawHub Skill Page](https://clawhub.ai/plagtech/skills/shopify-batch-payouts)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with JSON request examples, API endpoint instructions, and transaction-summary links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires user confirmation before irreversible on-chain execution]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
