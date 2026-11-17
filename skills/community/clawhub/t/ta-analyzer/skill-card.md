## Description:

Multi-timeframe technical analysis skill using CCXT. Calculates 20+ indicators including RSI, MACD, Bollinger Bands, Ichimoku, Stochastic, Williams %R, ADX, MFI, CCI, Fibonacci, Pivot Points, Support/Resistance, and detects 10+ chart patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raphael2025](https://clawhub.ai/user/raphael2025)

### License/Terms of Use:

MIT

## Use Case:

Developers and external users use this skill to fetch public crypto market data and generate multi-timeframe technical-analysis summaries, indicator values, chart-pattern detections, and trading-style signals.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading recommendations, stop-loss, take-profit, and price-prediction outputs may be incorrect or misleading.

Mitigation: Treat all outputs as informational technical analysis, validate them against independent market data, and do not use them as professional financial advice.

Risk: The skill depends on public Binance market data fetched through CCXT, so results may be unavailable, delayed, rate-limited, or affected by exchange data issues.

Mitigation: Check for fetch errors, confirm timestamps and prices before acting, and retry or compare against another trusted data source when results look stale or incomplete.

Risk: Some generated reasons and volume-analysis strings may appear in Chinese.

Mitigation: Review localized text before presenting it to users who require English-only outputs.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raphael2025/skills/ta-analyzer)
- [Publisher Profile](https://clawhub.ai/user/raphael2025)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Guidance]

**Output Format:** [JSON object with indicator values, detected patterns, trend summaries, recommendations, stop-loss, and take-profit fields.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fetches public Binance OHLCV data via CCXT; outputs are informational trading signals and may include Chinese text.]

## Skill Version(s):

1.0.0 (source: package.json and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
