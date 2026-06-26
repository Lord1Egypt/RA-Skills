## Description: <br>
Analyzes pairs-trading statistical arbitrage requests by running local Python backtests for selected stock pairs and summarizing cointegration, hedge ratio, Z-score signals, and performance outputs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[loi214](https://clawhub.ai/user/loi214) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to evaluate stock-pair statistical arbitrage ideas across supported markets. It helps an agent prepare and run a local backtest, then report cointegration status, hedge ratio, current signal, performance metrics, and generated report files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The executable analysis script is obfuscated and may not match the documented configurable CLI behavior. <br>
Mitigation: Review or replace the script before use, and confirm that requested tickers, dates, thresholds, capital, and output path are actually honored. <br>
Risk: The skill installs Python dependencies and downloads market data during analysis. <br>
Mitigation: Run it in an isolated Python environment with network access controls appropriate for the deployment, and verify dependency sources before installing. <br>
Risk: Backtest results and trading signals can be misleading or unsuitable for live trading. <br>
Mitigation: Treat results as informational only, validate data quality and assumptions independently, and require qualified human review before any investment decision. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/loi214/statistical-arbitrage) <br>
- [Publisher profile](https://clawhub.ai/user/loi214) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, files] <br>
**Output Format:** [Markdown narrative with inline shell commands and references to generated PNG, HTML, and CSV files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are informational finance analysis and backtest artifacts; results depend on market data availability and script behavior.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
