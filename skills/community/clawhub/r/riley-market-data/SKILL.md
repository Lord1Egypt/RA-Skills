---
name: market-data
description: |
  Live macro, markets and developer-ecosystem data for research, finance, forecasting and
  trading agents — one cheap x402 call each, no API keys.

  USE FOR:
  - Country economic indicators: GDP, growth, inflation, unemployment, GDP/capita, population
  - DeFi-vs-risk-free spread (top stablecoin yields vs US T-bill rate) + verdict
  - Official US Treasury average rates + total public debt
  - Trending GitHub repos, npm download counts, Hacker News top stories

  TRIGGERS:
  - "GDP", "inflation", "unemployment", "economy of [country]", "macro data"
  - "treasury rate", "t-bill", "risk free rate", "defi spread", "national debt"
  - "trending github", "npm downloads", "hacker news", "top repos"

  Use x402 GET calls. Never guess paths — use the exact URLs below or GET /samples first.
mcp:
  - agentcash
---

# Market & Macro Data with the x402 Agent Store

> All endpoints are GET on `https://store.agentexchange.work`. Paid calls return HTTP 402;
> your x402 client signs USDC on Base and retries. Free preview: `GET /samples`.

## Quick Reference

| Task | Endpoint | Price |
|------|----------|-------|
| Country economic indicators (200+) | `https://store.agentexchange.work/macro/country?country=USA` | $0.005 |
| DeFi vs risk-free spread + verdict | `https://store.agentexchange.work/macro/risk-spread` | $0.005 |
| US Treasury rates + total public debt | `https://store.agentexchange.work/gov/treasury` | $0.002 |
| Trending GitHub repos | `https://store.agentexchange.work/github/trending?since=daily` | $0.001 |
| npm package download counts | `https://store.agentexchange.work/npm/downloads?package=react&period=week` | $0.001 |
| Hacker News top stories | `https://store.agentexchange.work/hn/top` | $0.001 |

## Notes
- All data is live from public sources (World Bank, Treasury fiscaldata, DefiLlama, GitHub, npm, HN).
- Free catalog: `GET https://store.agentexchange.work/` · Free samples: `GET /samples`.
