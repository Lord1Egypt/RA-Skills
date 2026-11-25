---
name: realcryptocap
description: Answer crypto price, ranking, comparison and market-overview questions with live RealCryptoCap data (HTX primary price source, real market cap rankings, Pro market datasets).
version: 1.0.0
---

# RealCryptoCap

Use the RealCryptoCap MCP tools for any question about crypto prices, rankings or what the market is doing. They return live numbers.

| Question | Tool |
|---|---|
| "What's BTC at?", "How is SOL doing?", "Compare ETH and SOL" | `get_crypto_prices` |
| "Top 20 coins", "biggest cryptos" | `get_top_cryptos` |
| "What's the market doing?", "morning brief" | `get_market_brief` |
| "Latest crypto news" | `get_crypto_news` |
| Fear & Greed, funding / open interest / long-short, ETF flows, signals, global liquidity, stablecoin supply, real vs reported cap | `get_fear_greed`, `get_derivatives`, `get_etf_flows`, `get_trading_signals`, `get_global_liquidity`, `get_stablecoin_supply`, `get_real_vs_reported_market_cap` (Pro) |

- Quote prices from the tools, with the time they were updated.
- "Real market cap" ranks native cryptocurrencies; stablecoins, wrapped/staked receipts and tokenized assets are listed separately.
- Show several coins as a table.
- Market data, not financial advice.

Server: `https://realcryptocap.com/mcp` (free tier without sign-in). Pro members add `Authorization: Bearer <RealCryptoCap API key>` from realcryptocap.com/account, or use `https://realcryptocap.com/mcp/auth` to sign in with RealCryptoCap.
