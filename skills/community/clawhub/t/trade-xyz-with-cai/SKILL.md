---
name: trade-xyz-with-cai
description: Trade HIP-3 markets on trade.xyz via CAI — same Hyperliquid Route B tools (defi_trade, defi_orders) with xyz:SYMBOL assets and dex param. No trade.xyz signup. Requires platform or full API scope. Powered by CAI.com. v1.0.15.
metadata:
  version: 1.0.15
---

# trade.xyz (HIP-3) with CAI

**trade.xyz** is a Hyperliquid **HIP-3** frontend. CAI does **not** require a separate trade.xyz account. Use the same custodial HL stack as **hyperliquid-with-cai**: `platform_slug=hyperliquid`, Route B **`defi_trade`** / **`defi_orders`** / **`defi_positions`**.

## When to Use

- "Buy NVDA perp on trade.xyz with my CAI wallet"
- "Trade HIP-3 xyz markets via CAI"
- "Place an xyz:SYMBOL order on Hyperliquid builder markets"

## Route B task flow

Follow **hyperliquid-with-cai** enrollment and readiness, then:

1. **`defi_trade`** place example:
   - `platform_slug`: `hyperliquid`
   - `action`: `place`
   - `asset`: `xyz:NVDA` (builder symbol)
   - `size`, `price`, `is_buy`, `intent_usd`
   - optional `dex`: `xyz` when required by deployment
2. **Status:** **`defi_orders`** / **`defi_positions`** with `platform_slug=hyperliquid`.
3. **Cancel:** **`defi_trade`** with `action`: `cancel`, `oid`, `asset` (e.g. `xyz:NVDA`).

## Related wrapper

For general HL perps (BTC, ETH), install or reference **hyperliquid-with-cai**.

## Honesty

- **`GAP_DEFI_HYPERLIQUID_V1`** — **`partial_live`**
- No trade.xyz website registration narrative — same as HL: custodial address + agent approval only.

## Quick Setup

```bash
openclaw secrets set CAI_API_KEY "your_dashboard_api_key"
```

## Canonical Reference

- https://cai.com/skill.md §6.1b
- https://docs.trade.xyz/about-trade-xyz/hyperliquid-xyz-and-hip-3
- https://cai.com/developers.html
