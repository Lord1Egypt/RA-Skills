---
name: send-payment
description: Send a cross-chain payment FROM Stellar USDC TO any supported destination chain (Ethereum, Arbitrum, Base, BSC, Polygon, Solana, Stellar) via the Rozo intent API at intentapiv4.rozo.ai. Triggers on "send payment", "pay 0x...", "transfer USDC to <address>", "pay user on base", "payout to eth", or when the user shares a destination wallet address with an amount and chain. Source is always Stellar USDC from this wallet. Script creates the Rozo intent, then submits a Classic USDC payment to the returned deposit address.
---

# send-payment

High-level cross-chain payment from Stellar USDC. Uses Rozo's intent API so one call handles bridging, routing, and settlement.

## When to trigger

- "Send 10 USDC to 0xABCD... on base"
- "Pay this Solana address 5 USDC"
- "Transfer to G... on stellar"
- "Payout 50 USDC to <address> on ethereum"
- User pastes a destination address + amount + chain

## Not for

- Pay-per-call 402 flows — use `pay-per-call` sub-skill.
- Balance check before sending — use `stellar-balance` sub-skill first.
- Same-chain Stellar-to-Stellar **without** cross-chain routing — it works, but a direct Classic USDC payment is cheaper and simpler; use `@stellar/stellar-sdk` directly.

## Supported destinations (verified against Rozo spec)

Source is always **Stellar USDC**. Destinations + chain IDs:

| Chain | Chain ID | USDC | USDT |
|---|---|---|---|
| Ethereum | 1 | ✅ | ✅ |
| Arbitrum | 42161 | ✅ | ✅ |
| Base | 8453 | ✅ | ✅ |
| BSC (BNB Chain) | 56 | ✅ | ✅ |
| Polygon | 137 | ✅ | ✅ |
| Solana | 900 | ✅ | ❌ |
| Stellar | 1500 | ✅ | ❌ |

Stellar pay-in decimals: 7. BSC USDC/USDT: 18. All others: 6.

Amount limits: **$0.01 min, $10,000 max** per transaction. Rozo enforces these server-side — the script validates client-side before POSTing.

## Address detection (before running)

When the user shares an address, detect the chain format:

| Pattern | Chain | Action |
|---|---|---|
| `0x` + 40 hex | EVM — ambiguous | **Must ask which chain**: Ethereum / Arbitrum / Base / BSC / Polygon |
| Base58, 32-44 chars, no `0x` | Solana | Auto |
| `G...`, 56 chars, Base32 | Stellar G-wallet | Auto + **check USDC trustline first** |
| `C...`, 56 chars, Base32 | Stellar C-wallet (Soroban contract) | Different flow — use `stellar_payin_contracts` intent, recipient invokes contract `pay()` |

If Stellar C-wallet: the Rozo response will include `receiverAddressContract` and `receiverMemoContract`. Do NOT submit a Classic payment — the recipient must call the contract's `pay()` function with the amount and memo.

## Flow (what the script does)

1. **Validate** destination chain + token compatibility.
2. **POST** `/functions/v1/payment-api/` with `type: exactOut`, source=stellar USDC, destination=chosen chain/token/address.
3. **Receive** Rozo response: payment ID, deposit address (Stellar G-wallet owned by Rozo), memo (required for deposit), fee.
4. **Show quote** — total source amount (destination + fee), fee, expiration, deposit address.
5. **Confirm** — prompts user unless `--yes` passed.
6. **Submit Stellar Classic USDC payment** to Rozo's deposit address with the required memo. This is the step that actually moves money.
7. **Print Stellar tx hash + payment ID + explorer links**, plus the `status.ts` command to poll.

## How to run

```bash
# Standard: pay $10 USDC on Base to an EVM address
npx tsx skills/send-payment/run.ts \
  --to 0xAbCdEf1234567890AbCdEf1234567890AbCdEf12 \
  --chain base \
  --token USDC \
  --amount 10.00

# USDT on Arbitrum
npx tsx skills/send-payment/run.ts \
  --to 0x... --chain arbitrum --token USDT --amount 25.00

# To a Stellar G-wallet with trustline
npx tsx skills/send-payment/run.ts \
  --to GC56BX... --chain stellar --token USDC --amount 5.00

# With custom title/description shown in Rozo receipt
npx tsx skills/send-payment/run.ts \
  --to 0x... --chain base --amount 1.00 \
  --title "Invoice #123" --description "Monthly subscription"

# Skip confirmation (use with care — large-amount gate still fires)
npx tsx skills/send-payment/run.ts --to ... --chain base --amount 0.50 --yes

# Idempotent retry with custom orderId
npx tsx skills/send-payment/run.ts --to ... --chain base --amount 10 --order-id my-unique-id
```

## Check status

```bash
# One-shot
npx tsx skills/send-payment/status.ts <payment-id>

# Watch mode — polls every 5s until terminal
npx tsx skills/send-payment/status.ts <payment-id> --watch
```

Terminal statuses:
- `payment_completed` — ✅ success
- `payment_bounced` — ❌ payout failed (bad dest address?)
- `payment_expired` — ⏱ not funded in time
- `payment_refunded` — ↩ funds returned

## Safety rules (enforced by the script)

- ✅ **Mainnet required** — Rozo operates on pubnet only. Script errors out if `--network testnet`.
- ✅ **Confirmation by default** — must pass `--yes` to skip the prompt.
- ✅ **Amount range enforcement** — script rejects < $0.01 or > $10,000 before posting.
- ✅ **Pay-out validation** — USDT on Solana/Stellar is rejected client-side with a clear error.
- ❌ **Do not retry on unclear failure** — if the Rozo create fails after the Stellar payment is submitted, don't re-post. Look up the payment by tx hash: `GET /payments/check?txHash=<stellar-hash>` (via a future helper).
- ❌ **Never skip the memo** — Rozo deposit addresses are shared; the memo is how your payment gets routed to your order. Missing memo = lost funds.

## API reference

From `/Users/happyfish/workspace/agenttools/rozo-intents-skills/references/api-reference.md`:

- **Base URL**: `https://intentapiv4.rozo.ai/functions/v1/payment-api`
- **Auth**: none (public, rate-limited)
- **Create payment**: `POST /` (note the trailing slash)
- **Get payment**: `GET /payments/{id}`
- **Check by source**: `GET /payments/check?txHash=...` or `?receiverAddress=...&receiverMemo=...`

Request body is fixed to `appId: "rozoAgent"`. `type: "exactOut"` means the recipient gets exactly the amount you specified and the fee is added on top to the source amount.

## Flags

Pass on the command line (no env vars, no .env files):

```
--identity <name>          existing Stellar CLI identity to use for signing
--secret-file <path>       path to Stellar secret file (default: .stellar-secret)
--network <pubnet>         required: must be pubnet; testnet errors out
--horizon-url <url>        optional Horizon override (default: https://horizon.stellar.org)
```

The Rozo API base URL is hardcoded in `scripts/src/rozo-client.ts` — no override.
