## Description: <br>
Validates historical behavior of stock ranking, factor, and portfolio-selection strategies using reproducible backtests, benchmark comparison, turnover, drawdown, and bias warnings. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ndtchan](https://clawhub.ai/user/ndtchan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Investors, analysts, and agent developers use this skill to evaluate stock ranking, factor, or portfolio-selection rules against local historical signal and price CSVs before treating them as investment inputs. It helps summarize backtest setup, performance, benchmark comparison, robustness warnings, confidence, and data gaps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backtest results may be mistaken for forecasts or investment advice. <br>
Mitigation: State that outputs are historical simulations, not trading commands, and review them as one input among broader investment analysis. <br>
Risk: Incomplete CSV data, missing benchmarks, or non-point-in-time universe data can bias results. <br>
Mitigation: Require explicit data coverage, benchmark, fee, slippage, and point-in-time assumptions; downgrade confidence when these inputs are missing. <br>
Risk: Benchmark comparison and bias warnings are not fully automated by the included script. <br>
Mitigation: Manually verify benchmark comparisons and robustness warnings before relying on the report. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ndtchan/strategy-backtester) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Files, Guidance] <br>
**Output Format:** [Markdown report with a JSON handoff bundle; local scripts can also produce JSON and CSV files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local signal and price CSV inputs; no network access is required by the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
