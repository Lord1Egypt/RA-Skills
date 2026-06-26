---
name: bridge
description: Bridge or deposit USDC FROM Stellar TO another chain (Ethereum, Arbitrum, Base, BSC, Polygon, Solana) via Rozo. High-level routing — no manual smart contract calls. Triggers on "bridge to base", "deposit to ethereum", "move usdc from stellar to solana", "get my stellar usdc onto <chain>", or "i need usdc on <chain>". Delegates to Rozo's single intent API — this skill exists mostly as a semantic entry point.
---

# bridge

High-level "move my Stellar USDC to <other chain>" command. Under the hood this is the same Rozo intent API that powers `send-payment` — the difference is only intent:

- `send-payment` → sending TO someone else's address on another chain
- `bridge` → sending to **your own** address on another chain

Both map to the same Rozo `POST /payments` call. This skill exists to match natural language like "bridge" / "deposit" / "move my funds" without forcing the user to phrase it as a payment.

## When to trigger

- "Bridge 50 USDC from stellar to base"
- "Deposit my stellar USDC onto ethereum"
- "Move USDC from stellar to solana (my wallet is <addr>)"
- "I need USDC on arbitrum"
- "Get my stellar usdc onto polygon"

## Supported destinations

Same as `send-payment`:

| Chain | USDC | USDT |
|---|---|---|
| Ethereum | ✅ | ✅ |
| Arbitrum | ✅ | ✅ |
| Base | ✅ | ✅ |
| BSC | ✅ | ✅ |
| Polygon | ✅ | ✅ |
| Solana | ✅ | ❌ |

Stellar→Stellar is obviously not a bridge, so it's excluded here (use `send-payment` for that).

## Flow

1. Ask the user for their destination address on the target chain (if not given).
2. Preflight: check Stellar USDC balance with `stellar-balance`.
3. Delegate to `send-payment/run.ts` with source=stellar, dest=<chain>, to=<user's own addr>.
4. Show the Rozo payment ID + explorer links.

## How to run

```bash
# Interactive
npx tsx skills/bridge/run.ts

# Explicit
npx tsx skills/bridge/run.ts --chain base --amount 50 --my-address 0xAbCd...

# Use the same wallet secret as the source (wallet-to-wallet)
npx tsx skills/bridge/run.ts --chain base --amount 50 --my-address 0xAbCd... --yes
```

## Why this is just a thin wrapper

Rozo's intent API doesn't distinguish "bridge" from "payment". A bridge is just a payment to yourself. So this skill is a 30-line wrapper that:

1. Adds natural-language triggers for bridge-flavored prompts.
2. Makes it obvious the destination address should be **your own**, not a counterparty.
3. Shells out to `send-payment/run.ts`.

If you need more granular bridge primitives (specific routes, custom relayers), go direct to Rozo or another bridge API — this skill is deliberately opinionated.
