## Description: <br>
Use Robonet's MCP server to build, backtest, optimize, and deploy trading strategies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nickemmons](https://clawhub.ai/user/nickemmons) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External developers and traders use this skill to explore Robonet market data, generate and refine crypto or prediction-market trading strategies, backtest them, and manage live Hyperliquid deployments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward live trading deployment or restart actions that may affect real funds. <br>
Mitigation: Require separate explicit confirmation before deployment or restart, validate with backtests first, and monitor active deployments so they can be stopped quickly. <br>
Risk: Connected wallets, vaults, API keys, and credit accounts may expose financial loss or spending risk. <br>
Mitigation: Use a dedicated low-balance account where possible, keep conservative leverage and risk limits, and confirm account scope before use. <br>


## Reference(s): <br>
- [Robonet Skill Page](https://clawhub.ai/nickemmons/robonet-workbench) <br>
- [Robonet Dashboard](https://robonet.finance) <br>
- [Jesse Framework Docs](https://jesse.trade) <br>
- [Allora Network](https://allora.network) <br>
- [Hyperliquid](https://hyperliquid.xyz) <br>
- [Robonet MCP Tools Catalog](shared-references/tool-catalog.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with tool calls, strategy code, trading guidance, and configuration details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May result in Robonet MCP API calls that create, backtest, optimize, or deploy trading strategies.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
