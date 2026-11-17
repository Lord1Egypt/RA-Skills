## Description:

Provides thsdk-based stock-market analysis for minute K-lines, sector and index quotes, multi-stock comparisons, order-book depth, big-order flow, auction anomalies, intraday and historical minute data, Wencai NLP screening, and market news.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bensema](https://clawhub.ai/user/bensema)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to guide agents through THS/同花顺 market-data analysis with thsdk, including short-term price action, sector and index review, batch stock comparison, order-flow checks, auction anomaly review, and Wencai natural-language screening.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing thsdk with --upgrade can pull an unreviewed dependency version.

Mitigation: Install in a virtual environment and pin thsdk to a reviewed version before deployment.

Risk: The skill relies on network calls to THS/Wencai market-data services and produces Chinese/China-market oriented outputs.

Mitigation: Use it only where those external services and market scope are acceptable, and disclose the network dependency to users.

Risk: Market analysis output could be mistaken for investment advice.

Mitigation: Present outputs as informational market data and require human review before any trading or investment decision.

## Reference(s):

- [thsdk on PyPI](https://pypi.org/project/thsdk/)
- [ClawHub skill page](https://clawhub.ai/bensema/skills/ths-advanced-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown responses with Python examples, shell commands, tables, and chart-ready data descriptions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference pandas DataFrames, visualization-ready structures, and thsdk API calls for market-data workflows.]

## Skill Version(s):

1.0.4 (source: evidence.release.version and user changelog)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
