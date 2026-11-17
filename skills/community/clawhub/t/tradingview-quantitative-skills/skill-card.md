## Description:

Professional quantitative investment analysis system based on TradingView data that provides stock screening, technical pattern recognition, market review, risk management, and event-driven analysis with multi-factor scoring and trading strategies.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hypier](https://clawhub.ai/user/hypier)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query TradingView-backed market data and produce stock screening, technical analysis, market review, news and event analysis, and risk-management reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Credential exposure through MCP setup or example endpoints.

Mitigation: Use only a verified MCP endpoint, keep API keys and JWTs in a secret store or environment variable, and do not send bearer tokens to example hosts.

Risk: Mutable npm execution can resolve different package code over time.

Mitigation: Prefer pinned npm package versions and review resolved packages before installing or updating the MCP configuration.

Risk: Market analysis outputs can be mistaken for personalized investment advice.

Mitigation: Treat buy, sell, options, crypto, and position-size outputs as educational market analysis and independently verify data before trading.

Risk: External market-data services receive symbols, queries, authentication headers, and API requests.

Mitigation: Send only necessary market queries, review RapidAPI and provider terms, monitor API usage, and stay within rate limits.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/hypier/skills/tradingview-quantitative-skills)
- [TradingView Data API](references/api-documentation.md)
- [MCP Tools Usage Guide](references/mcp-tools-guide.md)
- [Technical Analysis Methodology](references/technical-analysis.md)
- [Technical Pattern Recognition Library](references/pattern-library.md)
- [Risk Management System](references/risk-management.md)
- [US Stock Practical Examples](references/us-stock-examples.md)
- [China A-Share Practical Examples](references/china-a-stock-examples.md)
- [Security Policy](SECURITY.md)
- [RapidAPI TradingView Data API](https://rapidapi.com/hypier/api/tradingview-data1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline JSON and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include educational trading recommendations, position sizing, and risk warnings based on external market data.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
