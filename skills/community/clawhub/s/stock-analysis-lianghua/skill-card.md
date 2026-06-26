## Description: <br>
Analyzes stock technical indicators and trends with a standalone Python script, and provides a reference template for modifying TradingAgentsV2 analyst nodes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[llq20133100095](https://clawhub.ai/user/llq20133100095) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to run stock ticker technical analysis, inspect indicator trends, and adapt TradingAgentsV2 analyst-node patterns for market reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Python script contacts public finance data providers and writes local CSV cache files. <br>
Mitigation: Run it only in environments where outbound requests to finance data providers and local cache-file creation are acceptable. <br>
Risk: Ticker symbols are used in cache filenames and data-provider requests. <br>
Mitigation: Use normal stock ticker symbols and avoid untrusted or path-like ticker strings. <br>
Risk: TradingAgentsV2 analyst-node changes can alter downstream market-analysis behavior. <br>
Mitigation: Review and test any TradingAgentsV2 code changes before applying them. <br>


## Reference(s): <br>
- [Technical Indicator Reference](artifact/indicators-reference.md) <br>
- [ClawHub skill page](https://clawhub.ai/llq20133100095/stock-analysis-lianghua) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; the analysis script prints plain-text market reports and summary tables.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces stock technical-analysis reports from ticker, date, lookback window, and selected indicator inputs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
