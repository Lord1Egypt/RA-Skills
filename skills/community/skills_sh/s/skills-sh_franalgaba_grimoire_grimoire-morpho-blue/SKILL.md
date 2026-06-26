---
name: grimoire-morpho-blue
description: Fetches Morpho Blue public deployment metadata using the Grimoire venue CLI. Use when you need contract addresses or adapter info.
---

# Grimoire Morpho Blue Skill

Use this skill to query Morpho Blue deployment metadata and vault snapshots for spell params.

Preferred invocations:

- `grimoire venue morpho-blue ...`
- `npx -y @grimoirelabs/cli venue morpho-blue ...` (no-install)
- `bun run packages/cli/src/index.ts venue morpho-blue ...` (repo-local)
- `grimoire-morpho-blue ...` (direct binary from `@grimoirelabs/venues`)

Recommended preflight:

- `grimoire venue doctor --adapter morpho-blue --chain 8453 --rpc-url <rpc> --json`

Use `--format spell` to emit a `params:` snapshot block.

The snapshot includes provenance fields (`snapshot_at`, `snapshot_source`) and APY data.

Use `vault-liquidity` for Morpho Vault V2 vault-wide withdrawal liquidity. It reads onchain Vault V2 fields, caps Morpho Market V1 liquidity-adapter assets by available underlying market cash, and does not use ERC-4626 `maxWithdraw` / `maxRedeem`, which Vault V2 intentionally returns as `0`.

APY semantics:

- `apy` / `net_apy` are decimal rates (for example `0.0408` = `4.08%`).
- When reporting, include both decimal and percent display when possible.

## Commands

- `grimoire venue morpho-blue info` — adapter metadata
- `grimoire venue morpho-blue addresses [--chain <id>]` — contract addresses per chain
- `grimoire venue morpho-blue vaults [--chain <id>] [--asset <symbol>] [--min-tvl <usd>] [--min-apy <decimal>] [--min-net-apy <decimal>] [--sort <netApy|apy|tvl|totalAssetsUsd|name>] [--order <asc|desc>] [--limit <n>]` — list and filter vaults
- `grimoire venue morpho-blue vaults-snapshot [--chain <id>] [--asset <symbol>] [--min-tvl <usd>] [--min-apy <decimal>] [--min-net-apy <decimal>] [--sort <netApy|apy|tvl|totalAssetsUsd|name>] [--order <asc|desc>] [--limit <n>]` — generate spell `params:` block for vaults (agent-only)
- `grimoire venue morpho-blue vault-liquidity [--chain <id>] --vault <address> [--rpc-url <url>] [--format json|table|spell]` — read Morpho Vault V2 withdrawable liquidity in asset units and integer bps

## Examples

```bash
grimoire venue morpho-blue info --format table
grimoire venue morpho-blue addresses --chain 1
grimoire venue morpho-blue addresses --chain 8453
grimoire venue morpho-blue vaults --chain 8453 --asset USDC --min-tvl 5000000 --format table
grimoire venue morpho-blue vaults --chain 8453 --asset USDC --min-tvl 5000000 --format spell
grimoire venue morpho-blue vaults-snapshot --chain 8453 --asset USDC --min-tvl 5000000
grimoire venue morpho-blue vault-liquidity --chain 8453 --vault 0xbeef0e0834849aCC03f0089F01f4F1Eeb06873C9 --format json
grimoire venue morpho-blue vault-liquidity --chain 8453 --vault 0xbeef0e0834849aCC03f0089F01f4F1Eeb06873C9 --format spell
```

Use `vaults-snapshot` to emit a `params:` block for spell inputs. This is an agent-only command (output suppressed in interactive mode).

`vault-liquidity --format spell` emits payload-ready JSON params for `protocol: morpho-vault-v2`, `metric: withdrawable_liquidity_bps`, `withdrawable_liquidity_assets`, `total_assets`, `idle_assets`, `liquidity_adapter`, and `liquidity_adapter_assets`.

Example provenance output fields to preserve:

- `snapshot_at`
- `snapshot_source`
- `units` (for example `net_apy=decimal`, `net_apy_pct=percent`, `tvl_usd=usd`)

## Metric Surface (Spell Comparisons)

Morpho exposes the `apy` metric surface and supports selector-based market targeting:

```spell
morpho_apy_default = apy(morpho, USDC)
morpho_apy_market = apy(morpho, USDC, "weth-usdc-86")
morpho_apy_market_id = apy(morpho, USDC, "0x...")
morpho_apy_generic = metric("apy", morpho, USDC, "wbtc-usdc-86")
morpho_utilization_bps = metric("utilization_bps", morpho, USDC, "wbtc-usdc-86")
vault_apy = metric("vault_apy", morpho, USDC, "vault=0xVaultAddress")
vault_net_apy = metric("vault_net_apy", morpho, USDC, "vault=0xVaultAddress")
vault_withdrawable_liquidity_bps = metric("withdrawable_liquidity_bps", morpho, USDC, "vault=0xVaultAddress")
```

Use `apy(morpho, asset[, selector])` for Morpho Blue market APY comparisons.
Use `metric("utilization_bps", morpho, asset[, selector])` for Morpho Blue market utilization checks.
Use `metric("vault_apy", morpho, asset, selector)` or `metric("vault_net_apy", morpho, asset, selector)` for MetaMorpho vault comparisons.
Use `metric("withdrawable_liquidity_bps", morpho, asset, selector)` for Morpho Vault V2 live withdrawal liquidity checks.

Selector behavior:

- market no selector (`apy`): resolves by `asset` on the active chain and picks the highest-TVL match
- config market selector: use known market ids from adapter config (for example `weth-usdc-86`)
- onchain market id selector: use raw market id (`0x...`)
- vault selectors (`vault_apy` / `vault_net_apy`): `vault=<address|name|symbol>` or bare vault address/name/symbol
- `vault_apy` / `vault_net_apy` require explicit selector (no implicit fallback)

When multiple vaults/markets exist for one asset, pass an explicit selector for deterministic comparisons.

## Spell Constraints

Morpho Blue actions do not support runtime constraints (`max_slippage`, etc.). Value-moving actions require an explicit `market_id`.

```spell
morpho_blue.lend(USDC, params.amount, "cbbtc-usdc-86")
morpho_blue.withdraw(USDC, params.amount, "cbbtc-usdc-86")
morpho_blue.borrow(USDC, params.amount) with (
  market_id="cbbtc-usdc-86",
)
morpho_blue.supply_collateral(cbBTC, params.amount, "cbbtc-usdc-86")
morpho_blue.withdraw_collateral(cbBTC, params.amount, "cbbtc-usdc-86")
```

Use `with (market_id=...)` when positional args are not convenient:

```spell
morpho_blue.lend(USDC, params.amount) with (
  market_id="0x1234...abcd",
)
```

Use `grimoire venue morpho-blue vaults` to discover available market IDs.

## Action Selection Guide

Choose actions by strategy intent:

- Supply-only strategy (no borrowing planned): prefer `vault_deposit` / `vault_withdraw`.
- Borrowing strategy (or future borrow/repay/collateral management): use market actions with explicit `market_id`.

Hard rules:

- `vault_deposit` / `vault_withdraw` require explicit vault address and do not use `market_id`.
- `lend`, `withdraw`, `borrow`, `repay`, `supply_collateral`, `withdraw_collateral` require explicit `market_id`.
- If vault address is missing for a vault action, do not guess: list candidate vaults and require user selection before authoring/executing.

## Action Semantics

- `lend(asset, amount, market_id)`: lend the market loan asset (lender side).
- `withdraw(asset, amount, market_id)`: withdraw previously lent loan asset.
- `supply_collateral(asset, amount, market_id)`: post collateral for borrowing (borrower side).
- `withdraw_collateral(asset, amount, market_id)`: remove posted collateral.
- `borrow(asset, amount, collateral?, market_id)`: borrow the market loan asset.
- `repay(asset, amount, market_id)`: repay borrowed loan asset.
- `vault_deposit(asset, amount, vault_address)`: deposit into MetaMorpho vault.
- `vault_withdraw(asset, amount, vault_address)`: withdraw from MetaMorpho vault.

`lend` and `supply_collateral` are not interchangeable:

- `lend` targets lender yield on loan asset.
- `supply_collateral` is collateral management for borrowing capacity.

APY expectations:

- `lend` accrues market supply APY (plus possible incentives).
- `supply_collateral` does not earn market lender APY; it is risk buffer for borrow.
- Collateral token may have its own native yield behavior (for example wstETH), separate from Morpho supply APY.

## Workflow Patterns

Supply-only via vault:

```spell
morpho_blue.vault_deposit(USDC, params.amount, "0xVaultAddress")
```

If vault is not provided, run discovery first and ask user to pick:

```bash
grimoire venue morpho-blue vaults --chain <id> --asset <symbol> --sort netApy --order desc --limit 5 --format table
```

Then use the selected vault address in `vault_deposit` / `vault_withdraw`.

Borrow workflow (market):

```spell
morpho_blue.supply_collateral(WETH, params.collateral_amount, "weth-usdc-86")
morpho_blue.borrow(USDC, params.borrow_amount, WETH, "weth-usdc-86")
```

Unwind borrow workflow:

```spell
morpho_blue.repay(USDC, params.repay_amount, "weth-usdc-86")
morpho_blue.withdraw_collateral(WETH, params.collateral_out, "weth-usdc-86")
```

Lend-only via market (when explicit market control is desired):

```spell
morpho_blue.lend(USDC, params.amount, "cbbtc-usdc-86")
```

## Default Markets

The adapter ships with pre-configured markets for Ethereum (chain 1) and Base (chain 8453):

### Ethereum (chain 1)

| Market | Loan | Collateral | LLTV |
|--------|------|-----------|------|
| cbbtc-usdc-1 | USDC | cbBTC | 86% |
| wbtc-usdc-1 | USDC | WBTC | 86% |
| wsteth-weth-1 | WETH | wstETH | 96.5% |

### Base (chain 8453)

| Market | Loan | Collateral | LLTV |
|--------|------|-----------|------|
| cbbtc-usdc-86 | USDC | cbBTC | 86% |
| weth-usdc-86 | USDC | WETH | 86% |

## Notes

- Outputs JSON/table; `vaults` also supports `--format spell`.
- Uses the SDK's chain address registry.
- Prefer `--format json` in automation and `--format table` for quick triage.
