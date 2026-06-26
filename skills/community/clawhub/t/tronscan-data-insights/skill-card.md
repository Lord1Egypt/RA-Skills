## Description: <br>
TRON network insights for new accounts, daily transaction counts, transaction type distribution, hot tokens, hot contracts, and top accounts by transaction count or staked TRX. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and external users use this skill to route TRON network analytics questions to TronScan MCP tools for activity trends, rankings, hot tokens or contracts, TVL, resource usage, and other public chain metrics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Address lookup requests may be sent to the TronScan MCP provider. <br>
Mitigation: Use address lookup only when the user intentionally asks for cross-chain address information. <br>
Risk: Daily new-account data can be mistaken for daily active users. <br>
Mitigation: Use getActiveStatistic for active account metrics and label getDailyNewAccounts as daily new addresses only. <br>
Risk: TronScan API or MCP rate limits may interrupt analysis. <br>
Mitigation: Retry with narrower time ranges or configure a TronScan API key when rate limits are encountered. <br>


## Reference(s): <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sshnii/tronscan-data-insights) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, API Calls, Analysis] <br>
**Output Format:** [Markdown guidance with selected TronScan MCP tool calls and summarized analytics results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only public TRON analytics; results depend on TronScan MCP availability, rate limits, and requested time ranges.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
