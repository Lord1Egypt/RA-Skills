## Description:

Parse and summarize backtest results from D:/Stock/ -- win rate, Sharpe, drawdown, returns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eohmig](https://clawhub.ai/user/eohmig)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and trading researchers use this skill to inspect local trading backtest JSON files and summarize performance metrics in a readable report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local trading backtest files from D:/Stock/, which may contain sensitive strategy or performance data.

Mitigation: Install and run it only in environments where the agent is permitted to read D:/Stock/backtest_results*.json.

Risk: Backtest JSON schemas or metric names may differ, which can lead to incomplete summaries.

Mitigation: Have the agent note missing metrics and schema gaps instead of filling unsupported values.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown summary table with concise notes about missing metrics or schema gaps.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Read-only analysis of D:/Stock/backtest_results.json and D:/Stock/backtest_results_full.json when present.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
