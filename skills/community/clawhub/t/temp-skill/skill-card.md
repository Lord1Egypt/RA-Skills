## Description: <br>
Provides local multi-asset portfolio analysis with CSV-based backtesting, rolling-window risk-parity rebalancing, performance metrics, and report/chart generation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wzratgit](https://clawhub.ai/user/wzratgit) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, analysts, and agent workflows use this skill to run local portfolio backtests from intended CSV market data, inspect risk-parity allocations, and generate informational performance reports and charts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the skill on unintended local CSV files may expose or process data the user did not mean to analyze. <br>
Mitigation: Run it only on CSV files selected for this analysis and review generated reports before sharing them. <br>
Risk: Generated report or chart filenames may replace existing files in the chosen output directory. <br>
Mitigation: Point the output option to a dedicated folder for each run. <br>
Risk: Reports and JSON outputs may include local file paths, timestamps, asset data, and analysis results. <br>
Mitigation: Inspect generated artifacts and remove sensitive details before distribution. <br>
Risk: Backtest and risk metrics can be mistaken for financial advice. <br>
Mitigation: Treat the output as informational analysis and have qualified reviewers assess investment decisions. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/wzratgit/temp-skill) <br>
- [README](artifact/README.md) <br>
- [Skill documentation](artifact/SKILL.md) <br>
- [Usage guide](artifact/优化使用指南.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, files, shell commands, guidance] <br>
**Output Format:** [Console summaries plus text reports, JSON data, and PNG chart files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and charts to a user-selected output directory; outputs may include local file paths, timestamps, asset data, and financial analysis results.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact manifest) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
