## Description: <br>
Generates structured Markdown deep-analysis reports for US, Hong Kong, and A-share stocks by fetching financial statements, valuation data, price data, and optional position-cost information from Yahoo Finance and Tushare. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[heiheiheibj](https://clawhub.ai/user/heiheiheibj) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and investors use this skill to generate Markdown stock-analysis reports for supported US, Hong Kong, and China market tickers. The reports summarize company profile, valuation, profitability, balance sheet quality, growth, cash flow, position status, and recommendations based on fetched market and financial data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review flags hard-coded proxy defaults that may route market-data traffic unexpectedly. <br>
Mitigation: Review or remove the proxy defaults before installation, and set proxy environment variables only when that routing is intended. <br>
Risk: The skill fetches market data from Yahoo Finance and Tushare, and A-share analysis may require a Tushare token. <br>
Mitigation: Provide TUSHARE_TOKEN only when China market analysis is needed, and avoid using the skill for unrelated financial conversations. <br>
Risk: Generated stock reports can contain stale or rate-limited market data and should not be treated as investment advice. <br>
Mitigation: Review the generated report against current source data and apply independent financial judgment before relying on it. <br>


## Reference(s): <br>
- [Financial Indicators Guide](references/indicators-guide.md) <br>
- [ClawHub Release Page](https://clawhub.ai/heiheiheibj/skill-stock-deep-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Analysis, Shell commands, Code, Guidance] <br>
**Output Format:** [Markdown report text printed by a Python CLI or returned by a Python function] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a ticker and market selection; optional position cost and currency parameters affect the generated report.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
