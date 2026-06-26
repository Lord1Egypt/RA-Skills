---
skill: order-monitor
version: 1.0.0
category: rerange_observability
---

# Order Monitor Skill

Use this skill to maintain continuous state for open Rerange orders. Monitoring
is required because Rerange orders are persistent liquidity positions, not
one-time swaps.

## Required Inputs

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "order_key": "<order-key>",
  "vault": "<vault-address>",
  "order_index": 0,
  "owner": "<owner-address>"
}
```

At least one of `order_key`, `(vault, order_index)`, or `owner` must be
provided.

## Required Reads

- `getOrderState(orderKey)`
- `isOrderClosed(orderKey)`
- `previewRerange(orderKey)` for actionability
- `hubConfig()` for pause and cooldown state
- `previewClose(orderKey)` before user-requested close
- Event logs: `OrderOpened`, `OrderReranged`, `OrderClosed`,
  `VaultCreated`, `OrderExecuted`

## Derived Lifecycle

Map protocol state into agent lifecycle states:

| Agent state | Source |
| --- | --- |
| `OPEN` | Order exists with no meaningful progress yet. |
| `ACTIVE` | Order has liquidity and is executing. |
| `IN_RANGE` | Current tick is between `lowerTick` and `upperTick`. |
| `OUT_OF_RANGE` | Order is open but current tick is outside live range. |
| `RERANGEABLE` | `previewRerange` succeeds and will close or activate. |
| `COMPLETED` | `OrderStatus.Completed` from `getOrderState`. |
| `CLOSED` | Order has closed flag or `isOrderClosed` is true. |
| `ACTION_BLOCKED` | Cooldown, adapter safety, hub pause, or gas economics block action. |

Protocol status is derived from live order, position, and market state. Agents
should not persist a stale lifecycle state as truth; persist the last observed
state only as cache metadata and refresh from `getOrderState`.

## Output Shape

```json
{
  "order_key": "<order-key>",
  "status": "IN_RANGE",
  "current_tick": -196120,
  "range": {
    "lower_tick": -196200,
    "upper_tick": -195000
  },
  "progress_bps": 4200,
  "remaining_source": "580000000000000000",
  "converted_target": "1450000000",
  "liquidity": "123456789",
  "fees": {
    "token0": "1200000000000000",
    "token1": "900000"
  },
  "rerange_count": 3,
  "last_rerange_at": 1760000000,
  "actionability": {
    "can_rerange": true,
    "cooldown_passed": true,
    "will_close": false,
    "next_lower_tick": -195900,
    "next_upper_tick": -195000
  }
}
```

## Agent Memory

Persist this minimal record:

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "order_key": "<order-key>",
  "owner": "<owner-address>",
  "vault": "<vault-address>",
  "order_index": 0,
  "intent": "sell_high",
  "from_token": "WETH",
  "to_token": "USDC",
  "target_tick": -195000,
  "trigger_ticks": 300,
  "created_at": 1760000000,
  "last_seen_status": "ACTIVE",
  "last_rerange_at": 1760000300,
  "last_progress_bps": 4200
}
```

Field provenance rules:

- `target_tick`, `trigger_ticks`, `created_at`, and vault linkage come from the
  live order or order state.
- `from_token` and `to_token` should be reconstructed from `token0`, `token1`,
  and `isSell`, then enriched with the integration's token metadata store.
- `intent` should be restored from creator-side context when available. If the
  agent is backfilling an unknown historical order, use a neutral value such as
  `unknown` rather than guessing between `sell_high`, `buy_low`, or a higher-level
  strategy label.
- If token metadata cannot be resolved consistently, persist raw token addresses
  and surface a warning instead of inventing symbols.

## Event Emissions For Agent Runtimes

Agents should normalize protocol observations into these runtime events:

- `POSITION_OPENED`
- `RANGE_EXITED`
- `RERANGE_AVAILABLE`
- `RERANGE_EXECUTED`
- `FEES_ACCRUED`
- `POSITION_COMPLETED`
- `POSITION_CLOSED`
- `ACTION_BLOCKED`

## Monitoring Cadence

- Active user-facing orders: every 5 to 15 minutes.
- Resolver candidate scans: every block to every 5 minutes, depending on gas
  and order universe.
- Passive portfolio reporting: every 30 to 60 minutes.
- Event log backfill: after every restart and after missed RPC intervals.

## Do Not

- Do not infer final order status from event logs alone.
- Do not mark an order completed unless `getOrderState` confirms completion or
  `OrderClosed` is final for the user's workflow.
- Do not trigger rerange purely because a range was exited; always preview.
- Do not treat `previewRerange` alone as permission to submit; also check
  `lastRerangeAt + hubConfig.rerangeCooldown` for permissionless reranges.
