## Description: <br>
Searches the TRON blockchain by name or keyword to resolve token or contract names to addresses and find accounts, transactions, or blocks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to search TronScan for TRON tokens, contracts, accounts, transactions, and blocks when they have a name, symbol, keyword, transaction hash, or block identifier. It is especially useful for resolving token or contract addresses before using deeper TronScan analysis skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search terms and blockchain identifiers are sent to the TronScan MCP/API service. <br>
Mitigation: Use the skill only when sharing those lookup values with TronScan is acceptable. <br>
Risk: An optional TronScan API key may be needed if unauthenticated requests are rate limited. <br>
Mitigation: Store any API key only in trusted MCP configuration and avoid exposing it in prompts or shared logs. <br>
Risk: Search results may include tokens where tokenCanShow is false. <br>
Mitigation: Treat tokenCanShow: false as a risk signal and inform the user before relying on or proceeding with that token. <br>


## Reference(s): <br>
- [TronScan Search ClawHub page](https://clawhub.ai/sshnii/tronscan-search) <br>
- [TronScan MCP server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Text, Guidance] <br>
**Output Format:** [Markdown or plain text summarizing TronScan search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include token IDs, contract addresses, account matches, transaction or block matches, and cautionary notes for tokenCanShow risk signals.] <br>

## Skill Version(s): <br>
1.0.3 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
