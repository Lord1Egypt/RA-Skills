---
name: vaunt-signals
description: Real-money trading evidence from a live Hyperliquid engine, pay-per-call in USDC on Base via x402. Ask "is this a buy right now?" and get BUY or NO with a buy price and a sell price from Vaunt's live real-money strategies, get evidence for or against your own trade, see what a trade actually costs to execute, and check the free answer key afterwards. No account, no API key.
version: 1.0.0
homepage: https://vaunt-dispatch-production.up.railway.app/agent
tags: [trading, crypto, hyperliquid, x402, signals, evidence, execution]
---

# Vaunt signals (x402, USDC on Base)

Vaunt runs real money on Hyperliquid and records every outcome. These routes sell the RESULTS —
never the rules. Every paid call is one HTTP request with an x402 payment header; any x402 client
(`@x402/fetch`, `@coinbase/cdp-sdk/x402`, `x402-python`) does the payment in one round trip. The
first call without payment returns HTTP 402 with the price, the input schema and an example output.

Base URL: `https://vaunt-dispatch-production.up.railway.app`

## When to use which route

| You want to know | Route | Price |
|---|---|---|
| **Is this a buy right now?** BUY or NO + buy price + sell price for ASSET, from Vaunt's live real-money strategies | `POST /agent/x402/ask` `{asset}` | $0.50 |
| What will a trade on ASSET cost me on Hyperliquid (slippage, fee, latency, depth)? | `GET /agent/x402/cost/<ASSET>` | $0.001 |
| Did the last two weeks of signals actually pay? (the answer key) | `GET /agent/scorecard` | free |
| Evidence for or against MY trade (asset + LONG/SHORT) | `POST /agent/x402/evaluate` `{asset, direction, horizon_h}` | $0.50 |
| Same, plus the asset's own trade history, execution cost and liquidity | `POST /agent/x402/evidence` | $1.00 |
| Just the label (STRONG/MODERATE/WEAK/AGAINST) | `POST /agent/x402/preview` | $0.001 |

`<ASSET>` is a Hyperliquid ticker: `BTC ETH SOL HYPE XRP DOGE SUI LINK ARB` or a tokenized equity
written as `xyz-NVDA xyz-TSLA xyz-COIN`.

## Free, no payment

- `GET /agent` — manifest with every route and price
- `GET /agent/evidence` — per-strategy live record (n, independent days, mean, win, hold)
- `GET /agent/sample` — ten closed trades with context
- `GET /agent/venues` — execution quality per venue class
- `GET /agent/scorecard` — the answer key: every position the live routes showed in the last 14 days
  with its outcome, plus the weekly and per-lane record. Free so it can be checked, not trusted.

## Reading the answer

- `support`: STRONG / MODERATE / WEAK / AGAINST / UNKNOWN — the basis is in `basis[]`.
- `cell_evidence.verdict`: VALIDATED needs 20+ independent days and t ≥ 2; UNDECIDED means the
  record is real but short. Read the label before the rank.
- `holding_now.yes`: Vaunt's own money is in it, shown 60 minutes after entry.
- Returns are per trade, net of fees, on notional. Independent days, not rows, are the sample size.

## What is never returned

Entry, invalidation, exit geometry, size, or the thresholds that define a cell. If you need those,
this is not the product.

## Example (Node)

```js
import { wrapFetchWithPayment } from '@x402/fetch';
const pay = wrapFetchWithPayment(fetch, client); // any x402 client with a Base USDC signer
const r = await pay('https://vaunt-dispatch-production.up.railway.app/agent/x402/ask', { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ asset: 'SOL' }) });
const a = await r.json();
console.log(a.answer, a.buy_price, a.sell_price, a.why, a.last_14_days);   // 'BUY' 117.65 119.41 …
```
