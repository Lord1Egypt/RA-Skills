---
name: grimoire-polymarket
description: Queries Polymarket market data and CLOB state, and manages CLOB orders via the Grimoire venue CLI wrapper backed by the official Polymarket CLI.
---

# Grimoire Polymarket Skill

Use this skill for Polymarket market discovery, CLOB market data, and order-management operations through the `polymarket` venue adapter.

Preferred invocations:

- `grimoire venue polymarket ...`
- `npx -y @grimoirelabs/cli venue polymarket ...` (no-install)
- `bun run packages/cli/src/index.ts venue polymarket ...` (repo-local)
- `grimoire-polymarket ...` (direct binary from `@grimoirelabs/venues`)

Recommended preflight:

- `grimoire venue doctor --adapter polymarket --json`
- `grimoire venue polymarket info --format json`

## Commands

Canonical agent commands:

- `grimoire venue polymarket info [--format <auto|json|table>]`
- `grimoire venue polymarket search-markets [--query <text>] [--slug <slug|url>] [--question <text>] [--event <text>] [--tag <text>] [--category <text>] [--league <text>] [--sport <text>] [--open-only <true|false>] [--active-only <true|false>] [--ignore-end-date <true|false>] [--tradable-only <true|false>] [--all-pages <true|false>] [--max-pages <n>] [--stop-after-empty-pages <n>] [--limit <n>] [--format <auto|json|table>]`

Allowed passthrough groups (official CLI surface, restricted by wrapper policy):

- `markets` (`list|get|search|tags`)
- `data` (positions/value/leaderboards/etc.)

Blocked groups in this wrapper (intentionally not exposed for agents):

- `wallet`
- `bridge`
- `approve`
- `ctf`
- `setup`
- `upgrade`
- `shell`

Legacy compatibility aliases are still supported (`market`, `book`, `midpoint`, `spread`, `price`, `last-trade-price`, `tick-size`, `neg-risk`, `fee-rate`, `price-history`, `order`, `trades`, `open-orders`, `balance-allowance`, `closed-only-mode`, `server-time`) but should not be used for new agent flows.

## Examples

```bash
# Wrapper/health
grimoire venue polymarket info --format json
grimoire venue polymarket status --format json

# Canonical discovery
grimoire venue polymarket search-markets --query bitcoin --active-only true --open-only true --format json
grimoire venue polymarket search-markets --category sports --league "la liga" --active-only true --open-only true --format json

# Official passthrough discovery/data
grimoire venue polymarket markets list --limit 25 --format json
grimoire venue polymarket markets search "atleti" --limit 25 --format json
grimoire venue polymarket data positions <address> --limit 25 --format json
grimoire venue polymarket data trades <address> --limit 25 --format json
grimoire venue polymarket data leaderboard --period week --order-by vol --limit 25 --format json

# Legacy compatibility aliases (still supported)
grimoire venue polymarket book --token-id <token_id> --format json
grimoire venue polymarket price --token-id <token_id> --side buy --format json
grimoire venue polymarket order --order-id <order_id> --format json
grimoire venue polymarket open-orders --market <condition_id> --format json
```

## Runtime Configuration

Adapter/runtime auth (for spell execution):

- required by default: `POLYMARKET_PRIVATE_KEY`
- optional API creds: `POLYMARKET_API_KEY`, `POLYMARKET_API_SECRET`, `POLYMARKET_API_PASSPHRASE`
- optional derive toggle (default true): `POLYMARKET_DERIVE_API_KEY=true|false`
- optional signature routing: `POLYMARKET_SIGNATURE_TYPE` (`0` EOA, `1` POLY_PROXY, `2` GNOSIS_SAFE), `POLYMARKET_FUNDER`
- `grimoire cast` / `grimoire resume` key-based flows inject the same wallet-manager key into the Polymarket adapter, so a separate `POLYMARKET_PRIVATE_KEY` env is not required there.

Venue CLI backend:

- Official binary required: `polymarket`
- Install: `brew tap Polymarket/polymarket-cli && brew install polymarket`
- Optional path override: `POLYMARKET_OFFICIAL_CLI=/custom/path/polymarket`

## Spell Actions

Polymarket uses `custom` action type with `op: "order"` for order placement:

```spell
polymarket.custom(
  op="order",
  token_id="TOKEN_ID",
  price="0.55",
  size="100",
  side="BUY",
  order_type="GTC",
)
```

The adapter does not support runtime constraints (`max_slippage`, etc.). Order routing:
- `GTC`/`GTD` → limit order (`createAndPostOrder`)
- `FOK`/`FAK` → market order (`createAndPostMarketOrder`)

## Metric Surface (Spell Comparisons)

Polymarket exposes `mid_price` for CLOB token midpoint comparisons:

```spell
poly_mid = metric("mid_price", polymarket, USDC, "token_id=<clobTokenId>")
```

Selector keys accepted: `token_id`, `tokenid`, `market_id`, `id`.
If selector is omitted, the metric falls back to the 3rd argument value.

## Adapter Notes

- Adapter name: `polymarket`
- Execution type: `offchain`
- Supported chain metadata: `137` (Polygon)
- Action type: `custom`
- Supported custom ops: `order`, `cancel_order`, `cancel_orders`, `cancel_all`, `heartbeat`

Order argument aliases accepted:

- token: `token_id` or `tokenID` or `tokenId` or `coin`
- amount: `size` or `amount`
- side: `BUY`/`SELL`
- order type: `GTC`/`GTD`/`FOK`/`FAK`
- extra compatibility aliases: `arg0..arg5`, `reduce_only`

Order type routing:

- `GTC`/`GTD` -> limit order path (`createAndPostOrder`)
- `FOK`/`FAK` -> market order path (`createAndPostMarketOrder`)

## Notes

- Prefer `--format json` for agent and automation workflows.
- `search-markets` is the agent-oriented normalized discovery command; passthrough `markets search` is thinner and closer to official behavior.
- Keep prompts/tooling on this CLI surface; do not call Polymarket HTTP APIs directly from advisory tools.
