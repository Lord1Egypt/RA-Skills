## Description:

Yahoo Finance API integration for OpenClaw. Use when users ask for stock prices, company financials, historical data, dividends, or market data. Supports real-time quotes, financial statements, and market analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[leohuang8688](https://clawhub.ai/user/leohuang8688)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external OpenClaw users use YahooClaw to retrieve market quotes, historical prices, technical indicators, dividends, and stock-related news for finance-oriented agent workflows. Its market analysis and buy/sell wording should be treated as informational output, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Queried symbols are sent to Yahoo Finance and returned market data may be delayed or inaccurate.

Mitigation: Inform users that results are third-party market data, verify time-sensitive prices against authoritative sources, and avoid using the output as the only basis for trading decisions.

Risk: The artifact includes buy/sell recommendation wording from technical indicators.

Mitigation: Present recommendations as informational analysis only and add product-level review or disclaimers before exposing them in finance workflows.

Risk: The package uses third-party dependencies for market data retrieval.

Mitigation: Pin and review dependencies in controlled environments before deployment.

## Reference(s):

- [YahooClaw on ClawHub](https://clawhub.ai/leohuang8688/skills/yahoo-claw)
- [Yahoo Finance](https://finance.yahoo.com/)
- [OpenClaw Documentation](https://docs.openclaw.ai/)

## Skill Output:

**Output Type(s):** [text, code, configuration, guidance]

**Output Format:** [JSON-style JavaScript objects and concise natural-language responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Network-backed market data responses may include delayed prices, historical quotes, technical indicators, news sentiment, and error messages.]

## Skill Version(s):

0.1.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
