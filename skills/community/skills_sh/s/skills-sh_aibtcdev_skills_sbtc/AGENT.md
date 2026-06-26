---
name: sbtc-agent
skill: sbtc
description: sBTC operations on Stacks L2 — check balances, transfer sBTC, deposit BTC to receive sBTC, track deposit status, and query peg statistics.
---

# sBTC Agent

This agent handles sBTC (wrapped Bitcoin on Stacks L2) operations. sBTC is pegged 1:1 to BTC and uses 8 decimal places (same as Bitcoin satoshis). Balance and info queries work without a wallet. Transfer and deposit operations require an unlocked wallet.

## Prerequisites

- Wallet must be unlocked before `transfer` or `deposit` operations: `bun run wallet/wallet.ts unlock --password <password>`
- The `deposit` subcommand requires Bitcoin in the wallet's BTC address — check with `bun run btc/btc.ts balance`
- The `deposit` subcommand requires Taproot keys — these are present when a wallet is created via the `wallet` skill
- `get-balance`, `get-deposit-info`, `get-peg-info`, and `deposit-status` work without a wallet

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Check sBTC balance for active wallet or any address | `get-balance` — pass `--address` to check any address |
| Send sBTC to another Stacks address | `transfer` — specify `--recipient` and `--amount` in satoshis |
| View personalized deposit address or general instructions | `get-deposit-info` — returns personalized address if wallet is unlocked |
| Check total sBTC supply and peg statistics | `get-peg-info` — no arguments needed |
| Bridge BTC from Bitcoin L1 to sBTC on Stacks L2 | `deposit` — builds and broadcasts the Bitcoin transaction automatically |
| Check whether a pending deposit has been processed | `deposit-status` — pass the Bitcoin `--txid` from the deposit |

## Safety Checks

- Before `transfer`: confirm the recipient address is a valid Stacks address and the amount (in satoshis) is correct — sBTC uses 8 decimals, so 1 sBTC = 100,000,000 satoshis
- Before `deposit`: verify you have sufficient BTC with `bun run btc/btc.ts balance`; the deposit will also spend BTC for the Bitcoin network fee on top of the deposit amount
- Before `deposit`: check UTXO safety with `bun run btc/btc.ts get-cardinal-utxos` — the `deposit` command defaults to cardinal-only UTXOs; do NOT pass `--include-ordinals` unless you are certain none of your UTXOs hold valuable inscriptions
- `deposit` is a cross-layer operation: Bitcoin confirmations are required before sBTC appears on Stacks; use `deposit-status` to track progress
- sBTC transfers are irreversible — double-check the recipient address before broadcasting

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "Wallet is not unlocked" | `transfer` or `deposit` called without unlocked wallet | Run `bun run wallet/wallet.ts unlock --password <password>` |
| "Bitcoin or Taproot keys not available" | Wallet unlocked but missing BTC/Taproot key derivation | Re-unlock the wallet; if the issue persists, the wallet may not support Taproot |
| "--amount must be a positive integer (satoshis)" | Non-numeric or zero amount passed to `transfer` or `deposit` | Pass a positive integer for satoshis (e.g., `100000` for 0.001 sBTC/BTC) |
| "--fee-rate must be 'fast', 'medium', 'slow', or a positive integer" | Invalid `--fee-rate` value passed to `deposit` | Use `fast`, `medium`, `slow`, or a numeric sat/vB value |
| "Deposit not found in Emily API" | `deposit-status` called before the deposit is indexed | Wait for Bitcoin confirmation and retry; the TX may not be a valid sBTC deposit |
| "No active wallet" | `get-balance` called with no address and no active wallet | Pass `--address <stacks-address>` or unlock a wallet first |

## Output Handling

- `get-balance`: read `balance.sats` for raw satoshi amount; `balance.btc` for human-readable display; `address` for which address was checked
- `transfer`: on success, `txid` is the Stacks transaction ID; `explorerUrl` links to the Hiro explorer; pass `txid` to downstream status checks
- `get-deposit-info`: when wallet is unlocked, `depositAddress` is the personalized Bitcoin address to send BTC to; `stacksAddress` is where sBTC will be minted
- `get-peg-info`: `totalSupply.sats` is the total sBTC in circulation; `pegRatio` should be close to `1.000000`
- `deposit`: on success, `txid` is the Bitcoin transaction ID; `explorerUrl` links to mempool.space; save `txid` to check with `deposit-status` later
- `deposit-status`: `status` values are `pending`, `accepted`, `confirmed`, or `not_found`; retry if `pending`; `not_found` means the deposit is not yet indexed or is invalid

## Example Invocations

```bash
# Check sBTC balance for the active wallet
bun run sbtc/sbtc.ts get-balance

# Transfer 0.001 sBTC (100000 satoshis) to another Stacks address
bun run sbtc/sbtc.ts transfer --recipient SP3FGQ8Z7JY9BWYZ5WM53E0M9NK7WHJF4691NHN0X --amount 100000

# Deposit 0.001 BTC to receive sBTC (uses medium fee rate, cardinal UTXOs only)
bun run sbtc/sbtc.ts deposit --amount 100000

# Check status of a pending deposit
bun run sbtc/sbtc.ts deposit-status --txid <bitcoin-txid>
```
