---
skill: safety-risk
version: 1.0.0
category: rerange_safety
---

# Safety And Risk Skill

Use this skill as a mandatory preflight for all Rerange actions. It defines the
checks agents must perform before opening, reranging, closing, or composing
orders.

## Global Checks

Every transaction path must verify:

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
- gas cost is acceptable for the action.

Close is the exception to the pause check: `close(orderKey)` is an owner or
manager recovery path and may be used while the hub is paused, after preview and
authorization checks.

## Open Checks

Before `open` or `open2`:

- `previewOpen(owner, params)` succeeds,
- if the user flow expects immediate activation, preview returns a non-empty
  activation plan,
- current tick has not drifted beyond the adapter policy since preview,
- target price is above current price for `sell_high`,
- target price is below current price for `buy_low`,
- allowance, Permit2 permit, or vault prefunding covers `capital`,
- if native ETH is supplied, the source token is the configured WETH and the
  value does not exceed the missing source-token amount,
- pool liquidity is sufficient for the order size,
- slippage and TWAP settings are not disabled accidentally.

## Rerange Checks

Before `rerange`:

- order is not closed,
- cooldown has elapsed,
- `previewRerange(orderKey)` succeeds,
- preview indicates close or activation,
- adapter safety checks pass,
- expected resolver reward justifies gas if running permissionlessly,
- transaction is submitted quickly enough that preview remains fresh.

Permissionless `rerange(orderKey)` enforces protocol cooldown. Manager policy
updates through the overload should still apply an explicit strategy cooldown
unless the user approved urgent intervention.

## Close Checks

Before `close`:

- caller is owner or authorized agent,
- `previewClose(orderKey)` succeeds,
- user understands whether balances return to owner or stay in vault,
- expected fees and protocol rewards are explained in target and non-target
  token terms.

## Risk Limits

Recommended default limits for autonomous agents:

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

User policy can tighten these limits. Agents should not loosen them without
explicit approval.

## Fee Settlement Awareness

Rerange settlement is asset-aware:

- resolver reward is paid only from target-asset fees,
- referrer share is paid only from non-target-asset fees,
- treasury receives remaining non-target-asset fees,
- target-asset fees are not routed to referrer or treasury,
- non-target-asset fees are not routed to resolver.

Agents must model rewards and user proceeds using this split.

## Circuit Breakers

Stop opening new orders and switch to read-only monitoring when:

- hub is paused,
- RPC responses disagree across providers,
- pool tick diverges materially from TWAP,
- indexed pool liquidity is stale,
- gas spikes above user policy,
- token metadata is inconsistent,
- preview and simulation disagree.

## Output Shape

```json
{
  "approved": false,
  "blocking_reasons": [
    "hub_paused",
    "preview_reverted"
  ],
  "warnings": [
    "pool_liquidity_is_stale"
  ],
  "checks": {
    "chain_supported": true,
    "hub_unpaused": false,
    "adapter_allowed": true,
    "preview_passed": false,
    "simulation_passed": null,
    "gas_policy_passed": true
  }
}
```

## Do Not

- Do not bypass preview to save RPC calls.
- Do not treat fee APR as guaranteed yield.
- Do not promise exact fill price; concentrated liquidity execution depends on
  path, liquidity, fees, and market movement.
- Do not execute with unknown token metadata.
- Do not use owner withdrawal functions from an autonomous resolver.
