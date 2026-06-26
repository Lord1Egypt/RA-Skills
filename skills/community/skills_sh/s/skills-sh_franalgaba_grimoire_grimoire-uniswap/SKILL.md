---
name: grimoire-uniswap
description: Retrieves Uniswap router metadata using the Grimoire venue CLI. Use when you need router addresses, adapter information, or Uniswap V3/V4 details.
---

# Grimoire Uniswap Skill

Use this skill to inspect Uniswap metadata and produce token/pool snapshots for spells.

Preferred invocations:

- `grimoire venue uniswap ...`
- `npx -y @grimoirelabs/cli venue uniswap ...` (no-install)
- `bun run packages/cli/src/index.ts venue uniswap ...` (repo-local)
- `grimoire-uniswap ...` (direct binary from `@grimoirelabs/venues`)

Recommended preflight:

- `grimoire venue doctor --adapter uniswap --chain 1 --rpc-url <rpc> --json`

## Commands

- `grimoire venue uniswap info` — adapter metadata
- `grimoire venue uniswap routers [--chain <id>]` — router addresses per chain
- `grimoire venue uniswap tokens [--chain <id>] [--symbol <sym>] [--address <addr>] [--source <url>]` — token list lookup
- `grimoire venue uniswap tokens-snapshot [--chain <id>] [--symbol <sym>] [--address <addr>] [--source <url>]` — generate spell `params:` block for tokens (agent-only)
- `grimoire venue uniswap pools --token0 <address|symbol> --token1 <address|symbol> [--chain <id>] [--fee <bps>] [--limit <n>] [--source <url>] [--endpoint <url>] [--graph-key <key>] [--subgraph-id <id>] [--rpc-url <url>] [--factory <address>]` — find pools for a token pair
- `grimoire venue uniswap pools-snapshot --token0 <address|symbol> --token1 <address|symbol> [--chain <id>] [--fee <bps>] [--limit <n>] [--source <url>] [--endpoint <url>] [--graph-key <key>] [--subgraph-id <id>] [--rpc-url <url>] [--factory <address>]` — generate spell `params:` block for pools (agent-only)

## Pool Data Sources

Pools can be fetched from The Graph (subgraph) or directly from on-chain factory contracts:

- **Subgraph** (default when `GRAPH_API_KEY` is set): queries The Graph decentralized network. Built-in subgraph IDs for Ethereum, Optimism, Polygon, Base, Arbitrum.
- **RPC** (fallback): if no usable graph config is present, pools uses on-chain factory lookups (with `--rpc-url`/`RPC_URL` when provided, otherwise chain default RPC where available).
- To force RPC mode: provide `--rpc-url` and omit `--graph-key`.

## Environment Variables

| Variable | Description |
|----------|-------------|
| `GRAPH_API_KEY` | The Graph API key for subgraph queries (get one at https://thegraph.com/studio/apikeys/) |
| `RPC_URL` | Fallback RPC URL for on-chain pool lookups |

## Examples

```bash
grimoire venue uniswap info --format table
grimoire venue uniswap routers
grimoire venue uniswap routers --chain 1
grimoire venue uniswap tokens --chain 1 --symbol USDC --format spell
grimoire venue uniswap pools --chain 1 --token0 USDC --token1 WETH --fee 3000 --format spell
grimoire venue uniswap pools --chain 8453 --token0 USDC --token1 WETH --fee 500 --rpc-url $RPC_URL --format table
grimoire venue uniswap pools --chain 8453 --token0 USDC --token1 WETH --fee 500 --graph-key $GRAPH_API_KEY --subgraph-id <id>
grimoire venue uniswap tokens-snapshot --chain 1 --symbol USDC
grimoire venue uniswap pools-snapshot --chain 1 --token0 USDC --token1 WETH --rpc-url $RPC_URL
```

Use `tokens-snapshot` or `pools-snapshot` to emit a `params:` block for spell inputs. These are agent-only commands (output suppressed in interactive mode).

## Metric Surface (Spell Comparisons)

Uniswap V3 and V4 expose `quote_out` for protocol comparison:

```spell
v3_out = metric("quote_out", uni_v3, USDC, "asset_out=WETH,amount=1000000,fee_tier=3000")
v4_out = metric("quote_out", uni_v4, USDC, "asset_out=WETH,amount=1000000,fee_tier=3000,tick_spacing=60")
```

Selector fields:

- required: `asset_out`
- optional: `amount` (defaults to 1 unit of input asset), `fee_tier`
- V4 optional: `tick_spacing`

## Spell Constraints

When writing swap actions in `.spell` files targeting Uniswap, use `with` clauses to set constraints:

```spell
uniswap_v3.swap(USDC, WETH, params.amount) with (
  fee_tier=3000,
  max_slippage=50,
  min_output=900000000000000,
  deadline=300,
)
```

**`fee_tier` is required.** The adapter throws if `fee_tier` is not specified. It is an action parameter (not a constraint) and is extracted from the `with()` clause.

Common fee tiers: `500` (0.05%), `3000` (0.3%), `10000` (1%).

| Parameter | Type | Description |
|-----------|------|-------------|
| `fee_tier` | integer (bps) | **Required.** Uniswap pool fee tier (e.g. `500`, `3000`, `10000`) |

| Constraint | Type | Description |
|-----------|------|-------------|
| `max_slippage` | integer (bps) | Maximum slippage in basis points (e.g. `50` = 0.5%) |
| `min_output` | integer (wei) | Minimum output amount floor |
| `max_input` | integer (wei) | Maximum input amount cap |
| `deadline` | integer (seconds) | Transaction deadline from now |
| `require_quote` | boolean | Fail if on-chain quote fetch fails |
| `require_simulation` | boolean | Fail if simulation unavailable |
| `max_gas` | integer (wei) | Gas estimate cap |

Always set both `max_slippage` and `min_output` for swaps to prevent unexpected losses.

## Supported Adapters

| Adapter | Router | Approval Flow |
|---------|--------|---------------|
| `@uniswap_v3` | SwapRouter02 | Standard ERC20 approve |
| `@uniswap_v4` | Universal Router | Permit2 |

## Notes

- CLI currently exposes V3 metadata. V4 adapter is available programmatically via `createUniswapV4Adapter()`.
- For metadata lookups (`tokens`, `pools`), use `grimoire venue uniswap ...` even when your spell venue is `uniswap_v4`.
- Outputs JSON/table; `tokens` and `pools` also support `--format spell`.
- Prefer `--format json` for automation and reproducible snapshots.
- Only metadata is exposed (no on-chain quote endpoints).
