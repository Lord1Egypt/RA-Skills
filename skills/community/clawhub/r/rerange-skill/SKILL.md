---
name: rerange
description: Build, preview, monitor, rerange, close, and risk-check non-custodial Rerange liquid orders using @rerange/wagmi.
homepage: https://rerange.xyz
metadata: {"openclaw":{"homepage":"https://rerange.xyz","requires":{"bins":["node"]}}}
---

# Rerange Skill

Use this skill when a user or agent needs to discover Rerange deployments,
construct liquid orders, monitor order state, run permissionless reranges,
manage user vault delegation, compose bounded strategies, or perform safety
preflight checks.

Rerange is a non-custodial liquidity execution protocol:

```text
intent -> directional concentrated-liquidity order -> monitored execution
```

Use `@rerange/wagmi` as the SDK boundary for ABIs, generated contract actions,
and canonical deployment metadata. Do not reconstruct hub or vault addresses
manually when the SDK can provide them.

## SDK Execution

This skill includes a Node helper at `{baseDir}/index.js`.

Run it with:

```bash
node {baseDir}/index.js <command> [args]
```

The helper imports `@rerange/wagmi`; in this repository it can also fall back to
the local built SDK at `../sdk/dist/index.js` for development.

Commands:

- `deployments [chainId]`: print all supported deployments or one deployment.
- `abi hub|vault`: print the selected ABI from `@rerange/wagmi`.
- `encode hub|vault <functionName> <jsonArgs>`: encode calldata without signing.
- `read <chainId> hub|vault <address> <functionName> <jsonArgs> [rpcUrl]`: perform a read-only contract call.

Examples:

```bash
node {baseDir}/index.js deployments
node {baseDir}/index.js deployments 8453
node {baseDir}/index.js abi hub
node {baseDir}/index.js encode hub getOrderState '["0x...orderKey"]'
node {baseDir}/index.js read 8453 hub 0x888956E46d2af8F6B2890a39E55542219F4bd192 hubConfig '[]' https://mainnet.base.org
```

The helper never signs transactions and never asks for private keys. For writes,
return unsigned transaction intent, wagmi action name, target contract, calldata,
value, and safety status so a wallet-connected runtime can simulate and submit.

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
- Never request, store, or handle private keys or seed phrases.

## Recommended Agent Flow

1. Run protocol discovery to resolve deployment metadata, token metadata,
   adapter allowlist status, pool data, and vault or order identity.
2. Run safety and risk checks before any state-changing action.
3. For a new user intent, build order parameters, then submit `open` or `open2`
   only after fresh preview, funding, and simulation checks.
4. Persist the returned or emitted `orderKey`, then monitor with live
   `getOrderState`.
5. Use resolver rerange only for maintenance actions that pass preview,
   cooldown, adapter safety, and gas policy.
6. Use vault management only for owner-authorized vault, delegation, close, and
   direct withdrawal workflows.

## Protocol Discovery

Use discovery before any other Rerange action. It resolves the chain,
deployment, adapters, tokens, pools, vaults, order keys, and live hub config.

Required inputs:

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "owner": "<owner-address>",
  "from_token": "WETH",
  "to_token": "USDC",
  "order_key": "<order-key>",
  "vault": "<vault-address>",
  "order_index": 0
}
```

Only `chain_id` is always required. Interpret optional identifiers in this
priority order: `order_key`, `(vault, order_index)`, `vault`, `owner`.

Required reads:

- Deployment metadata from `@rerange/wagmi`.
- `RerangeHub.hubConfig()`
- `RerangeHub.adapters(adapter)`
- `RerangeHub.vaults(owner)` as the next vault index upper bound.
- `RerangeHub.predictVault(owner, vaultIndex)`
- `RerangeHub.vaultOrderCount(vault)`
- `RerangeHub.getOrderKey(vault, orderIndex)`
- `RerangeHub.getOrder(orderKey)` when reconstructing existing order metadata.
- `RerangeHub.getOrderState(orderKey)`

Pool selection must prefer pools where token order is canonical, adapter is
allowed, usable liquidity exists near current tick, fee tier fits the execution
horizon, and tokens are supported. Rank valid pools by live liquidity, then
historical volume, then fee tier suitability. For large orders, require live or
indexed liquidity data.

For a new order with no explicit vault, read `vaults(owner)`, call
`predictVault(owner, vaultIndex)`, use that predicted address in `previewOpen`,
then let `open` create the vault or create it explicitly with `createVault`.

Return a blocking error when the chain is unsupported, the hub is paused,
adapter is not allowed, token is unsupported or ambiguous, no valid pool exists,
an order key cannot be resolved, or required reads fail through healthy RPC.

## Intent Order Builder

Use this for `sell_high`, `buy_low`, `passive_exit`, and `rebalance_step`
intents. DCA and grid strategies are composed by the strategy composer.

Required inputs:

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "owner": "<owner-address>",
  "intent": "sell_high",
  "from_token": "WETH",
  "to_token": "USDC",
  "amount": "1.0",
  "target_price": 3500,
  "trigger_bps": 500,
  "pool": "<pool-address>",
  "risk_profile": "moderate",
  "referrer": "ZERO_ADDRESS",
  "keep_balances_in_vault": false,
  "unwrap_out": false
}
```

Construction rules:

1. Resolve deployment, tokens, adapters, and candidate pools.
2. Convert `amount` into raw token units using source token decimals.
3. Canonically sort the pool pair into `token0` and `token1`.
4. Set `isSell = true` when source token is `token0`; otherwise `false`.
5. Convert `target_price` into `targetTick` using canonical pool token order.
6. Convert `trigger_bps` into `triggerTicks`, or default to the tick distance
   between current price and target.
7. Resolve `risk_profile` into concrete adapter policy values.
8. Encode adapter config with pool, fee tier, TWAP, tick drift, and slippage.
9. Call `previewOpen(owner, params)`.
10. Return unsigned transaction parameters only after preview succeeds.

Risk profile defaults:

```json
{
  "conservative": {"max_slippage_bps": 50, "max_twap_deviation_ticks": 50, "max_tick_deviation": 50},
  "moderate": {"max_slippage_bps": 100, "max_twap_deviation_ticks": 100, "max_tick_deviation": 100},
  "aggressive": {"max_slippage_bps": 150, "max_twap_deviation_ticks": 150, "max_tick_deviation": 150}
}
```

If no mapping is configured, ignore `risk_profile` and require concrete adapter
policy fields.

Create order parameter shape:

```json
{
  "vault": "ZERO_ADDRESS",
  "adapter": "<adapter-address-from-deployments>",
  "token0": "<canonical-token0-address>",
  "token1": "<canonical-token1-address>",
  "capital": "1000000000000000000",
  "isSell": true,
  "targetTick": -195000,
  "triggerTicks": 300,
  "adapterConfig": "<encoded-adapter-config>",
  "referrer": "ZERO_ADDRESS",
  "keepBalancesInVault": false,
  "unwrapOut": false
}
```

Use `open(params)` after approval or vault prefunding. Use
`open2(params, permit, signature)` only when the owner provides Permit2. Always
refresh `previewOpen(owner, params)` before submission.

Block order construction when target direction is wrong, capital is zero, hub is
paused, adapter is not allowed, preview reverts, immediate flow has no activation
plan, current tick drifted materially, funding cannot be proven, or the user
asks to bypass slippage, TWAP, or liquidity checks.

## Order Monitor

Use monitoring for open Rerange orders because they are persistent liquidity
positions, not one-time swaps.

At least one of `order_key`, `(vault, order_index)`, or `owner` is required.

Required reads:

- `getOrderState(orderKey)`
- `isOrderClosed(orderKey)`
- `previewRerange(orderKey)` for actionability
- `hubConfig()` for pause and cooldown state
- `previewClose(orderKey)` before user-requested close
- Events: `OrderOpened`, `OrderReranged`, `OrderClosed`, `VaultCreated`,
  `OrderExecuted`

Map live protocol state into agent states: `OPEN`, `ACTIVE`, `IN_RANGE`,
`OUT_OF_RANGE`, `RERANGEABLE`, `COMPLETED`, `CLOSED`, and `ACTION_BLOCKED`.
Never persist stale lifecycle state as truth; refresh from `getOrderState`.

Persist minimal memory: chain id, order key, owner, vault, order index, intent,
tokens, target tick, trigger ticks, creation time, last seen status, last rerange
time, and last progress bps. Reconstruct tokens from `token0`, `token1`, and
`isSell`; do not invent symbols when metadata is missing.

Monitor active user-facing orders every 5 to 15 minutes, resolver candidates
from every block to every 5 minutes, passive portfolio reports every 30 to 60
minutes, and event logs after restart or missed RPC intervals.

Do not infer final status from event logs alone. Do not trigger rerange purely
because a range was exited; always preview and check cooldown.

## Resolver Rerange

Use this for permissionless resolvers that advance or close orders by calling
`rerange` or `batchRerange`. Resolvers do not need vault ownership. Resolver
rewards are paid only from target-asset fees.

Build candidates from `OrderOpened` logs, local indexed open orders, watchlists,
and `OrderReranged` events. Drop candidates when `isOrderClosed(orderKey)` is
true.

Required reads per candidate:

1. `getOrderState(orderKey)`
2. `hubConfig()`
3. `previewRerange(orderKey)`
4. Current gas estimate and target-token value for expected reward.

For permissionless `rerange(orderKey)`, enforce
`block.timestamp >= order.lastRerangeAt + hubConfig.rerangeCooldown`.

A candidate is executable only when preview succeeds and will close, will
activate, is economically justified while in range, price is inside the trigger
band around target, or price crossed the target and the action will close.

Submit only when:

```text
expected_target_asset_reward_value >= gas_cost * required_margin
```

Use `1.2` for private routing and `1.5` for public mempool unless policy says
otherwise. Include L1 data fee on L2 networks. Ignore non-target-asset fees for
resolver reward estimation. For sell orders target token is `token1`; for buy
orders target token is `token0`.

Use `rerange(orderKey)` for a single candidate, manager overloads only with
explicit authority, and `batchRerange(orderKeys)` for permissionless scanning.
Do not submit during hub pause, without a fresh preview, inside cooldown, or
when gas exceeds expected reward.

## Vault Manager

Use this for owner-authorized vault workflows: create vaults, assign
time-limited agents, choose balance policy, close orders, and report balances.

Owner actions:

- `RerangeHub.createVault()`
- `RerangeVault.setAgent(agent, accessExpiresAt)`
- `RerangeHub.close(orderKey)` when owner-authorized
- `RerangeVault.withdraw(token, to, amount)`
- `RerangeVault.call(target, value, data)` for exact owner-approved calls
- `RerangeVault.multicall(targets, values, data)` for exact owner-approved
  batches

A configured vault agent can manage supported orders but must not receive
withdrawal authority. Use `setAgent(agent, accessExpiresAt)` for scoped,
session-key-like delegation.

Balance policy:

- `keepBalancesInVault = false`: close returns attributable balances to owner.
- `keepBalancesInVault = true`: final balances remain in vault.
- `unwrapOut = true`: unwrap WETH output to native ETH where supported.

Before closing, read `getOrderState`, call `previewClose`, explain expected
returned tokens, fees, and reward settlement, submit `close(orderKey)` only from
owner or authorized agent context, then confirm via event and final balances.

Do not ask users to delegate unlimited wallet authority. Do not call arbitrary
vault `call` unless the owner explicitly requested target, value, calldata,
purpose, and risk.

## Strategy Composer

Use this to turn portfolio or treasury objectives into bounded Rerange orders.
Supported modules: `productive_limit_order`, `passive_exit`,
`buy_low_accumulation`, `dca`, `grid`, `rebalance`, and `treasury_runway`.

Do not present leverage, liquidation protection, derivatives, or cross-chain
execution as Rerange v1 features.

Planning rules:

1. Check portfolio balances and existing open Rerange orders.
2. Enforce user exposure, concentration, and order-count limits.
3. Split capital only when multiple orders materially improve execution control.
4. Use the intent order builder for each proposed order.
5. Use safety and risk checks for each order and aggregate strategy.
6. Return explicit order parameters and monitoring policy.

For DCA, create one order for the current step and wait for completion, close,
or timeout before the next step, unless simultaneous deployment is approved. For
grid, place buys below current price and sells above current price, cap per-band
capital, cap active orders, and monitor aggregate exposure after every fill.

Do not reinvest proceeds, replace completed bands, or hide the difference
between an order target and a guaranteed execution price without explicit user
policy.

## Safety And Risk

Use this as mandatory preflight for all Rerange actions.

Global checks:

- supported chain,
- correct hub address,
- `hubConfig.paused == false` for opens and reranges,
- adapter is allowed,
- token addresses and decimals are known,
- pool token order is canonical,
- user amount is nonzero,
- target direction matches user intent,
- preview succeeds,
- simulation succeeds where wallet tooling supports it,
- gas cost is acceptable.

Close is the pause exception: `close(orderKey)` is an owner or manager recovery
path and may be used while paused after preview and authorization checks.

Open checks require successful `previewOpen`, non-empty activation when the flow
expects immediate activation, bounded tick drift since preview, correct target
direction, sufficient allowance, Permit2, vault prefunding, or native wrap,
sufficient pool liquidity, and enabled slippage and TWAP policy.

Rerange checks require open order, elapsed cooldown, successful
`previewRerange`, close or activation signal, adapter safety, profitable gas for
permissionless execution, and fresh submission.

Close checks require owner or authorized agent caller, successful
`previewClose`, and clear explanation of balance destination, fees, and rewards.

Recommended autonomous limits:

```json
{
  "max_single_order_portfolio_pct": 20,
  "max_asset_exposure_pct": 40,
  "max_active_orders_per_pair": 8,
  "min_rerange_interval_sec": 300,
  "max_slippage_bps": 100,
  "max_twap_deviation_ticks": 100,
  "min_profit_to_gas_ratio": 1.2
}
```

Fee settlement is asset-aware: resolver reward is paid only from target-asset
fees; referrer share is paid only from non-target-asset fees; treasury receives
remaining non-target-asset fees; target-asset fees are not routed to referrer or
treasury; non-target-asset fees are not routed to resolver.

Stop opening new orders and switch to read-only monitoring when hub is paused,
RPC responses disagree, pool tick diverges from TWAP, indexed liquidity is
stale, gas spikes above policy, token metadata is inconsistent, or preview and
simulation disagree.

Never bypass preview, promise exact fill price, execute with unknown token
metadata, treat fee APR as guaranteed yield, or use owner withdrawal functions
from an autonomous resolver.
