# stocki-financial-reader

OpenClaw aggregate skill for institutional-grade financial data. Routes user queries about real-time quotes, financials, valuation time series, OHLCV history, industry membership, consensus forecasts, and composite analysis to 8 reference contracts that drive the stocki gateway (`skill.stocki.com.cn`).

For ClawBot (WeChat / Lark / WhatsApp / ...) end users via OpenClaw agents.

> **Disclaimer**: This skill is a financial-data retrieval tool that surfaces structured quote, financial, valuation, and consensus data through the stocki gateway. It does NOT constitute investment advice or buy/sell recommendations, and it does NOT execute any transactions. Data may be delayed or subject to upstream adjustments; users should verify independently before making decisions. The application integrating this skill is responsible for ensuring final outputs comply with the regulations of its jurisdiction.

## Architecture

- `SKILL.md` — top-level OpenClaw router (frontmatter + Routing Table + R1–R8)
- `references/<n>.md` — 8 reference contracts (one per endpoint family)
- `scripts/{_http,doctor,diagnose}.py` — shared HTTP helper + self-diagnostics
- `INSTALL.md` — install & setup

## References

| Reference | Purpose | Primary endpoint |
|---|---|---|
| [`market-calendar`](references/market-calendar.md) | Market status / trading days / availability | `GET /api/v3/market/*`, `/availability` |
| [`realtime-quote`](references/realtime-quote.md) | Real-time quotes (multi-asset batch + fundamentals snapshot) | `POST /api/v3/quotes/get_*latest_quotes` |
| [`price-history`](references/price-history.md) | OHLCV history / adjustments / interval returns | `POST /api/v3/datareader/read` (`data_type=price`) |
| [`industry-and-symbols`](references/industry-and-symbols.md) | Industry membership / index members / share / company profile | `POST /api/v3/datareader/read` + `/api/v2/market_symbol/get_symbols` |
| [`fundamentals-panel`](references/fundamentals-panel.md) | Financial statements / derived indicators / market cap / valuation panels | `POST /api/v3/datareader/read` (financial / indicator / market_cap / valuation) |
| [`consensus-and-target`](references/consensus-and-target.md) | Consensus forecasts / target prices / revenue breakdown | `POST /api/v3/datareader/read` |
| [`financial-context`](references/financial-context.md) | One-shot composite view (L1 quote, L2 fundamentals, L3 consensus) | `POST /api/v3/financial_context/{cn,hk}` |
| [`metric-resolver`](references/metric-resolver.md) ⚠ pending | Metric name resolution (CN / EN / synonyms → canonical) | `POST /api/v2/market_metric/get_metrics` |

## Install / Setup

See [INSTALL.md](INSTALL.md).

## License

MIT-0 (enforced by ClawHub on publish). Anyone may use, modify, and redistribute without attribution.

## Data Usage

Repository code is released under MIT-0. However, the data returned by this skill at runtime is provided by the stocki gateway and **is NOT covered by MIT-0** — it is subject to the stocki data service agreement.

- Personal / research queries: governed by your stocki API key's terms of use
- Bulk scraping, redistribution, or commercial re-distribution: contact the stocki team for separate licensing
