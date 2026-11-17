## Description:

Retrieves real-time A-share stock quotes from Eastmoney and produces basic technical-analysis reports using MA, RSI, and MACD indicators.

This skill is ready for commercial/non-commercial use.

## Publisher:

[will1189](https://clawhub.ai/user/will1189)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to query A-share stock prices, price changes, volume, and related market fields, then request basic MA, RSI, and MACD technical analysis. Its output should be treated as informational market analysis rather than personalized financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may visit Eastmoney quote pages for stock codes requested by the user.

Mitigation: Install only where this network access pattern is acceptable, and review requested stock codes before use in sensitive contexts.

Risk: MA, RSI, MACD, and buy/sell signal wording can be mistaken for personalized financial advice.

Mitigation: Present the analysis as informational technical-analysis output and require independent research before making investment decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/will1189/skills/stock-acquisition-analysis)
- [Eastmoney Shanghai quote page pattern](https://quote.eastmoney.com/sh{stock_code}.html)
- [Eastmoney Shenzhen quote page pattern](https://quote.eastmoney.com/sz{stock_code}.html)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown or structured text with quote fields, indicator calculations, and technical-analysis commentary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include informational buy/sell signal wording based on technical indicators; not personalized financial advice.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
