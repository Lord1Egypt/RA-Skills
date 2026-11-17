## Description:

Query Radix DLT blockchain data including wallet balances and performance, token prices and market movers, validator staking info, transaction history, network statistics, ecosystem news, DeFi yield pools, XRD trading venues, dApp directory, and developer resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mavremu](https://clawhub.ai/user/mavremu)

### License/Terms of Use:


## Use Case:

External users, developers, and analysts use this skill to query Radix mainnet wallet, token, staking, DeFi, ecosystem, and developer-resource data through the Emily remote MCP service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing the mcporter npm CLI and registering a remote MCP service expands the local and remote execution surface.

Mitigation: Install only if comfortable with the mcporter dependency, review the package before use, and register the Emily service URL exactly as documented.

Risk: Radix wallet addresses and related queries are sent to the Emily remote MCP service.

Mitigation: Use public addresses or non-sensitive queries only, and do not provide seed phrases, private keys, credentials, or signed transactions.

Risk: Blockchain, market, staking, and yield data may be cached, rate limited, or unsuitable as the sole basis for high-impact financial decisions.

Mitigation: Verify important financial or staking decisions against authoritative sources and account for the documented freshness and rate-limit constraints.

## Reference(s):

- [Radix Explorer on ClawHub](https://clawhub.ai/mavremu/skills/radix-explorer)
- [Emily Remote MCP Service](https://www.ineedemily.com/api/mcp/mcp)
- [Emily](https://www.ineedemily.com)
- [Radix Gateway API Documentation](https://docs.radixdlt.com/docs/network-apis)
- [Astrolescent](https://astrolescent.com)
- [CoinMarketCap](https://coinmarketcap.com)
- [Attos Earn](https://earn.attos.world)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and MCP tool-call guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote MCP responses reflect upstream Radix, market, and ecosystem data freshness and rate limits.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
