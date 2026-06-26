## Description: <br>
Quantflow Skill turns Chinese natural-language financial research requests into executable workflows for data retrieval, cleaning, comparison, screening, export, brief analysis, and AKQuant-based backtesting across A-shares, indexes, ETFs/funds, financials, valuation, flows, news, sectors, themes, and macro data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yejinlei](https://clawhub.ai/user/yejinlei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, analysts, and developers use this skill to map Chinese financial-data questions into Akshare and AKQuant workflows for market data, fundamentals, fund flows, macro data, exports, and backtesting-oriented research outputs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses akshare and akquant to make network requests to financial data providers. <br>
Mitigation: Run it only in environments where those outbound data requests are approved and expected. <br>
Risk: The skill may write local research exports or cache files such as CSV or Parquet datasets. <br>
Mitigation: Review output paths and local storage handling before using it with sensitive research data. <br>
Risk: Backtest and financial-analysis outputs can be mistaken for live trading advice. <br>
Mitigation: Treat all results as research output and require human review before any investment or trading decision. <br>


## Reference(s): <br>
- [Akshare data interface reference](references/数据接口.md) <br>
- [Quantflow Skill ClawHub page](https://clawhub.ai/yejinlei/quantflow-skill) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown summaries, tables, Python snippets, shell commands, and local CSV or Parquet export paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include data scope, source interface names, request parameters, row counts, failed segments, and limitations when data is incomplete.] <br>

## Skill Version(s): <br>
1.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
