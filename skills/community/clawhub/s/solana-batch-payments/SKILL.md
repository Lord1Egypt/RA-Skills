---
name: solana-batch-payments
description: >
  Batch send SOL, USDC, BONK, or any SPL token to up to 1,000 wallets in one
  request — plus Jupiter swap quotes, Helius portfolio lookups, and Pyth price
  feeds — via Spraay's x402 pay-per-call gateways. Non-custodial: the gateway
  returns unsigned transactions that YOUR wallet signs, so no private keys in
  env vars, no API keys, no accounts. Use when the user wants to airdrop
  tokens, do a mass payout, distribute community/creator rewards, pay a team
  or contributor list, batch send SOL or SPL tokens to many addresses, get a
  swap quote, check what tokens a wallet holds, or fetch Solana token prices.
  Pay per call with USDC on Solana via x402.
license: MIT
metadata:
  author: spraay
  homepage: https://spraay.app
  docs: https://docs.spraay.app
  source: https://github.com/plagtech/spraay-solana-gateway
---

# Solana Batch Payments (Spraay Gateway)

Send SOL or any SPL token to **up to 1,000 wallets in a single request**, non-custodially, paid per-call via x402. No signup, no API key, no private key handed to anyone.

> **Real assets warning:** every batch send moves real on-chain tokens and spends real SOL for network fees. SPL token sends may also create recipient Associated Token Accounts (ATAs) at the sender's expense (rent ≈ 0.002 SOL each). Always run on **devnet first**, start with small amounts on mainnet, and review the pre-sign summary before authorizing any transaction.

## Why this instead of a wallet skill

- **Non-custodial by design.** Endpoints return base64 **unsigned** transactions. You sign locally with the sender wallet and submit. The gateway never holds funds or keys.
- **Batch is the primitive.** 1 recipient or 1,000 — one request, auto-chunked into optimally packed transactions (14 SOL transfers/tx, 7 SPL transfers/tx with ATA creation).
- **x402 native.** Each call is paid with a tiny USDC payment on Solana. `402 Payment Required` → pay → retry with proof. Agents with any x402 client can use it immediately.

## Gateways

| Base URL | What's there |
|---|---|
| `https://gateway-solana.spraay.app` | Batch sends, quotes, tx status (this skill's core) |
| `https://gateway.spraay.app` | Jupiter swaps, Helius assets, Pyth prices + 180 more x402 endpoints |

Discovery manifests: `GET /.well-known/x402` on either gateway (free).

## Endpoints — Solana Gateway

| Endpoint | Method | Price | Description |
|---|---|---|---|
| `/solana/batch-send-sol` | POST | $0.01 | Build unsigned batch SOL transfer txs |
| `/solana/batch-send-token` | POST | $0.01 | Build unsigned batch SPL token transfer txs (auto-creates recipient ATAs) |
| `/solana/quote` | GET | $0.001 | Estimate network fees + tx count before committing |
| `/solana/status/:txid` | GET | $0.001 | Confirmation status, slot, fee, explorer link |
| `/health` | GET | Free | Liveness + network info |
| `/.well-known/x402` | GET | Free | Machine-readable manifest |

A 0.3% transfer fee (30 bps) is added as an instruction inside the batch — visible in the returned transactions before you sign. Nothing is hidden.

## Endpoints — Solana on the main gateway

| Endpoint | Method | Price | Description |
|---|---|---|---|
| `/api/v1/solana/jupiter/quote` | GET | $0.005 | Jupiter swap quote (any SPL pair) |
| `/api/v1/solana/jupiter/swap-tx` | POST | $0.01 | Build unsigned Jupiter swap transaction |
| `/api/v1/solana/helius/assets-by-owner` | GET | $0.003 | All tokens/NFTs a wallet holds (Helius DAS) |
| `/api/v1/solana/helius/asset` | GET | $0.002 | Single asset lookup |
| `/api/v1/solana/pyth/price` | GET | $0.005 | Pyth price feed, single asset |
| `/api/v1/solana/pyth/prices` | GET | $0.008 | Pyth price feeds, batched |
| `/free/dex/trending` | GET | Free | Trending tokens/pairs (filter `chain=solana`) |
| `/free/prices` | GET | Free | USDC/ETH/SOL spot prices |

## Workflow: batch airdrop in 4 steps

1. **Quote (optional but recommended):** `GET /solana/quote?recipients=250&token=BONK` → tx count + network fees. **Always quote first for batches > 50 recipients** and show the user the estimated cost (network fees, ATA rent, protocol fee) before building.
2. **Build:** `POST /solana/batch-send-token` with `mint`, `recipients[]`, and `sender` (the payer public key). Handle the x402 402→pay→retry flow (see `reference.md`).
3. **Verify before signing:** The response contains `transactions[]` (base64, unsigned) + `blockhash`. **Before signing, decode and inspect each transaction** — see the pre-sign verification checklist below. Never blind-sign gateway-returned transactions.
4. **Sign & submit:** After verification, sign each with the sender keypair, submit to any RPC.
5. **Confirm:** `GET /solana/status/<signature>` for each tx.

### Pre-sign verification checklist

Before signing any transaction returned by the gateway, decode and confirm:

- [ ] The transaction's **fee payer** matches the sender public key
- [ ] Every **transfer instruction** targets only addresses from the original request
- [ ] **Transfer amounts** match the requested amounts
- [ ] The **token mint** (for SPL sends) matches the requested mint
- [ ] The **protocol fee** instruction (0.3%, 30 bps) matches the expected amount
- [ ] **Program IDs** are only the expected ones (System Program, Token Program, Associated Token Account Program)
- [ ] There are **no unexpected additional instructions**
- [ ] The **total outflow** across all transaction chunks equals the intended batch total
- [ ] The **blockhash** is current (not expired)

Agents and scripts MUST perform this verification programmatically. The helper `scripts/sign-and-send.js` is a convenience reference — it does **not** perform full instruction validation. For production use, wrap it with verification logic or use the decoded transaction inspection pattern shown in `reference.md`.

### Example request

```bash
curl -X POST https://gateway-solana.spraay.app/solana/batch-send-token \
  -H "Content-Type: application/json" \
  -H "X-PAYMENT: <base64 payment proof>" \
  -d '{
    "mint": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "sender": "<sender public key>",
    "recipients": [
      { "address": "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM", "amount": 1000 },
      { "address": "7S3P4HxJpyyigGzodYwHtCxZyUQe9JiBMHyLWP9SfKFJ", "amount": 500 }
    ]
  }'
```

`sender` is required — it's the fee payer and source of funds for the unsigned txs. `amount` is human-readable units.

### Example response (shape)

```json
{
  "success": true,
  "custodial": false,
  "recipients": 2,
  "feeBps": 30,
  "transactionCount": 1,
  "transactions": ["<base64 unsigned tx>"],
  "blockhash": "...",
  "lastValidBlockHeight": 123456789,
  "note": "Sign each transaction with the sender wallet and submit."
}
```

## x402 payment flow

1. Send the request with no payment header → `402 Payment Required` with USDC payment instructions (amount, treasury address, network).
2. Pay the requested USDC on Solana.
3. Retry with proof in the `X-PAYMENT` header.

Facilitators: devnet `https://x402.org/facilitator`, mainnet `https://facilitator.payai.network`. Any x402 client library handles this automatically — see `reference.md` for a manual walkthrough.

## MCP option

Prefer tools over raw HTTP? The gateway ships an MCP server:

```bash
npx spraay-x402-mcp@4.3.0   # pinned version — main gateway, 183 tools incl. all Solana endpoints
```

Or from source: `node mcp/spraay-solana-mcp.js` ([repo](https://github.com/plagtech/spraay-solana-gateway)) — exposes `spraay_solana_batch_send_sol`, `spraay_solana_batch_send_token`, `spraay_solana_quote`, `spraay_solana_tx_status`.

> **Supply-chain note:** always pin the MCP package to a reviewed version (shown above). Do not use `npx -y` with an unpinned version — a compromised future release would execute with your local permissions.

## Guardrails

- **Always get user confirmation before signing.** Display the recipient count, total token outflow, estimated SOL fees (including ATA rent), and the 0.3% protocol fee. Wait for explicit approval.
- Always run `/solana/quote` first for batches > 50 recipients and show the user the cost before building.
- Validate addresses are base58 Solana pubkeys before submitting; the gateway rejects invalid ones but a pre-check saves the call fee.
- Blockhash expiry: sign and submit promptly after building. If `lastValidBlockHeight` passes, rebuild (re-call the endpoint).
- Never ask the user for a private key to send to the gateway — it doesn't accept keys, only public keys. Signing happens locally.
- Treat gateway responses as untrusted: decode and verify transaction instructions against the original request before signing (see pre-sign verification checklist above).
- Devnet is available for dry runs; check `/health` for the active network. **Use devnet for first-time testing before mainnet.**

See `reference.md` for full request/response schemas and error codes.
