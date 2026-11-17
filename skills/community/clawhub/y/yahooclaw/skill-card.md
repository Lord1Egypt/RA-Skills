## Description:

Yahoo Finance API integration for OpenClaw. Use when users ask for stock prices, company financials, historical data, dividends, or market data. Supports real-time quotes, financial statements, and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to retrieve market data, stock quotes, historical prices, dividends, company metrics, news, and technical-analysis summaries inside an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release evidence reports an embedded Alpha Vantage API key.

Mitigation: Rotate or remove the embedded key and require Alpha Vantage credentials to be supplied through the runtime environment.

Risk: Weak input controls around outbound market-data requests can create unreliable or excessive provider calls.

Mitigation: Validate and encode ticker and indicator parameters, and enforce practical batch and news limits before deployment.

Risk: Technical indicators and sentiment summaries can be mistaken for investment advice.

Mitigation: Present financial analysis as informational output and require users to verify decisions against authoritative financial sources.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/leohuang8688/skills/yahooclaw)
- [Yahoo Finance](https://finance.yahoo.com/)
- [Alpha Vantage API key documentation](https://www.alphavantage.co/support/#api-key)
- [OpenClaw documentation](https://docs.openclaw.ai/)
- [API configuration](docs/API-CONFIGURATION.md)
- [Usage scenarios](docs/USAGE-SCENARIOS.md)

## Skill Output:

**Output Type(s):** [JSON, Text, Analysis, Guidance]

**Output Format:** [JSON objects with short text summaries for quotes, history, dividends, news, and technical indicators]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Market data may be delayed, rate-limited, or unavailable depending on upstream providers.]

## Skill Version(s):

0.1.7 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
