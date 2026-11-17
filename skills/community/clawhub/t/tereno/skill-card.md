## Description:

This skill helps agents assess Base smart contracts and prediction markets before acting, share verification results, and use cooperative bounties and dividends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tereno-xyz](https://clawhub.ai/user/tereno-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and autonomous agents use the skill to check Base tokens, contracts, and prediction market rules before transactions, trades, or escrow decisions, and to share verifiable assessment results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Running an unpinned npm package with automatic confirmation can execute local code; the scan did not establish malicious behavior and was partial.

Mitigation: Review the package and its source, use a specific audited version, keep wallet secrets and other sensitive credentials out of the process, and confirm payment requirements before signing.

## Reference(s):

- [Tereno website](https://www.tereno.xyz)
- [Tereno MCP endpoint](https://www.tereno.xyz/api/mcp)
- [Capabilities, endpoints and MCP tools](artifact/references/capabilities-and-pricing.md)
- [Binance Agentic Wallet x402 workflow](artifact/references/baw-x402-workflow.md)
- [Cooperative cache, bounties and dividends](artifact/references/cooperation-economy.md)
- [ERC-8183 escrow and ERC-7579 smart account guards](artifact/references/escrow-and-erc7579.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, JSON, Shell commands, Guidance]

**Output Format:** [Structured JSON verdicts and evidence, with Markdown guidance and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts include reason codes, evidence, limitations, and freshness information; assessments are advisory and can require human review.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
