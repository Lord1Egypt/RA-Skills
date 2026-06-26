---
name: stellar-balance
description: Manage a Stellar account's balance — check USDC/XLM, add a Classic USDC trustline, or swap XLM to USDC on the DEX. Stellar-only (does NOT do cross-chain balances — use the bridge skill for that). Triggers on "check balance", "how much USDC do I have", "add usdc trustline", "swap xlm to usdc", "i need usdc on stellar", "my account doesn't have usdc yet", or when the user pastes a G... address.
---

# stellar-balance

Stellar account management for the wallet agent. Three scripts, one skill.

| Script | When |
|---|---|
| `run.ts` | Check USDC + XLM on an account |
| `add-trustline.ts` | Enable Classic USDC (required before receiving from external wallets or swapping on DEX) |
| `swap-xlm-to-usdc.ts` | Convert XLM to USDC via the Stellar Classic DEX (path payment) |

## When to trigger

- "check my stellar balance" → `run.ts`
- "how much USDC do I have on stellar" → `run.ts`
- "add usdc trustline" / "i need usdc on stellar but have none" → `add-trustline.ts`
- "swap xlm to usdc" / "convert my xlm to usdc" → `swap-xlm-to-usdc.ts`
- User pastes a `G...` address with no other context → `run.ts`

## Not for

- EVM / Solana / multi-chain balances — route to `bridge` sub-skill (Rozo).
- SAC token balances for arbitrary contracts — this skill only knows USDC and XLM.
- Buying USDC with fiat — use an on-ramp (Coinbase, MoonPay, etc.).

## Typical onboarding flow

When a user's Stellar account is brand new and has only XLM:

```bash
# 1. See what's there
npx tsx skills/check-balance/run.ts

# 2. Enable USDC
npx tsx skills/check-balance/add-trustline.ts

# 3. Swap XLM → USDC (example: swap 10 XLM)
npx tsx skills/check-balance/swap-xlm-to-usdc.ts 10

# 4. Verify
npx tsx skills/check-balance/run.ts
```

## Commands

### check balance

```bash
# Derive pubkey from --identity or --secret-file (default: .stellar-secret)
npx tsx skills/check-balance/run.ts

# Use an existing Stellar CLI identity
npx tsx skills/check-balance/run.ts --identity mpp-mainnet-payer

# Check any pubkey
npx tsx skills/check-balance/run.ts GABCD...

# JSON output
npx tsx skills/check-balance/run.ts --json
```

Output:
```
Account: GABCD...
Network: pubnet

  USDC   42.5000000    (Classic)
  USDC    8.1234567    (SAC — Soroban)
  XLM   125.0000000    (native)

Reserves: 2.0 XLM
Spendable XLM: 123.0000000
```

Reads from Horizon (Classic balances + reserves) and Soroban RPC (SAC balance via contract simulation).

### add USDC trustline

```bash
npx tsx skills/check-balance/add-trustline.ts
```

- Idempotent — safe to re-run.
- Uses mainnet Circle issuer on pubnet (`GA5Z...KZVN`), testnet issuer on testnet.
- Costs one subentry (+0.5 XLM min balance).
- SAC-only users don't strictly need this, but any Classic USDC operation does.

### swap XLM → USDC

Two modes — pick whichever the user expressed naturally:

```bash
# "Swap 10 XLM to USDC" → spend exactly 10 XLM
npx tsx skills/check-balance/swap-xlm-to-usdc.ts --xlm 10

# "I need 1 USDC" / "Change enough XLM for 1 USDC" → receive exactly 1 USDC
npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc 1

# Tighter slippage (default 1%)
npx tsx skills/check-balance/swap-xlm-to-usdc.ts --usdc 5 --slippage 0.005

# Skip confirmation on mainnet (large-amount gate still fires)
npx tsx skills/check-balance/swap-xlm-to-usdc.ts --xlm 10 --yes
```

**Intent mapping — pick the right mode:**

| User says | Use |
|---|---|
| "swap 10 XLM to USDC" | `--xlm 10` (strict send) |
| "sell 10 XLM for USDC" | `--xlm 10` |
| "I want 1 USDC" | `--usdc 1` (strict receive) |
| "get me 5 USDC from my XLM" | `--usdc 5` |
| "swap enough XLM to buy 10 USDC" | `--usdc 10` |

- `--xlm` uses Horizon's `strictSendPaths` + `PathPaymentStrictSend` — quotes the best output given a fixed input.
- `--usdc` uses `strictReceivePaths` + `PathPaymentStrictReceive` — quotes the cheapest input for a fixed output. Uses current DEX rate automatically; no need for the agent to compute XLM/USD manually.
- Requires an existing trustline — errors out with a hint if missing.

**Confirmation gates (always respected):**

- **Mainnet** → prompts for confirmation unless `--yes` passed
- **> 50,000 XLM OR > 10,000 USDC** → always prompts, even on testnet, even with `--yes`. This is intentional: large swaps are never silent.

## Prerequisites

- `.stellar-secret` file, `--secret-file <path>`, or an existing Stellar CLI identity selected with `--identity <name>`. All other config via CLI flags: `--network`, `--horizon-url`, `--rpc-url`, `--asset-sac`.
- For mainnet, read `references/mainnet-checklist.md`.
- Account must already exist on-chain (funded with ≥ 1 XLM on pubnet, or Friendbot on testnet).
