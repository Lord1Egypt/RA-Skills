## Description: <br>
Provides TRON network analytics for transaction volume, type distribution, hot contracts, trending tokens, active accounts, staking metrics, and resource economics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and TRON ecosystem operators use this skill to generate concise network health, trending activity, governance, and resource-economics reports from public TRON blockchain data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on a TronGrid MCP server for public blockchain data. <br>
Mitigation: Verify that the configured TronGrid MCP server is legitimate before use. <br>
Risk: Optional web-searched price data may be third-party, stale, or inconsistent with on-chain observations. <br>
Mitigation: Treat price data as contextual only and confirm important figures against trusted market sources. <br>
Risk: Address labels such as exchange, bot, or whale are classifications rather than verified identities. <br>
Mitigation: Present address classifications as heuristic and avoid relying on them as confirmed identity claims. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>
- [Network overview example](examples/network-overview.md) <br>
- [Trending activity example](examples/trending-activity.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown report with tables, metrics, and key takeaways] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses public TRON blockchain data from the configured TronGrid MCP server; optional web-searched price data should be treated as third-party context.] <br>

## Skill Version(s): <br>
1.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
