---
skill: resolver-rerange
version: 1.0.0
category: rerange_automation
---

# Resolver Rerange Skill

Use this skill to operate a permissionless resolver that advances or closes
orders by calling `rerange` or `batchRerange`.

Resolvers do not need vault ownership. Resolver rewards are paid only from
target-asset fees according to protocol fee settlement.

## Candidate Discovery

Build the candidate universe from:

- `OrderOpened` logs,
- local indexed open orders,
- owner or vault watchlists,
- `OrderReranged` events for recently active positions.

Drop candidates when `isOrderClosed(orderKey)` is true.

## Required Reads Per Candidate

1. `getOrderState(orderKey)`
2. `hubConfig()`
3. `previewRerange(orderKey)`
4. Current gas estimate and target-token value for expected reward

For permissionless `rerange(orderKey)`, enforce `block.timestamp >=
order.lastRerangeAt + hubConfig.rerangeCooldown` before submitting. The manager
overload can update order policy, but autonomous agents should still apply a
local cooldown unless the strategy explicitly authorizes faster intervention.

## Rerange Eligibility

A candidate is executable only when preview succeeds and at least one of these
is true:

- `preview.willClose` is true,
- `preview.activatePlan.activateOrder` is true,
- the order is inside its current live position and refresh is economically
  justified,
- price is inside the trigger band around target,
- price has crossed the target and the action will close.

Conceptually, outside the old position:

- SELL orders can rerange when `currentTick >= targetTick - triggerTicks`.
- BUY orders can rerange when `currentTick <= targetTick + triggerTicks`.

The adapter is responsible for final tick drift, TWAP, slippage, and activation
minima. The agent still must preview and simulate.

## Profitability Check

Submit only when:

```text
expected_target_asset_reward_value >= gas_cost * required_margin
```

Recommended defaults:

- `required_margin`: `1.2` for private routing, `1.5` for public mempool.
- Include L1 data fee on L2 networks.
- Ignore non-target-asset fees for resolver reward estimation.

Map preview rewards to the target token before pricing them:

- for SELL orders, target token is `token1`, so resolver reward is `reward1`,
- for BUY orders, target token is `token0`, so resolver reward is `reward0`.

If the target-token reward is zero, permissionless execution is unprofitable
unless the resolver has an explicit non-economic maintenance mandate.

## Transaction Methods

- `rerange(orderKey)` for a single high-confidence candidate.
- `rerange(orderKey, targetTick, triggerTicks)` only when the order manager is
  intentionally updating target policy and has authority.
- `batchRerange(orderKeys)` for permissionless scanning. It returns per-order
  success flags instead of reverting the full batch.
- `multicall` with individually encoded `rerange` calls only after strict
  preview filtering.

## Output Shape

```json
{
  "action": "batchRerange",
  "chain_id": "<chain-id-from-deployments>",
  "hub": "<hub-address-from-deployments>",
  "order_keys": ["<order-key>"],
  "expected": {
    "will_close": 1,
    "will_activate": 3,
    "reward_value_usd": "8.14",
    "gas_cost_usd": "4.01"
  },
  "filters": {
    "cooldown_passed": true,
    "preview_passed": true,
    "adapter_safety_passed": true,
    "profitable": true
  }
}
```

## Failure Handling

- If a candidate preview fails, mark it temporarily blocked and retry after the
  next tick movement or after cooldown.
- If `batchRerange` partially fails, decode successful results and keep failed
  orders in the candidate set only if the failure is transient.
- If hub is paused, stop submitting transactions and continue read-only
  monitoring.
- If gas spikes above expected reward, defer execution.
- If preview was read on an old block, refresh it before submitting. Treat
  preview outputs as block-scoped, not durable instructions.

## Do Not

- Do not rerange during hub pause.
- Do not submit transactions without a fresh `previewRerange`.
- Do not count source-asset or non-target fees as resolver reward.
- Do not spam rerange attempts inside `hubConfig.rerangeCooldown`.
- Do not change `targetTick` or `triggerTicks` unless acting as an authorized
  manager with explicit strategy policy.
