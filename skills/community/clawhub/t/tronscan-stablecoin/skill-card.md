## Description: <br>
Analyze the TRON stablecoin ecosystem across supply, holders, transfers, large transactions, blacklist status, liquidity pools, TVL, and key events for USDT, USDC, USDD, and TUSD. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sshnii](https://clawhub.ai/user/sshnii) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to route TRON stablecoin research requests to the appropriate TronScan MCP tools for supply, holder, transfer, blacklist, pool, TVL, and event analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stablecoin research prompts and blockchain addresses may be sent to TronScan's MCP service. <br>
Mitigation: Avoid including private notes or unnecessary sensitive context in prompts. <br>
Risk: API key setup for rate-limit handling could target the wrong endpoint if configuration is not checked. <br>
Mitigation: Verify the TronScan MCP endpoint before adding any API key. <br>


## Reference(s): <br>
- [TronScan MCP Guide](https://mcpdoc.tronscan.org) <br>
- [TronScan MCP Server](https://mcp.tronscan.org/mcp) <br>
- [TronScan Developer API](https://tronscan.org/#/developer/api) <br>
- [ClawHub Skill Page](https://clawhub.ai/sshnii/tronscan-stablecoin) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/sshnii) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, API Calls, configuration] <br>
**Output Format:** [Markdown guidance with tool names, parameters, and troubleshooting notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Read-only guidance for using TronScan MCP stablecoin analytics; some tools require time ranges, token addresses, pool addresses, or transaction type filters.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
