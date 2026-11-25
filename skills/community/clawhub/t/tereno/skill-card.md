## Description:

Provides Base smart contract and token risk checks, prediction market evidence review, and cooperative verification tools for agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tereno-xyz](https://clawhub.ai/user/tereno-xyz)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Tereno to review Base token and contract risks before transactions, assess prediction market resolution evidence, and share verification results across agents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it includes an unpinned command that downloads and runs an MCP package and recommends a smart-account hook without explaining its effects; no malicious intent is established.

Mitigation: Before installing, check package version and integrity, review hook permissions and its removal or recovery process, and confirm what market information may be sent to Tereno.

Risk: The security scan was partial: all six listed components were scanned, but several local references could not be resolved, leaving incomplete evidence.

Mitigation: Review unresolved components and treat the scan as incomplete before relying on the skill.

## Reference(s):

- [Tereno service](https://www.tereno.xyz)
- [Tereno MCP endpoint](https://www.tereno.xyz/api/mcp)
- [Capabilities and pricing](references/capabilities-and-pricing.md)
- [Binance Agentic Wallet x402 workflow](references/baw-x402-workflow.md)
- [Cooperative cache and dividends](references/cooperation-economy.md)
- [ERC-8183 escrow and ERC-7579 smart account guards](references/escrow-and-erc7579.md)

## Skill Output:

**Output Type(s):** [Analysis, API Calls, Guidance, JSON]

**Output Format:** [Structured JSON verdicts with supporting evidence and concise agent guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Verdicts may include validity limits, reason codes, evidence, limitations, artifact references, and receipts.]

## Skill Version(s):

1.1.1 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
