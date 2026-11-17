## Description:

Generates structured Markdown financial analysis reports for US, Hong Kong, and China A-share stocks by fetching financial statements, valuation, price, and position data from Yahoo Finance and Tushare.

This skill is ready for commercial/non-commercial use.

## Publisher:

[heiheiheibj](https://clawhub.ai/user/heiheiheibj)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and analysts use this skill to generate stock deep-dive reports for US, Hong Kong, and China A-share tickers, optionally including position-cost context for profit and loss calculations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can silently route external market-data traffic through an undocumented hard-coded proxy.

Mitigation: Remove the proxy default or explicitly configure trusted proxy settings before running the skill.

Risk: Ticker requests, Tushare token use, and optional position-cost inputs may expose sensitive portfolio context to external services.

Mitigation: Use a skill-specific environment, protect the Tushare token, and avoid entering sensitive portfolio details unless the external data-sharing risk is acceptable.

Risk: Generated financial reports can contain stale, incomplete, or provider-delayed market and financial data.

Mitigation: Cross-check outputs against authoritative filings or market-data sources before making investment decisions.

## Reference(s):

- [Financial Indicators Guide](artifact/references/indicators-guide.md)
- [ClawHub Skill Page](https://clawhub.ai/heiheiheibj/skills/skill-stock-deep-analysis)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, code, guidance]

**Output Format:** [Markdown report with tables and narrative analysis; CLI usage and Python API examples are documented.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may include fetched market data, financial metrics, valuation indicators, position cost, profit and loss calculations, and investment-risk disclaimers.]

## Skill Version(s):

1.0.0 (source: server release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
