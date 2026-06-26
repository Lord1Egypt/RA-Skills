## Description: <br>
Provides THS/thsdk-based stock-market analysis workflows for minute K-lines, sector and index quotes, multi-stock comparisons, order-book depth, large-order flow, auction anomalies, intraday data, historical intraday data, Wencai natural-language screening, and market news. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[bensema](https://clawhub.ai/user/bensema) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to retrieve and analyze stock-market data through thsdk, including short-term trading views, sector and index analysis, batch stock comparison, and Wencai natural-language screening. It guides agents toward structured market summaries, tables, chart-ready data, and Python examples rather than acting as a trading execution system. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill depends on the third-party thsdk package and THS/Wencai market-data provider. <br>
Mitigation: Install only when those dependencies are trusted, preferably in a virtual environment with pinned package versions. <br>
Risk: Natural-language screening queries may disclose private watchlists, trading strategies, or personal financial details to the data provider. <br>
Mitigation: Avoid submitting confidential strategies, private watchlists, or personal financial information in Wencai or other provider-backed queries. <br>
Risk: Market-data outputs can be incomplete, stale, or unsuitable for financial decisions without review. <br>
Mitigation: Treat generated analysis as decision support and verify important quotes, signals, and assumptions against authoritative market sources before use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/bensema/ths-advanced-analysis) <br>
- [thsdk on PyPI](https://pypi.org/project/thsdk/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown analysis with tables, Python snippets, shell installation commands, and chart-ready data guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include tabular market summaries, normalized trend comparisons, correlation heatmap guidance, and THS/Wencai query examples.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
