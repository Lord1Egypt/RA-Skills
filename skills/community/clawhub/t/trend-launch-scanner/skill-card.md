## Description: <br>
趋势启动扫描器 is a trend-following stock screening skill that scores Chinese A-share candidates using technical indicators, confirmation signals, industry dispersion, sentiment checks, tracking, and backtest helpers. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[jayden-zhong](https://clawhub.ai/user/jayden-zhong) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and agent operators use this skill to run a local market-data scanner that ranks potential early trend stocks and records follow-up tracking information. It is suitable for research and validation workflows, not as standalone investment advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Helper scripts can overwrite generated stock-pool Python files from network-fetched market data. <br>
Mitigation: Review those scripts before use, change hard-coded output paths, and run them only in an isolated workspace where overwrites are acceptable. <br>
Risk: The skill creates or updates local market-data, tracking, weight, and backtest files under configured .qclaw paths. <br>
Mitigation: Run the scanner only after confirming the local data location and permissions match the intended environment. <br>
Risk: Some helper scripts depend on hard-coded local import paths and non-HTTPS market-data endpoints. <br>
Mitigation: Update local paths and prefer HTTPS data sources before running fetch or rebuild helpers. <br>
Risk: Backtest and scoring results may be misleading if treated as investment advice. <br>
Mitigation: Independently validate thresholds, holding-period logic, and data quality before relying on the outputs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jayden-zhong/trend-launch-scanner) <br>
- [Publisher profile](https://clawhub.ai/user/jayden-zhong) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and console-style text with Python command examples and generated local data files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Scanner output depends on live market-data requests and locally persisted tracking, weights, and backtest data.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
