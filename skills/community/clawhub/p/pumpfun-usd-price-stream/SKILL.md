---
name: pumpfun-token-feed
description: >
  Real-time streaming PumpFun token feed on Solana with live USD pricing for every token.
  Subscribe to a live stream of PumpFun tokens over WebSocket: USD price (Open, High, Low,
  Close in USD), USD volume, USD moving averages (SMA, EMA, WMA), and tick-to-tick USD %
  change — streamed in real time from the Bitquery GraphQL API.
requires:
  env:
    - name: BITQUERY_API_KEY
      required: true
      description: Your Bitquery API token (required for WebSocket connection)
---

# PumpFun Token Feed — real-time streaming with USD pricing

This skill gives you a **real-time streaming PumpFun token feed** over WebSocket. Every tick carries **USD pricing for each token** — OHLC in USD, USD volume, USD-denominated moving averages (Mean, SMA, EMA, WMA), and tick-to-tick USD % change — all streamed live from the Bitquery API without polling.

Tokens are filtered to Solana network addresses containing "pump" (PumpFun tokens). `Price.IsQuotedInUsd` is always present so downstream code knows prices are already in USD.

---

## What to consider before installing

This skill implements a Bitquery WebSocket PumpFun token feed and uses one external dependency and one credential. Before installing:

1. **Registry metadata**: The registry may not list `BITQUERY_API_KEY` even though this skill and its script require it. Ask the publisher or update the registry metadata before installing so installers surface the secret requirement.
2. **Token only via URL**: Bitquery supports **no other auth method** — the token can **only** be passed in the WebSocket URL as `?token=...`. Because the token always appears in the URL, it can leak to logs, proxy logs, shell history, or IDE history. Never print or log the full URL; store the key only in an environment variable; rotate the key if it may have been exposed.
3. **Sandbox first**: Review and run the included script in a sandboxed environment (e.g. a virtualenv) to confirm behavior and limit blast radius.
4. **Source and publisher**: If the skill’s homepage or source is unknown, consider verifying the publisher or using an alternative with a verified source. If the registry metadata declares `BITQUERY_API_KEY` and the source/publisher are validated, this skill is likely coherent and benign.

---

## Prerequisites

- **Environment**: `BITQUERY_API_KEY` — your Bitquery API token (required).

**Credential and URL-only auth:** The Bitquery streaming endpoint accepts the token **only in the WebSocket URL** as a query parameter (`?token=...`). It does **not** support header-based auth or any other method. Therefore:
  - The token will always be present in the connection URL and can be exposed in **logs, proxy logs, shell history, or IDE history** if the URL is printed or logged.
  - **Do not** print or log the full WebSocket URL. Build the URL in code from an env var (e.g. `os.getenv("BITQUERY_API_KEY")`) and never emit it.
  - Store the key only in an environment variable; **rotate the key** if you suspect it was exposed (e.g. URL was logged or committed).

- **Runtime**: Python 3 and `pip`. Install the dependency: `pip install 'gql[websockets]'`.

---

## Security Checklist

**Before running this skill, confirm:**

- [ ] You have set `BITQUERY_API_KEY` in your environment: `export BITQUERY_API_KEY=your_token_here`
- [ ] You are running in a **sandboxed or isolated environment** (virtualenv, Docker, or dedicated machine)
- [ ] **Logging and shell history are disabled or monitored** to prevent URL capture: check `HISTFILE`, `.bash_history`, system logs, IDE debug output
- [ ] You understand that the WebSocket URL will contain your API token in plaintext in memory
- [ ] You have a plan to rotate your key if it is ever exposed
- [ ] You will **not** print, log, or commit the full URL to any file or logging system

If any of these cannot be confirmed, do not proceed with this skill until those conditions are met.

---

## Trader Use Cases

These are the key reasons a trader would use this feed:

**1. Entry / Exit Signal Detection**
Monitor the USD close price on every 1-second tick. When `Close (USD)` crosses a threshold or EMA diverges from SMA, trigger an entry or exit alert. The EMA reacts faster to price momentum than the SMA — traders watch for EMA/SMA crossovers on the stream.

**2. Momentum & Pump Detection**
Track tick-to-tick USD % change per token. A sudden spike (e.g. `+15% in one tick`) is a classic early-pump signal. Combine with `Volume.Usd` — a volume surge alongside a price spike confirms momentum vs. a noise candle.

**3. Scalping (very short-term trading)**
The 1-second tick interval is purpose-built for scalpers. Watch `Ohlc.High − Ohlc.Low` in USD to measure intra-second volatility. Wide spreads on small USD prices signal high volatility windows where scalp entries are possible.

**4. Stop-Loss / Take-Profit Monitoring**
Stream `Close (USD)` per token and compare against the trader's entry price (stored in session). Fire an alert when `Close < stop_loss_usd` or `Close > take_profit_usd`. Because prices are already in USD (`IsQuotedInUsd: true`), no conversion is needed.

**5. Volume Spike / Whale Alert**
`Volume.Usd` per tick tells you how many USD traded in that 1-second window. Sudden large USD volume on a low-mcap PumpFun token often precedes a price move. Filter ticks where `Volume.Usd > threshold` to surface whale activity.

**6. Multi-Token Price Dashboard**
The subscription returns ALL active PumpFun tokens simultaneously. Build a live leaderboard of tokens ranked by: highest USD price change, highest USD volume, or widest USD price range. Useful for scanning the entire PumpFun market at once.

**7. Mean Reversion**
When `Close (USD)` diverges significantly from `Average.Mean (USD)`, a mean-reversion trader expects a snapback. Watch for `(Close − Mean) / Mean > X%` on the stream to identify overextended moves.

**8. Token Launch Monitoring**
New PumpFun tokens appear in the stream as soon as they become active. Traders watching for newly launched tokens can detect first ticks: `tick_count == 1` for a given address = new token just went live.

---

## Step 1 — Check API Key

```python
import os
api_key = os.getenv("BITQUERY_API_KEY")
if not api_key:
    print("ERROR: BITQUERY_API_KEY environment variable is not set.")
    print("Run: export BITQUERY_API_KEY=your_token")
    exit(1)
```

If the key is missing, tell the user and stop. Do not proceed without it. 

---

## Step 2 — Run the stream

Install the WebSocket dependency once:

```bash
pip install 'gql[websockets]'
```

Use the streaming script:

```bash
python ~/.openclaw/skills/pumpfun-token-feed/scripts/stream_pumpfun.py
```

Optional: stop after N seconds:

```bash
python ~/.openclaw/skills/pumpfun-token-feed/scripts/stream_pumpfun.py --timeout 60
```

Or subscribe inline with Python:

```python
import asyncio, os
from gql import Client, gql
from gql.transport.websockets import WebsocketsTransport

async def main():
    token = os.environ["BITQUERY_API_KEY"]
    url = f"wss://streaming.bitquery.io/graphql?token={token}"
    transport = WebsocketsTransport(
        url=url,
        headers={"Sec-WebSocket-Protocol": "graphql-ws"},
    )
    async with Client(transport=transport) as session:
        sub = gql("""
            subscription {
                Trading {
                    Tokens(
                        where: {
                            Interval: {Time: {Duration: {eq: 1}}},
                            Token: {
                                NetworkBid: {},
                                Network: {is: "Solana"},
                                Address: {includesCaseInsensitive: "pump"}
                            }
                        }
                    ) {
                        Token { Address Name Symbol Network }
                        Block { Time }
                        Price {
                            IsQuotedInUsd
                            Ohlc { Open High Low Close }
                            Average { Mean SimpleMoving ExponentialMoving WeightedSimpleMoving }
                        }
                        Volume { Usd }
                    }
                }
            }
        """)
        async for result in session.subscribe(sub):
            tokens = result["Trading"]["Tokens"]
            for t in tokens:
                ohlc = t["Price"]["Ohlc"]
                vol  = t["Volume"]["Usd"]
                print(
                    f"{t['Token']['Symbol']} | "
                    f"USD Close: ${float(ohlc['Close']):.8f} | "
                    f"Vol USD: ${float(vol):,.2f}"
                )

asyncio.run(main())
```

---

## Step 3 — USD pricing fields on every tick

All prices on the stream are already **quoted in USD** (`Price.IsQuotedInUsd = true` for PumpFun/Solana tokens). No conversion required.

| Field | What it means for traders |
|---|---|
| `Price.Ohlc.Open` (USD) | USD price at the start of this 1s tick |
| `Price.Ohlc.High` (USD) | Highest USD price traded in this tick |
| `Price.Ohlc.Low` (USD) | Lowest USD price traded in this tick |
| `Price.Ohlc.Close` (USD) | Final USD price — use for entry/exit/stop logic |
| `Price.Average.Mean` (USD) | Simple mean USD price over the interval |
| `Price.Average.SimpleMoving` (USD) | SMA — smoothed USD trend line |
| `Price.Average.ExponentialMoving` (USD) | EMA — reacts faster to USD price moves |
| `Price.Average.WeightedSimpleMoving` (USD) | WMA — weighted USD average |
| `Volume.Usd` | Total USD traded in this tick — whale / momentum signal |
| Tick Δ % | Computed from consecutive Close (USD) values |

> **Note on USD scale**: PumpFun tokens commonly trade at `$0.00000001`–`$0.001` USD. Always display 8 decimal places to avoid showing `$0.00`.

---

## Step 4 — Format output for traders

When presenting USD-priced ticks to a trader, use this layout:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
PumpFun: BONK  (bonkABcD...pumpXyZw)  [Solana]
Time: 2025-03-06T14:00:01Z
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
USD Price  │  Open:  $0.00001234   High: $0.00001350
           │  Low:   $0.00001200   Close: $0.00001310  ← entry/exit ref
USD Averages
  Mean:    $0.00001270
  SMA:     $0.00001260
  EMA:     $0.00001275   (EMA > SMA → bullish momentum)
  WMA:     $0.00001268
Tick Δ:   +0.61% USD vs previous tick

USD Volume:  $45,678.00   ← whale check
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Interval (subscription)

The default subscription uses **duration 1** (1-second tick data). The same `Trading.Tokens` subscription supports other durations in the `where` clause for different trader timeframes:

| Duration | Use case |
|---|---|
| `1` | Scalping, pump detection (1-second ticks) |
| `5` | Short-term momentum, 5-second bars |
| `60` | Intraday swing — 1-minute candles |
| `1440` | Daily candles for longer-term tracking |

---

## Filter Logic

The subscription filters tokens by three conditions simultaneously:
- `Network: {is: "Solana"}` — Solana blockchain only
- `Address: {includesCaseInsensitive: "pump"}` — address must contain "pump" (PumpFun tokens)
- `NetworkBid: {}` — Bitquery network bid filter (required)
- `Interval.Time.Duration: {eq: 1}` — 1-second candles

---

## Error handling

- **Missing BITQUERY_API_KEY**: Tell user to export the variable and stop
- **WebSocket connection failed / 401**: Token invalid or expired (auth is via URL `?token=` only — do not pass the token in headers)
- **Subscription errors in payload**: Log the error and stop cleanly (send complete, close transport)
- **No ticks received**: Bitquery may need a moment to send the first tick; PumpFun token activity is intermittent — some tokens only trade for minutes
- **All prices showing $0.00**: Use 8 decimal places — PumpFun token prices are often `< $0.0001`

---

## Reference

Full field reference is in `references/graphql-fields.md`. Use it to add filters or request extra fields (e.g. specific token address, date range) in the subscription.
