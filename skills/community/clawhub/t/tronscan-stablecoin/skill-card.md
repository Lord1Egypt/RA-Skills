## Description:

TronScan Stablecoin helps agents analyze the TRON stablecoin ecosystem across supply, holders, transfers, large transactions, blacklists, liquidity pools, TVL, and key events for USDT, USDC, USDD, and TUSD.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sshnii](https://clawhub.ai/user/sshnii)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query TronScan MCP stablecoin analysis tools for TRON-based USDT, USDC, USDD, and TUSD supply, holder, transfer, blacklist, liquidity, TVL, and major event information.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User questions and query parameters handled through this skill may be sent to the TronScan MCP service.

Mitigation: Avoid sending sensitive wallet research, private addresses, or confidential business context unless that use is approved for the configured TronScan MCP service.

Risk: TronScan API calls may be rate limited when no API key is configured.

Mitigation: Configure an approved TronScan API key when sustained use is needed, and retry failed requests only within acceptable rate limits.

## Reference(s):

- [TronScan MCP Guide](https://mcpdoc.tronscan.org)
- [TronScan MCP Server](https://mcp.tronscan.org/mcp)
- [TronScan Developer API](https://tronscan.org/#/developer/api)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls, configuration]

**Output Format:** [Markdown guidance with tool names, parameters, and usage notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides calls to TronScan MCP stablecoin tools; some tools require token, time range, sorting, or transaction type parameters.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
