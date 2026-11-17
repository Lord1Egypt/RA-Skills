## Description:

Fetch real-time crypto prices and calculate technical indicators (SMA, EMA, MACD, RSI, Bollinger Bands, ATR) for BTC, ETH, SOL, BNB, XRP, DOGE using multi-source market data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[totoxu](https://clawhub.ai/user/totoxu)

### License/Terms of Use:

MIT

## Use Case:

External users and agents use this paid OpenClaw skill to retrieve cryptocurrency market data, historical OHLCV data, and technical-analysis signals for supported coins. Results should be presented as educational market analysis, not financial advice.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Paid invocations contact SkillPay and the release includes a packaged billing credential.

Mitigation: Remove and rotate the hardcoded billing key before installation; configure billing through environment variables and make user billing consent explicit.

Risk: The skill contacts external market-data and billing APIs during normal use.

Mitigation: Install only where those network destinations and data-sharing expectations are acceptable; monitor failures and present payment links only when billing errors require them.

Risk: Automated buy, sell, and neutral signals could be mistaken for investment advice.

Mitigation: Present outputs as educational technical analysis and include the cryptocurrency volatility and non-financial-advice disclaimer from the artifact.

Risk: Runtime dependency versions are not pinned in the artifact.

Mitigation: Pin and review dependencies before production deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/totoxu/skills/totoxu-crypto-analyzer)
- [Publisher Profile](https://clawhub.ai/user/totoxu)
- [Binance API](https://api.binance.com/api/v3)
- [CoinGecko API](https://api.coingecko.com/api/v3)
- [CoinCap API](https://api.coincap.io/v2)
- [CryptoCompare API](https://min-api.cryptocompare.com/data)
- [SkillPay Billing API](https://skillpay.me/api/v1/billing)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; scripts return JSON market data, historical data, billing errors, and technical-indicator analysis.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3.9+, requests, supported coin symbols, and billing environment variables for non-test paid invocations.]

## Skill Version(s):

1.3.0 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
