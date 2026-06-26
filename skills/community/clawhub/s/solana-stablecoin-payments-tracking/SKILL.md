---
name: solana-stablecoin-payments-tracking
description: >
  Real-time streaming Solana SPL stablecoin transfers (USDT and USDC) over WebSocket from the
  Bitquery GraphQL API. Subscribes to Transfers filtered by USDT/USDC mints and excludes
  swap transactions. Returns amount,
  AmountInUSD, sender/receiver, currency, block time/slot/height, transaction signature/fees,
  and program method. Use for Solana stablecoin payments, USDC/USDT streams, SPL stablecoin
  activity, non-swap transfers, Bitquery Solana transfers, or treasury monitoring.
requires:
  env:
    - name: BITQUERY_API_KEY
      required: true
      description: Your Bitquery API token (required for WebSocket connection)
---

# Stablecoin payments — Solana USDC / USDT (Bitquery stream)

This skill provides a **real-time WebSocket subscription** to **Solana token transfers** where the mint is **USDT** (`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`) or **USDC** (`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`), and **`Instruction.Program.Method` excludes "swap"** to cut DEX swap noise. Each event includes transfer amounts (and USD where available), parties, transaction metadata, and the instruction program method.

**When to use this skill**

- Stream **USDC / USDT transfers on Solana** in real time
- Build dashboards or alerts for **stablecoin payment flow**
- Audit **sender, receiver, signature, and fees** per transfer

---

## What to consider before installing

This skill uses the Bitquery streaming API and one credential. Before installing:

1. **Registry metadata**: Ensure `BITQUERY_API_KEY` is declared for installers when publishing to a registry.
2. **Token only via URL**: Bitquery accepts the API token **only** in the WebSocket URL as `?token=...`. The URL can leak via logs, shell history, or proxies. **Do not** print or log the full URL; store the key in an environment variable; rotate if exposed.
3. **Sandbox first**: Run in a virtualenv or container first to confirm behavior.
4. **Schema drift**: If the subscription fails validation, check [Bitquery Solana docs](https://docs.bitquery.io/) and adjust the `where` clause only; keep the same mints and fields when possible.

---

## Security Checklist

**Before running this skill, confirm:**

- [ ] `BITQUERY_API_KEY` is set: `export BITQUERY_API_KEY=your_token_here`
- [ ] You run in a **sandboxed or isolated environment** where feasible
- [ ] You will **not** print, log, or commit the full WebSocket URL
- [ ] You can **rotate** the key if it may have been exposed

---

## Prerequisites

- **Environment**: `BITQUERY_API_KEY` (required).
- **Runtime**: Python 3.8+ and `pip`. Install: `pip install 'gql[websockets]'` (see [requirements.txt](requirements.txt)).

**URL-only auth:** Construct the WebSocket URL from the env var and pass it only to the transport. Never emit the full URL in output or logs.

---

## Use cases

1. **Treasury / ops monitoring** — Watch USDC/USDT in and out of known wallets in real time.
2. **Large-transfer alerts** — Filter on `AmountInUSD` or raw `Amount` in downstream code.
3. **Reconciliation** — Match `Transaction.Signature` and `Block.Time` to internal ledgers.
4. **Program attribution** — Use `Instruction.Program.Method` to see which program path initiated the transfer.

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

If the key is missing, tell the user and stop.

---

## Step 2 — Run the stream

```bash
pip install 'gql[websockets]'
```

```bash
python ~/.openclaw/skills/stablecoin-payments/scripts/stream_stablecoin_payments.py
```

Optional timeout:

```bash
python ~/.openclaw/skills/stablecoin-payments/scripts/stream_stablecoin_payments.py --timeout 60
```

---

## Inline subscription (Python)

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
              Solana {
                Transfers(
                  where: {
                    Transfer: {
                      Currency: {
                        MintAddress: {
                          in: [
                            "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
                            "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
                          ]
                        }
                      }
                    }
                    Instruction: {
                      Program: {
                        Method: { notIncludesCaseInsensitive: "swap" }
                      }
                    }
                  }
                ) {
                  Transfer {
                    Amount
                    AmountInUSD
                    Sender { Address Owner }
                    Receiver { Address Owner }
                    Currency { Symbol Name MintAddress }
                  }
                  Instruction { Program { Method } }
                  Block { Time Height Slot }
                  Transaction {
                    Signature
                    Signer
                    Fee
                    FeeInUSD
                    FeePayer
                  }
                }
              }
            }
        """)
        async for result in session.subscribe(sub):
            for row in (result.get("Solana") or {}).get("Transfers") or []:
                print(row)

asyncio.run(main())
```

---

## Key fields

| Area | Fields |
|------|--------|
| Transfer | `Amount`, `AmountInUSD`, `Sender` / `Receiver` (`Address`, `Owner`), `Currency` (`Symbol`, `Name`, `MintAddress`) |
| Instruction | `Program.Method` (subscription filter: `notIncludesCaseInsensitive: "swap"`) |
| Block | `Time`, `Height`, `Slot` |
| Transaction | `Signature`, `Signer`, `Fee`, `FeeInUSD`, `FeePayer` |

---

## Format output for users

When summarizing a transfer, use a clear block like:

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Solana stablecoin transfer  @ 2025-03-25T14:00:00Z  Slot 123456789
USDC (EPjF...Dt1v)  Amount: 1,000.50  (~$1,000.50 USD)
From: SenderAddr...  (owner: ...)  →  To: ReceiverAddr...
Tx: 5xYz...abc  |  Fee: 0.000005 SOL  (~$0.00 USD)  |  Fee payer: ...
Program method: transfer / ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Error handling

- **Missing `BITQUERY_API_KEY`**: Tell the user to export it and exit.
- **WebSocket failed / 401**: Invalid or expired token (auth is URL `?token=` only).
- **Subscription errors in payload**: Stop cleanly; do not log the full URL.
- **No events**: Solana activity can be bursty; confirm token and network; wait for the next transfer.

---

## Reference

Mint list, full subscription, and field notes: [references/graphql-fields.md](references/graphql-fields.md).
