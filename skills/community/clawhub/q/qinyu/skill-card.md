## Description:

QinYu Pro v2.0 is an all-in-one cryptocurrency analysis skill that fetches public market data to provide real-time prices, technical indicators, market sentiment, DeFi analytics, funding rates, gas prices, and spot/futures strategy guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[woshiqinyu520](https://clawhub.ai/user/woshiqinyu520)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use QinYu to request Chinese-language cryptocurrency market analysis, price checks, technical indicators, DeFi and futures context, and informational trading-strategy guidance for supported crypto assets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may provide trading or leverage suggestions that users could mistake for financial advice.

Mitigation: Present outputs as informational analysis only and require users to make decisions based on their own risk tolerance and independent review.

Risk: The skill contacts public cryptocurrency data APIs, so outputs depend on third-party API availability, freshness, and rate limits.

Mitigation: Check source availability and timestamps before relying on the analysis, and avoid treating failed or partial data fetches as complete market coverage.

## Reference(s):

- [QinYu ClawHub Skill Page](https://clawhub.ai/woshiqinyu520/skills/qinyu)
- [Supported Coins](references/supported_coins.md)
- [CoinGecko](https://www.coingecko.com/)
- [Binance API](https://api.binance.com/api/v3/ticker/24hr?symbol={symbol})
- [Alternative.me Fear and Greed API](https://api.alternative.me/fng/?limit=2)

## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Chinese-language terminal report or JSON, with command examples in Markdown documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes informational crypto market analysis, indicators, support/resistance levels, and spot/futures strategy suggestions.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
