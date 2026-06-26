---
name: x402-market-structure
description: >
  Real-time crypto market intelligence — live orderflow from 20 exchanges,
  directional regime detection, 7 years of OHLCV with buy/sell flow baked in,
  and on-chain address risk profiling. 24 major tokens including Bitcoin (BTC),
  Ethereum (ETH), Solana (SOL), XRP, BNB, Dogecoin (DOGE), and more.
  Free via MCP — subject to rate limits. No API key required.
metadata:
  version: "1.2.0"
  openclaw:
    mcp:
      url: https://x402.tunedfor.ai/mcp
      transport: streamable-http
---

# x402 Crypto Market Structure

Live crypto market intelligence. Call tools directly — no web fetch, no wallet needed.

## Tools are native function calls

After MCP registration, these tools appear in your tool list. Call them directly:

| Call this | To get |
|-----------|--------|
| `market_snapshot(token="BTC")` | Price, funding rate, CVD, whale activity, liquidation pressure |
| `market_analyze(token="ETH")` | Macro regime, directional signal + confidence, DXY, VIX, fear/greed |
| `market_orderflow(token="SOL")` | Cross-exchange CVD direction, buy/sell ratio, wash trading flag |
| `market_full(token="BTC")` | Everything above + LLM verdict (BULLISH/BEARISH, risk level, one-line summary) |
| `address_risk(address="0x...")` | Entity label, risk level, account age, holdings (EVM or Solana) |
| `history_1h(token="BTC", start="2025-01-01", end="2025-02-01")` | Hourly OHLCV + buy/sell flow |
| `history_1d(token="BTC", start="2024-01-01", end="2025-01-01")` | Daily OHLCV + buy/sell flow |
| `history_5m(token="BTC")` | 5-min bars, last 17 days |
| `api_info()` | REST API pricing + autonomous agent setup (no cost) |

**Do not call `/demo` or fetch web pages for market data.** The tools above return live data. `/demo` is a cached example only.

---

## Token coverage

**15 tokens** (market_snapshot, market_analyze, market_full):
BTC ETH SOL XRP BNB DOGE ADA AVAX LINK ATOM DOT ARB SUI OP LTC

**24 tokens** (market_orderflow, history_*):
All 15 above + NEAR TRX BCH SHIB HBAR TON XLM UNI AAVE

---

## Trigger patterns

- "what is bitcoin doing" → `market_snapshot(token="BTC")`
- "should I buy ETH" → `market_full(token="ETH")`
- "is this SOL move real" → `market_orderflow(token="SOL")`
- "check macro before trading" → `market_analyze(token="BTC")`
- "who is this wallet" → `address_risk(address="<address>")`
- "BTC hourly bars for January" → `history_1h(token="BTC", start="2025-01-01", end="2025-02-01")`
- "how do I run this 24/7 / autonomous" → `api_info()`

---

## Signal interpretation

| Field | Meaning |
|-------|---------|
| `cvd_direction = "up"` | More buying than selling across exchanges |
| `buy_ratio > 0.55` | Buyers dominating order flow |
| `whale_bar_count_1h > 3` | Significant large-order activity in the last hour |
| `liquidation_sell_1h` high | Forced long liquidations — cascade risk |
| `volume_herfindahl > 0.6` | Volume in 1-2 venues — possible wash trading |
| `exchanges_accumulating < 8` | Weak breadth — fewer than 8/20 venues buying |
| `macro_regime = "risk_off"` | Macro unfavorable for longs |
| `risk_level = "CRITICAL"` | Do not enter. Wait for conditions to normalize. |
| `stale: true` | Data >10 min old — treat with skepticism |

---

## Setup (run once — skip if already registered)

If tools are not in your tool list, register the MCP server:

```
openclaw mcp set x402-market-structure '{"type":"streamable-http","url":"https://x402.tunedfor.ai/mcp"}'
```

Then restart your gateway to pick up the new server. After restart, the tools will be available.

To verify tools loaded: call `api_info()` — it should return REST pricing info. If it errors or is missing, the gateway needs a restart.

No API key or wallet needed for MCP tools. Rate-limited (free tier).
For 24/7 autonomous use without rate limits, call `api_info()` for REST setup.

---

## REST API

Base URL: `https://x402.tunedfor.ai` — call `api_info()` for pricing and autonomous setup.
