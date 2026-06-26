## Description: <br>
Get TRC20 token lists on TRON with price, 24h change, 24h volume, market cap, and holder-count signals for token discovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to query TronScan MCP token-list tools, compare TRC20 tokens by price, change, volume, market cap, and holders, and discover hot or popular TRON tokens. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on an external TronScan MCP endpoint for public TRON token-list lookups. <br>
Mitigation: Confirm the MCP endpoint is the intended TronScan service before use. <br>
Risk: Configuring a TronScan API key for rate limits could expose credentials if pasted into chat. <br>
Mitigation: Store API keys in the MCP configuration and avoid sharing them in conversation. <br>
Risk: Token-list results may include assets marked by TronScan fields as suspicious, unsafe, or not suitable to show. <br>
Mitigation: Flag tokens with tokenCanShow false or tokenLevel 3 or 4 before recommending further analysis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sshnii/tronscan-token-list) <br>
- [TronScan MCP server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, API calls] <br>
**Output Format:** [Markdown text with referenced TronScan MCP tool calls and token metrics] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include pagination, sorting, and token risk flags from TronScan fields when available.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
