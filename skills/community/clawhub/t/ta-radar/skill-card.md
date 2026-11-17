## Description:

TA Radar generates objective cryptocurrency technical-analysis reports for spot trading pairs and on-chain contract addresses using EMA, RSI, MACD, Bollinger Bands, support and resistance levels, and trend analysis.

This skill is ready for commercial/non-commercial use.

## Publisher:

[deanpeng-dotcom](https://clawhub.ai/user/deanpeng-dotcom)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use TA Radar to request cryptocurrency technical-analysis reports for tickers or contract addresses across 1h, 4h, and 1d intervals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Asset tickers or contract addresses are sent to public market-data services and the allorigins.win proxy.

Mitigation: Use only non-sensitive symbols or public contract addresses, and run the skill only when sharing those lookups with the named services is acceptable.

Risk: The execution workflow uses a predictable temporary script path at /tmp/ta_radar_run.py.

Mitigation: Run the skill in an isolated account or container and remove the temporary script after execution.

Risk: The security evidence marks the release suspicious and recommends verifying package completeness before relying on it.

Mitigation: Review the packaged files and security findings before deployment or recurring use.

## Reference(s):

- [TA Radar ClawHub Skill Page](https://clawhub.ai/deanpeng-dotcom/skills/ta-radar)
- [Publisher Profile](https://clawhub.ai/user/deanpeng-dotcom)
- [Repository Metadata](https://github.com/clawhub/ta-radar)
- [Deployment Guide](references/deployment.md)
- [Binance Kline Data Endpoint](https://api.binance.info/api/v3/klines)
- [Gate.io Candlestick Data Endpoint](https://api.gateio.ws/api/v4/spot/candlesticks)
- [DexScreener Search Endpoint](https://api.dexscreener.com/latest/dex/search)
- [AllOrigins Proxy Endpoint](https://api.allorigins.win/raw)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown and console text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TA_SYMBOL and optionally TA_INTERVAL; fetches public market data from Binance, Gate.io, and DexScreener via allorigins.win.]

## Skill Version(s):

1.2.0 (source: evidence release, SKILL.md frontmatter, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
