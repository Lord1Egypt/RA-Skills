---
skill: strategy-composer
version: 1.0.0
category: rerange_strategy
---

# Strategy Composer Skill

Use this skill to turn portfolio or treasury objectives into sets of Rerange
orders. Rerange v1 orders have fixed targets and sliding liquidity windows;
complex strategies are composed by opening, monitoring, reranging, and closing
multiple bounded orders.

## Supported Strategy Modules

| Strategy | Composition |
| --- | --- |
| `productive_limit_order` | One order with target price and trigger band. |
| `passive_exit` | One or more sell orders above current price. |
| `buy_low_accumulation` | One or more buy orders below current price. |
| `dca` | Sequential or staggered orders with bounded capital per step. |
| `grid` | Multiple buy and sell orders around current price. |
| `rebalance` | Orders that move only the excess exposure above policy target. |
| `treasury_runway` | Passive exits from volatile assets into stable assets over bands. |

Do not present leverage, liquidation protection, derivatives, or cross-chain
execution as v1 protocol features.

## Required Inputs

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "owner": "<owner-address>",
  "objective": "passive_exit",
  "source_asset": "WETH",
  "target_asset": "USDC",
  "total_amount": "10",
  "bands": [
    {
      "target_price": 3500,
      "amount": "2.5",
      "trigger_bps": 300
    },
    {
      "target_price": 3800,
      "amount": "2.5",
      "trigger_bps": 300
    }
  ],
  "max_asset_exposure_pct": 40,
  "max_orders": 8
}
```

## Planning Rules

1. Check portfolio balances and existing open Rerange orders.
2. Enforce user exposure, concentration, and order-count limits.
3. Split capital only when multiple orders materially improve execution
   control.
4. Use `intent-order-builder` for each proposed order.
5. Use `safety-risk` to simulate each order and the aggregate strategy.
6. Return a plan with explicit order parameters and monitoring policy.

## DCA Pattern

For accumulation over time:

- create one order for the current step,
- wait for completion, close, or timeout before opening the next step, or
- create staggered bounded orders only if the user approved simultaneous
  capital deployment.

Avoid claiming time-based execution if no scheduler is attached.

## Grid Pattern

For grid execution:

- place buy orders below current price and sell orders above current price,
- cap per-band capital,
- cap total active orders,
- monitor aggregate exposure after every fill,
- do not automatically replace completed bands unless the user approved a grid
  maintenance policy.

## Output Shape

```json
{
  "strategy": "passive_exit",
  "chain_id": "<chain-id-from-deployments>",
  "orders": [
    {
      "intent": "sell_high",
      "from_token": "WETH",
      "to_token": "USDC",
      "amount": "2.5",
      "target_price": 3500,
      "trigger_bps": 300,
      "status": "previewed"
    }
  ],
  "aggregate": {
    "total_source_amount": "10",
    "max_active_orders": 4,
    "estimated_target_exposure_after_completion": "USDC"
  },
  "monitoring": {
    "position_check_minutes": 10,
    "rerange_evaluation_minutes": 15,
    "rebalance_review_hours": 24
  }
}
```

## Do Not

- Do not open many overlapping orders when one order satisfies the intent.
- Do not reinvest proceeds into a new order without explicit policy.
- Do not hide the difference between an order target and a guaranteed execution
  price.
- Do not use static APR estimates as the primary reason to enter a strategy.
