---
name: defi-agent
skill: defi
description: DeFi operations on Stacks mainnet — ALEX DEX token swaps and pool queries, plus Zest Protocol lending (supply, withdraw, borrow, repay, claim rewards).
---

# DeFi Agent

This agent handles DeFi operations across two mainnet Stacks protocols: ALEX DEX (AMM token swaps via alex-sdk) and Zest Protocol (lending and borrowing against collateral). All operations are mainnet-only. Most operations require an unlocked wallet for routing context; write operations additionally submit on-chain transactions.

## Prerequisites

- Wallet unlocked via `bun run wallet/wallet.ts unlock` (required for all operations including reads)
- Network must be mainnet — ALEX DEX and Zest Protocol are mainnet-only
- For `zest-borrow`: sufficient collateral must be supplied to Zest first
- For `alex-swap`: use `alex-list-pools` first to confirm the token pair exists
- For `zest-supply`/`zest-borrow`: use `zest-list-assets` to get the correct asset symbol or contract ID

## Decision Logic

| Goal | Subcommand |
|------|-----------|
| Get token swap price before committing | `alex-get-swap-quote` — read expected output for tokenX→tokenY |
| Execute a token swap on ALEX DEX | `alex-swap` — swaps with optional slippage protection |
| Look up pool reserves for a token pair | `alex-get-pool-info` — returns reserve balances |
| Discover tradeable token pairs | `alex-list-pools` — lists all ALEX pools with token IDs |
| List assets available on Zest | `zest-list-assets` — shows supported symbols and contract IDs |
| Check current lending/borrow position | `zest-get-position` — returns supplied and borrowed amounts |
| Supply assets to earn lending yield | `zest-supply` — deposits assets into Zest lending pool |
| Withdraw supplied assets | `zest-withdraw` — redeems supplied assets plus interest |
| Borrow against supplied collateral | `zest-borrow` — borrows assets from Zest |
| Repay borrowed assets | `zest-repay` — repays borrowed amount plus interest |
| Claim accumulated Zest rewards | `zest-claim-rewards` — claims wSTX rewards for sBTC suppliers |

## Safety Checks

- Before `alex-swap`: always run `alex-get-swap-quote` first and verify the expected output is acceptable
- Before `alex-swap`: set `--min-amount-out` to enforce slippage protection (default is 0 = no protection)
- Before `zest-borrow`: verify collateral ratio via `zest-get-position` — Zest positions carry liquidation risk
- Before `zest-borrow`: check that supplied collateral value exceeds borrow amount at current protocol LTV limits
- Before `zest-withdraw`: confirm no outstanding borrow that would become undercollateralized after withdrawal
- Token amounts are in smallest units (micro-STX, sats) — double-check decimal places before submitting

## Error Handling

| Error message | Cause | Fix |
|--------------|-------|-----|
| "No active wallet found. Specify --wallet-id." | Wallet session expired or not unlocked | Run `bun run wallet/wallet.ts unlock` |
| "Pool not found or no liquidity" | Token pair doesn't exist on ALEX | Run `alex-list-pools` to find valid pairs |
| "No position found for this asset" | Address hasn't supplied this asset | Supply asset first with `zest-supply` |
| "--limit must be a positive integer" | Invalid `--limit` value passed | Pass a positive integer (e.g. `--limit 50`) |

## Output Handling

- `alex-get-swap-quote`: use `quote.expectedAmountOut` to decide if swap is worth executing; pass as `--min-amount-out` in `alex-swap`
- `alex-swap`: `txid` and `explorerUrl` confirm the on-chain transaction
- `alex-list-pools`: use `pools[].tokenX` and `pools[].tokenY` contract IDs for `--token-x`/`--token-y` in swap commands
- `zest-list-assets`: use `assets[].symbol` (e.g. `stSTX`, `sBTC`) as shorthand in `--asset` for all `zest-*` commands
- `zest-get-position`: `position.supplied` and `position.borrowed` are in smallest units; monitor collateral ratio
- All write operations return `txid` — feed into a query skill or explorer URL to verify settlement

## Example Invocations

```bash
# Get a swap quote on ALEX DEX (STX → ALEX)
bun run defi/defi.ts alex-get-swap-quote --token-x STX --token-y ALEX --amount-in 1000000

# Execute swap with slippage protection (min 95% of expected out)
bun run defi/defi.ts alex-swap --token-x STX --token-y ALEX --amount-in 1000000 --min-amount-out 49700

# Supply sBTC to Zest Protocol lending pool
bun run defi/defi.ts zest-supply --asset sBTC --amount 10000
```
