## Description:

Comprehensive US stock analysis including fundamental analysis, technical analysis, stock comparisons, and investment report generation using Tavily API when available or web search fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[litiao1224](https://clawhub.ai/user/litiao1224)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to gather current US market data and produce stock overviews, fundamental and technical analyses, peer comparisons, and investment-style reports for US tickers. The output is informational analysis and should not be treated as personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Stock ratings, target prices, position sizing, and entry or exit suggestions may be mistaken for personalized financial advice.

Mitigation: Treat outputs as informational analysis only, verify source dates, and consult a qualified financial professional before acting on recommendations.

Risk: Market data and news can become stale quickly, affecting valuation and technical conclusions.

Mitigation: Verify that quoted prices, filings, analyst ratings, and news are current before using the report.

## Reference(s):

- [Financial Metrics Reference](references/financial-metrics.md)
- [Fundamental Analysis Reference](references/fundamental-analysis.md)
- [Stock Analysis Report Template](references/report-template.md)
- [Technical Analysis Reference](references/technical-analysis.md)
- [ClawHub Skill Page](https://clawhub.ai/litiao1224/skills/us-stock-analysis-litiao)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown reports with tables, bullet points, source dates, and optional shell command examples for data gathering]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires current market data retrieval; TAVILY_API_KEY is the preferred environment variable for Tavily-powered searches.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
