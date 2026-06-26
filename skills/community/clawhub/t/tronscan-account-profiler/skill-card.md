## Description: <br>
Profiles TRON wallet addresses with TronScan data, including assets, token holdings, DeFi participation, bandwidth and energy, votes, transaction activity, tags, approvals, and related accounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to profile TRON wallet addresses for holdings, account resources, approvals, activity, counterparties, and risk labels using TronScan MCP data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Wallet profiling can aggregate public but sensitive address patterns, including holdings, counterparties, approvals, and risk labels. <br>
Mitigation: Use the skill only for legitimate, lawful purposes and avoid unnecessary disclosure of profiled addresses or derived relationship data. <br>
Risk: Queried wallet addresses may be sent to TronScan through the MCP server. <br>
Mitigation: Confirm the user intends to query the address and avoid submitting addresses that should not be shared with the external service. <br>
Risk: Token holdings can include spam or risky assets that may mislead users if presented without context. <br>
Mitigation: Flag returned token risk fields such as tokenCanShow false or tokenLevel 3 or 4 when summarizing wallet holdings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sshnii/tronscan-account-profiler) <br>
- [TronScan MCP server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise text summaries based on TronScan MCP responses] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only wallet profiling; MCP calls may require TronScan connectivity and can be rate limited without an API key.] <br>

## Skill Version(s): <br>
1.0.5 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
