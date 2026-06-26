## Description: <br>
Browse and rank TRC-20 and TRC-10 tokens on TRON using TronGrid on-chain data, with category filters and holder, activity, supply, and contract signals. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greason](https://clawhub.ai/user/greason) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to discover, compare, and summarize TRON token data from TronGrid. It is useful for producing token overview tables, category-specific token lists, and on-chain activity summaries while noting that price, volume, and market-cap data require a separate market-data source. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Token rankings may be mistaken for price, volume, or market-cap rankings. <br>
Mitigation: Label rankings as on-chain heuristics based on holders, supply, and recent activity, and verify market metrics with a dedicated market-data source before making financial decisions. <br>
Risk: TRC-20 discovery is limited because TronGrid does not provide a complete list-all endpoint for TRC-20 contracts. <br>
Mitigation: Use user-provided contract addresses or the built-in reference list, and state when a requested token is outside the available reference set. <br>
Risk: Invalid, new, or inactive token contracts may return incomplete holder or transaction data. <br>
Mitigation: Skip invalid contracts, note missing data clearly, and avoid treating sparse holder or activity data as a quality guarantee. <br>


## Reference(s): <br>
- [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api) <br>
- [ClawHub skill page](https://clawhub.ai/greason/trongrid-token-list) <br>
- [Publisher profile](https://clawhub.ai/user/greason) <br>
- [Top TRON tokens example](examples/top-tron-tokens.md) <br>
- [DeFi tokens on TRON example](examples/defi-tokens.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, API calls, guidance] <br>
**Output Format:** [Markdown tables and concise explanatory notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses read-only TronGrid lookups; token rankings are based on on-chain heuristics rather than price, volume, or market capitalization.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
