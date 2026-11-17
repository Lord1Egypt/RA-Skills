---
name: sol-inbound-watcher
description: Watch a Solana address for new inbound SOL/USDC transfers and alert via webhook or stdout. Use when an agent must confirm a customer paid without polling explorers by hand.
version: 0.1.0
---

# Sol Inbound Watcher

Agents sell things. Buyers pay on Solana. Then the agent needs to know **payment landed** without babysitting Solscan.

This skill is a small, local watcher: poll a public RPC, detect **new inbound** signatures above a floor, print/emit them once.

## What it does

- Polls `getSignaturesForAddress` + `getTransaction` on a public Solana RPC
- Filters **inbound** transfers to your address (lamports increase / token transfer in)
- Optional minimum amount (default 0.001 SOL)
- Dedupes by signature (state file)
- Emits JSON lines to stdout and optionally POSTs to a webhook

## What it does not do

- No custody, no private keys, no auto-spend
- No fake marketplace smoke tests
- No dependency on another agent “buying your listing”

## Install

```bash
# from this skill folder
python3 -m pip install --user httpx 2>/dev/null || true
```

## Run once (check for new payments)

```bash
python3 scripts/watch_inbound.py \
  --address YOUR_SOLANA_ADDRESS \
  --min-sol 0.001 \
  --state /tmp/sol-inbound-state.json
```

## Run loop (every 60s)

```bash
python3 scripts/watch_inbound.py \
  --address YOUR_SOLANA_ADDRESS \
  --min-sol 0.001 \
  --loop 60 \
  --webhook https://example.com/hooks/paid \
  --state ~/.openclaw/workspace/memory/sol-inbound-state.json
```

## Webhook body

```json
{
  "signature": "...",
  "slot": 123,
  "lamports": 1000000,
  "sol": 0.001,
  "from": ["..."],
  "to": "YOUR_ADDRESS",
  "blockTime": 1710000000
}
```

## Colony / workflow-seller note

If you sell this automation on a marketplace that pays in SOL, send payouts to your **proved** wallet and keep the sale signature for hand-in. This tool is the product buyers actually need after they sell anything on-chain.

## License

MIT
