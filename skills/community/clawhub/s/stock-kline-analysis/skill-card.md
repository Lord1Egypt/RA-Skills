## Description: <br>
Given a stock name or code, auto-detect its market, fetch 6-month daily K-line, plot candlestick + MA/Bollinger/MACD/RSI/ATR with multi-timeframe confirmation, and deliver structured analysis with trend, momentum, valuation context, portfolio-relative strength, and event-aware risk notes. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iideas18](https://clawhub.ai/user/iideas18) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and analysts use this skill to run stock K-line analysis from a stock name or code, including market detection, technical indicators, chart generation, valuation context, relative-strength comparison, and event-aware risk notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Market-data requests may send stock symbols or company names to external services. <br>
Mitigation: Use the skill only in a trusted Python environment and avoid submitting confidential watchlists or private identifiers. <br>
Risk: Generated technical and valuation analysis could be mistaken for investment advice. <br>
Mitigation: Treat outputs as informational analysis and review conclusions before making trading or portfolio decisions. <br>
Risk: Chart and report generation writes files locally. <br>
Mitigation: Choose an appropriate output directory and review generated files before sharing or reusing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iideas18/stock-kline-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/iideas18) <br>


## Skill Output: <br>
**Output Type(s):** [analysis, markdown, code, shell commands, files, guidance] <br>
**Output Format:** [Markdown analysis with optional shell commands and locally generated chart/report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May query external market-data services through AkShare and may write chart or report files to a local output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
