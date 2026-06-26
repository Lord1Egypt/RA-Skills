## Description: <br>
Query Radix DLT blockchain data including wallet balances and performance, token prices and market movers, validator staking info, transaction history, network statistics, ecosystem news, DeFi yield pools, XRD trading venues, dApp directory, and developer resources. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[MAvRemu](https://clawhub.ai/user/MAvRemu) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this skill to query Radix mainnet wallet, token, staking, DeFi, ecosystem, news, and developer-resource data through Emily's Radix assistant service. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Radix wallet addresses, token addresses, RNS domains, and lookup queries may be sent to the Emily remote MCP service. <br>
Mitigation: Avoid querying wallets, portfolios, or domains you consider sensitive unless you are comfortable sharing those lookups with that service. <br>
Risk: The skill depends on adding the mcporter npm CLI and registering a remote endpoint. <br>
Mitigation: Install only in environments where adding the mcporter CLI and remote MCP configuration is acceptable. <br>


## Reference(s): <br>
- [Radix Explorer on ClawHub](https://clawhub.ai/MAvRemu/radix-explorer) <br>
- [Emily Radix Assistant](https://www.ineedemily.com) <br>
- [Emily MCP Endpoint](https://www.ineedemily.com/api/mcp/mcp) <br>
- [Radix Gateway API Documentation](https://docs.radixdlt.com/docs/network-apis) <br>
- [Astrolescent](https://astrolescent.com) <br>
- [CoinMarketCap](https://coinmarketcap.com) <br>
- [Attos Earn](https://earn.attos.world) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and MCP tool-call guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the mcporter CLI and uses a remote read-oriented Radix data service.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
