## Description:

Strategy Engine helps agents assemble and run quantitative strategy backtests through an MCP server using documented defaults for dates, periods, instruments, fees, slippage, and stop-loss conditions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rxjhfmf](https://clawhub.ai/user/rxjhfmf)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and traders use this skill when an agent needs to translate strategy conditions into a Strategy Engine MCP request, run factor-expression backtests, and return a report link for reviewing results.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Ambiguous financial-analysis requests may cause an agent to run a remote strategy backtest when the user's intent is not explicit.

Mitigation: Confirm that the user wants a backtest run before invoking the MCP server, especially for broad financial-analysis requests.

Risk: Default assumptions for dates, commission, slippage, capital, and instrument pools can materially affect backtest results.

Mitigation: Review and restate the selected defaults before execution, and ask the user to supply any missing values that change the analysis.

Risk: The artifact contains stale or inconsistent examples for some defaults and dates.

Mitigation: Prefer server/tool defaults when available and verify generated dates and parameter values before submitting the MCP request.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/rxjhfmf/skills/strategy-engine)
- [Strategy analysis report viewer](https://visual.hzyotoy.com/?data_dir=xzr&data_id=123456789&initCash=10000000)

## Skill Output:

**Output Type(s):** [Text, Markdown, API calls, Configuration, Guidance]

**Output Format:** [Markdown with parameterized MCP tool calls and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include generated run identifiers, defaulted backtest parameters, and external strategy-analysis report links.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
