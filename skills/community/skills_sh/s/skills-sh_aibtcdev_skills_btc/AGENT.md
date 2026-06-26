---
name: btc-agent
skill: btc
description: Bitcoin L1 operations — check balances, estimate fees, list UTXOs, transfer BTC, and classify UTXOs as cardinal or ordinal to avoid accidentally spending inscriptions.
---

# BTC Agent

This agent handles Bitcoin L1 operations using mempool.space for balance and fee data, and the Hiro Ordinals API for cardinal/ordinal UTXO classification on mainnet. Balance and fee queries require no wallet. Transfer operations require an unlocked wallet.

## Prerequisites

- Wallet must be unlocked before running `transfer` — use `bun run wallet/wallet.ts unlock --password <password>` first
- Balance, fees, utxos, get-cardinal-utxos, get-ordinal-utxos, and get-inscriptions work without a wallet if `--address` is provided
- `get-cardinal-utxos`, `get-ordinal-utxos`, and `get-inscriptions` are mainnet-only (Hiro Ordinals API does not index testnet)

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Check BTC balance for active wallet or any address | `balance` — returns total, confirmed, unconfirmed |
| Get current fee estimates before sending | `fees` — returns fast/medium/slow/economy/minimum sat/vB |
| List all UTXOs for an address | `utxos` — use `--confirmed-only` to skip mempool entries |
| List only safe-to-spend UTXOs (no inscriptions) | `get-cardinal-utxos` — mainnet only |
| List UTXOs containing inscriptions (do not spend) | `get-ordinal-utxos` — mainnet only |
| List all inscriptions owned by an address | `get-inscriptions` — mainnet only |
| Send BTC to a recipient address | `transfer` — cardinal-only by default; requires unlocked wallet |

## Safety Checks

- Before `transfer`: run `balance` to confirm sufficient funds (amount + estimated fee)
- Before `transfer`: run `get-cardinal-utxos` on mainnet to confirm cardinal UTXOs exist
- On mainnet, `transfer` uses cardinal UTXOs only by default — do not pass `--include-ordinals` unless you intend to risk inscription loss
- On testnet, ordinal protection is unavailable — all UTXOs may be spent
- Verify recipient address format before sending (bc1q.../bc1p... for mainnet, tb1... for testnet)
- Fees are denominated in satoshis — confirm `--amount` is satoshis, not BTC

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No Bitcoin address provided and wallet is not unlocked" | No `--address` flag and wallet is locked | Provide `--address` or unlock wallet first |
| "Wallet is not unlocked. Use wallet/wallet.ts unlock first." | `transfer` called without unlocked wallet | Run `bun run wallet/wallet.ts unlock --password <password>` |
| "Bitcoin keys not available. Please unlock your wallet again." | Session expired or wallet missing BTC keys | Unlock wallet again |
| "No cardinal UTXOs available for address..." | All UTXOs contain inscriptions | Either use `--include-ordinals` (risks inscription loss) or move inscriptions first |
| "No UTXOs found for address..." | Address has no BTC balance | Fund the address before transferring |
| "--amount must be a positive integer (satoshis)" | Non-numeric or zero amount passed | Pass a positive integer representing satoshis |
| "--fee-rate must be 'fast', 'medium', 'slow', or a positive integer" | Invalid fee-rate value | Use one of the named tiers or a positive integer |

## Output Handling

- `balance`: use `balance.satoshis` for math, `balance.btc` for display, `utxoCount` for UTXO-aware decisions
- `fees`: use `fees.medium.satPerVb` as the default; `fees.fast.satPerVb` for urgent transactions
- `utxos`: pass `utxos[].txid` and `utxos[].vout` to transaction builders; filter by `confirmed: true` before spending
- `get-cardinal-utxos`: `summary.count` tells you how many safe UTXOs exist; `summary.totalValue.satoshis` for available spend amount
- `get-ordinal-utxos`: do not spend these UTXOs in regular transfers; pass `utxos[].txid` to ordinals-p2p when trading
- `get-inscriptions`: use `inscriptions[].id` (format: `{txid}i0`) for ordinals-p2p trading operations
- `transfer`: save `txid` for tracking; `explorerUrl` for confirmation; `transaction.fee.satoshis` for accounting

## Example Invocations

```bash
# Check BTC balance for the active wallet
bun run btc/btc.ts balance

# List cardinal (safe-to-spend) UTXOs on mainnet
bun run btc/btc.ts get-cardinal-utxos --address bc1q...

# Transfer BTC with medium fee rate (cardinal UTXOs only)
bun run btc/btc.ts transfer --recipient bc1q... --amount 100000 --fee-rate medium
```
