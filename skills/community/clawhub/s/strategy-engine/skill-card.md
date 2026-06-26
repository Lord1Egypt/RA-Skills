## Description: <br>
Calls a Strategy Engine MCP server to run quantitative factor-expression strategies, trading backtests, and financial analysis using the MCP server's default parameters. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rxjhfmf](https://clawhub.ai/user/rxjhfmf) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agents use this skill to assemble parameters and invoke Strategy Engine MCP backtests for factor-expression strategies, including period, instrument pool or contract codes, date range, stop-loss, commission, slippage, and result-link reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Strategy parameters may be sent to an external MCP or result-viewing service during backtest execution. <br>
Mitigation: Before each run, confirm the date range, contract or pool, initial cash, commission, slippage, and user intent to send the parameters. <br>
Risk: Incorrect defaults or inferred parameters could produce misleading backtest results. <br>
Mitigation: Review the assembled MCP parameters before execution, especially period, stock pool, time range, stop-loss logic, fees, and slippage. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/rxjhfmf/strategy-engine) <br>
- [Strategy result viewer](https://visual.hzyotoy.com/?data_dir=xzr&data_id=123456789&initCash=10000000) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, configuration, API calls, markdown] <br>
**Output Format:** [Markdown guidance with structured MCP tool-call parameters and result links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Strategy Engine MCP request parameters and a result-viewing link after execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
