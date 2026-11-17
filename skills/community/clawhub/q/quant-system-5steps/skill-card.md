## Description:

5-Step Quant Trading System with multi-source data, enhanced ML models, and 15+ strategy templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pikachu022700](https://clawhub.ai/user/pikachu022700)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to run a five-step cryptocurrency quant workflow for market-data collection, technical analysis, model training, strategy generation, and backtest review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Trading outputs may be misleading because the workflow can silently use simulated data and under-tested strategies.

Mitigation: Treat outputs as experimental, verify market data provenance, and avoid using backtest or signal results for real trading decisions unless the synthetic-data fallback and strategy execution gaps are fixed or clearly surfaced.

Risk: Public crypto-market API failures can reduce data reliability for analysis and backtesting.

Mitigation: Review the collected data source before relying on generated signals, strategy code, or performance metrics.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pikachu022700/skills/quant-system-5steps)
- [ClawHub metadata homepage](https://clawhub.com/quant-system-5steps)
- [Hyperliquid info API](https://api.hyperliquid.xyz/info)
- [Binance ticker price API](https://api.binance.com/api/v3/ticker/price?symbol={symbol})
- [Binance order book API](https://api.binance.com/api/v3/depth?symbol={symbol}&limit=10)
- [Binance klines API](https://api.binance.com/api/v3/klines?symbol={symbol}&interval={interval}&limit={limit})

## Skill Output:

**Output Type(s):** [text, json, code, guidance]

**Output Format:** [Python dictionary / JSON-like result with console text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes market-data analysis, a model signal, generated strategy code, backtest metrics, and optimization suggestions.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
