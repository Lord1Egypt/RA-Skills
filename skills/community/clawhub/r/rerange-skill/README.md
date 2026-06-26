# Rerange Agent Skills

This folder defines public skills for agents that integrate with Rerange.
The skills are written for MCP servers, autonomous resolvers, portfolio agents,
treasury agents, and wallet-connected assistants.

Rerange is a non-custodial liquidity execution protocol. Agents should model it
as:

```text
intent -> directional concentrated-liquidity order -> monitored execution
```

The protocol surface is built around:

- `RerangeHub`, which creates orders, previews actions, coordinates reranges,
  closes orders, and exposes canonical order state.
- `RerangeVault`, which holds user assets and executes adapter plans. Vault
  agents can manage orders but cannot withdraw funds.
- DEX adapters, currently Uniswap v3 and v4 adapters, which prepare venue calls
  and enforce tick, TWAP, slippage, and liquidity constraints.

## Skill Catalog

| Skill | Purpose | Primary actor |
| --- | --- | --- |
| [`protocol-discovery`](https://github.com/rerange-xyz/info/blob/main/skills/protocol-discovery.md) | Resolve deployments, adapters, tokens, pools, vaults, ABIs, and hub config. | All agents |
| [`intent-order-builder`](https://github.com/rerange-xyz/info/blob/main/skills/intent-order-builder.md) | Convert user execution intents into `CreateOrderParams` and previewed orders. | Wallet and portfolio agents |
| [`order-monitor`](https://github.com/rerange-xyz/info/blob/main/skills/order-monitor.md) | Track order state, progress, fees, range, market tick, and lifecycle events. | Monitoring and treasury agents |
| [`resolver-rerange`](https://github.com/rerange-xyz/info/blob/main/skills/resolver-rerange.md) | Find executable orders and submit profitable `rerange` or `batchRerange` calls. | Permissionless resolvers |
| [`vault-manager`](https://github.com/rerange-xyz/info/blob/main/skills/vault-manager.md) | Manage vault creation, manager delegation, owner-authorized close, and balance policy. | Wallet and treasury agents |
| [`strategy-composer`](https://github.com/rerange-xyz/info/blob/main/skills/strategy-composer.md) | Compose DCA, grid, passive exit, and allocation changes from multiple Rerange orders. | Portfolio agents |
| [`safety-risk`](https://github.com/rerange-xyz/info/blob/main/skills/safety-risk.md) | Apply mandatory checks before opening, reranging, closing, or composing strategies. | All agents |

## SKILL.md

https://github.com/rerange-xyz/info/blob/main/skills/SKILL.md

## Shared Rules

- Use `getOrderState(orderKey)` as the canonical order state read.
- Use `previewOpen`, `previewRerange`, and `previewClose` before submitting
  transactions.
- Treat target price as fixed user intent. Reranging moves the live liquidity
  window, not the execution objective.
- Keep token prices in user units until the integration boundary, then convert
  to ticks.
- Use canonical pool token order for `token0` and `token1`; `isSell` identifies
  which token is being sold.
- Respect `hubConfig.paused`, `hubConfig.rerangeCooldown`, adapter safety
  checks, and gas economics.
- Never grant an agent withdrawal authority. `setAgent` is for scoped order
  management, not custody.

## Recommended Agent Flow

1. Run `protocol-discovery` to resolve deployment metadata, token metadata,
   adapter allowlist status, pool data, and vault or order identity.
2. Run `safety-risk` before any state-changing action.
3. For new user intent, run `intent-order-builder`, then submit `open` or
   `open2` only after fresh preview, funding, and simulation checks.
4. Persist the returned or emitted `orderKey`, then use `order-monitor` as the
   continuous state source.
5. Use `resolver-rerange` only for maintenance actions that pass preview,
   cooldown, adapter safety, and gas policy.
6. Use `vault-manager` only for owner-authorized vault, delegation, close, and
   direct withdrawal workflows.

## Public Deployments

Use generated [ABIs](https://github.com/rerange-xyz/info/tree/main/protocol/abi)
and canonical [deployments](https://github.com/rerange-xyz/info/tree/main/protocol/deployments)
metadata for supported networks, hub addresses, adapters, and protocol config.
