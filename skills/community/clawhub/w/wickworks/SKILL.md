---
name: wickworks
description: Stateless OHLC primitives service: candlestick bars in, technical indicators + Smart-Money-Concepts objects out. Single POST / takes a bars array + an indicators selection map and returns computed primitives; GET /metadata is the output-path catalog; GET /health. 67 primitives across trend (SMA/EMA + 15 more MAs, Donchian, Ichimoku), momentum (RSI, MACD, Stoch, StochRSI, ADX, MFI, CCI, Williams %R, ROC, MOM, TSI, TRIX, UO, Fisher), volatility (ATR, NATR, Bollinger, Keltner, Squeeze), volume (VWAP, VWMA, OBV, AD, ADOSC, CMF, KVO), and SMC (order blocks, fair-value gaps, BOS/CHoCH, swing structure, S/R levels, liquidity, retracements, sessions, previous-period H/L) plus pre-baked summaries. camelCase, NaN-safe JSON. Unified REST + MCP (streamable-HTTP at /mcp, tools health / list_indicators / metadata / compute). Auth-less by default. Use when the user wants technical indicators or Smart-Money-Concepts primitives computed from OHLC candlestick bars.
homepage: https://github.com/psyb0t/docker-wickworks
user-invocable: true
metadata:
  { "openclaw": { "emoji": "🕯️", "primaryEnv": "WICKWORKS_URL", "requires": { "bins": ["docker", "curl"] } } }
---

# wickworks

Stateless OHLC primitives service: bars in, indicators + Smart-Money-Concepts objects out. No scoring, no opinions, no state.

- **Trend:** SMA/EMA + 15 other moving averages (`dema`, `tema`, `hma`, `kama`, `zlma`, `t3`, `alma`, `jma`, …), `linreg`, Donchian channels, Ichimoku.
- **Momentum:** RSI, MACD, Stochastic, StochRSI, ADX, MFI, CCI, Williams %R, ROC, MOM, TSI, TRIX, Ultimate Oscillator, Fisher.
- **Volatility:** ATR, NATR, Bollinger Bands, Keltner Channels, Squeeze.
- **Volume:** VWAP (anchored), VWMA, OBV, AD, ADOSC, CMF, KVO.
- **SMC:** order blocks, fair-value gaps (`fvg`/`fvgs`), BOS/CHoCH (`bosChoch`), swing structure (`swingLevels`), S/R levels (`srLevels`), `liquidity`, `retracements`, `sessions`, previous-period H/L (`previousHighLow`).
- **Summaries:** `levels`, `position`, `slope`, `momentum`, `volume`, `recentRange`, `price`. Pre-baked last-bar projections over the raw series.
- **Two ways to drive it:** the REST API (`POST /`) and an MCP server (streamable-HTTP at `/mcp`). Same compute, same output envelope.

All JSON field names are **camelCase**; output is **NaN-safe** (`NaN` → `null`). Bars are UTC unix seconds; the container runs `TZ=UTC`.

For installation, configuration, and container setup, see [references/setup.md](references/setup.md).

## Security & safety

- **Stateless + read-only:** every call is self-contained, bars in, primitives out. wickworks stores nothing, writes no files, mutates nothing, and has **no destructive operations**. There is no state to corrupt and nothing to confirm before calling.
- **Auth-less by default, network-exposed:** wickworks ships with no built-in auth; anyone who can reach the port can call it. Bind it to loopback (`-p 127.0.0.1:8000:8000`) and only expose it behind your own reverse proxy / VPN with auth if it needs to be reachable off-host. The MCP bridge's optional `WICKWORKS_TOKEN` is for a bearer your *proxy* enforces, not wickworks itself.
- **Consumer of the data you send:** you hand it OHLC bars; it computes on them and returns numbers. It does not fetch, phone home, or transmit your bars anywhere. Point the skill only at a wickworks instance you (or a trusted operator) run.
- **Bounded input:** the request is capped at `MAX_BARS` bars (default 5000); oversized requests get `413`. Every indicator needs a minimum number of bars (SMC outputs and summaries need `MIN_BARS`, default 50), or the request returns an `insufficient_bars` error listing the deficits.

## When To Use

- The user has OHLC candlestick bars and wants technical indicators computed (RSI, MACD, Bollinger, Ichimoku, Supertrend, …).
- The user wants Smart-Money-Concepts structure: order blocks, fair-value gaps, BOS/CHoCH, swing highs/lows, support/resistance, liquidity pools.
- You're enriching a trading/market dataset server-side and want one call to return many primitives at once.

## When NOT To Use

- The user wants a *forecast*, a *signal*, or a buy/sell *opinion*. wickworks emits primitives only, no scoring. (Forecasting is a different service.)
- You don't have OHLC bars (wickworks computes on bars you supply; it has no market-data feed of its own).
- You need indicators over more than `MAX_BARS` bars in one call. Window it down or raise `MAX_BARS` on the server.

## Setup

```bash
export WICKWORKS_URL="http://localhost:8000"   # your running instance
```

See [references/setup.md](references/setup.md) to stand one up (`docker run` or docker compose).

## The compute contract: `POST /`

One endpoint does the work. Body:

```json
{
  "symbol": "SYMBOL_X",
  "timeframe": "H1",
  "bars": [
    { "time": 1700000000, "open": 100, "high": 102, "low": 99, "close": 101, "volume": 1200 }
  ],
  "indicators": { "rsi": true, "macd": true }
}
```

- **`bars`:** array of `{ time (UTC unix seconds), open, high, low, close, volume }`. `volume` is required, finite, and non-negative. The caller chooses the activity or volume series before calling Wickworks.
- **`indicators`:** a map of **output-name → spec**. This is the whole point:
  - `"rsi": true` → run `rsi` with defaults, output under key `rsi`.
  - `"rsi14": { "type": "rsi", "length": 14 }` → run `rsi` with `length=14`, output under key `rsi14` (the key is the output name, `type` picks the indicator).
  - `"rsi": { "length": 21 }` → key doubles as the type when no `type` is given.
- **`symbol` / `timeframe`:** echoed back in the response. `timeframe` is an opaque chart interval label, not a resampling instruction.

Response envelope: `{ symbol, timeframe, candles, <outputName>: <series-or-object>, ... }`, one entry per requested output, each a series the same length as `bars` (or a structured object for multi-line indicators like `macd` / `bbands` / `ichimoku`, or an array of objects for SMC like `orderBlocks` / `fvgs`).

```bash
# Health
curl -s "$WICKWORKS_URL/health"

# The output-path catalog (labels + descriptions; static per version, so cache it)
curl -s "$WICKWORKS_URL/metadata"

# Compute RSI + MACD + order blocks in one call
curl -s -X POST "$WICKWORKS_URL/" -H 'Content-Type: application/json' -d '{
  "symbol": "SYMBOL_X", "timeframe": "H1",
  "bars": [ /* ...OHLC bars... */ ],
  "indicators": { "rsi": true, "macd": true, "orderBlocks": true }
}'
```

## Indicator names

Pass any of these as `indicators` keys (also available at runtime via the MCP `list_indicators` tool):

```
ad, adosc, adx, alma, aroon, atr, bbands, bosChoch, cci, chandelierExit, cmf,
dema, donchian, ema, fisher, fvg, fvgs, fwma, hma, ichimoku, jma, kama, kc, kvo,
levels, linreg, liquidity, macd, mfi, mom, momentum, natr, obv, orderBlocks,
position, previousHighLow, price, psar, recentRange, retracements, rma, roc, rsi,
sessions, sinwma, slope, sma, squeeze, srLevels, stoch, stochrsi, supertrend,
swingLevels, swma, t3, tema, trima, trix, tsi, uo, volume, vortex, vwap, vwma,
willr, wma, zlma
```

Fetch `GET /metadata` (or the MCP `metadata` tool) for the human-readable label + description of every output path each of these produces.

## MCP Endpoint (`/mcp`)

wickworks mounts a [Model Context Protocol](https://modelcontextprotocol.io) server over Streamable HTTP at `/mcp`, in the same process, so an agent can drive it over JSON-RPC without the REST client. It's **stateless** (no initialize handshake needed) and returns JSON. Tools:

| Tool | Args | Returns |
|---|---|---|
| `health` | none | `{ ok, version }` |
| `list_indicators` | none | `{ indicators: [...] }`, the registered indicator types |
| `metadata` | none | the output-path catalog (`{ version, count, entries }`) |
| `compute` | `bars`, `indicators`, `timeframe?`, `symbol?` | the same envelope as `POST /` |

Point an MCP client straight at the endpoint:

```bash
# Claude Code (native remote MCP, no bridge needed)
claude mcp add --transport http wickworks "$WICKWORKS_URL/mcp"

# Raw JSON-RPC (stateless, call tools/call directly)
curl -s "$WICKWORKS_URL/mcp/" \
  -H 'Content-Type: application/json' \
  -H 'Accept: application/json, text/event-stream' \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call",
       "params":{"name":"compute","arguments":{
         "bars":[/* ...OHLC... */],"indicators":{"rsi":true},"symbol":"SYMBOL_X","timeframe":"H1"}}}'
```

The [`@psyb0t/wickworks`](https://github.com/psyb0t/docker-wickworks/tree/main/.agents/plugins/wickworks) OpenClaw plugin is a thin stdio↔HTTP bridge to this endpoint for MCP clients that only speak local stdio servers.

## Errors

- `400 bars must not be empty` / `400 indicators must not be empty`: empty request pieces.
- `400 { error: "insufficient_bars", available, deficits }`: a requested indicator needs more bars than supplied; `deficits` lists which and how many.
- `400` unknown indicator: the requested `type`/key isn't in the registry (see the indicator-names list above). Unknown or out-of-range parameters are also `400`.
- `422`: the body fails schema validation (missing or extra field, non-positive price, bad candle geometry, bar times not strictly increasing).
- `413 too many bars`: more than `MAX_BARS` bars in one request.

Over MCP the same failures come back as an `isError` tool result carrying the message, not an HTTP status.
