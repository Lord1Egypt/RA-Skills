## Description:

Provides simplified access to US and Hong Kong stock data, including prices, history, company information, financials, analyst insights, screeners, options, and news through Yahoo Finance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xdl2003](https://clawhub.ai/user/xdl2003)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to retrieve market data for US and Hong Kong equities, including prices, historical data, company fundamentals, analyst information, screeners, options, and related news. Returned data should be treated as third-party market data rather than investment advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill installs and uses third-party Python packages for market data access.

Mitigation: Install yfinance and pandas from a trusted package source and prefer pinned dependency versions in controlled environments.

Risk: Yahoo Finance market data may be delayed, incomplete, rate limited, or unavailable for some symbols.

Mitigation: Treat returned data as third-party market data, handle network and symbol errors, and avoid relying on it alone for financial decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xdl2003/skills/yfinance-client)
- [Publisher profile](https://clawhub.ai/user/xdl2003)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown guidance with Python code examples and callable client methods returning Python objects such as floats, dictionaries, lists, and pandas DataFrames]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses yfinance and pandas; market data may be delayed, incomplete, unavailable for some symbols, or subject to rate limiting.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
