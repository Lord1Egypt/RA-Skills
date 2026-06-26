---
skill: intent-order-builder
version: 1.0.0
category: rerange_execution
---

# Intent Order Builder Skill

Use this skill to convert a user intent into a previewed Rerange order. Agents
should prefer this skill over direct raw contract construction.

## Supported Intents

| Intent | Translation |
| --- | --- |
| `sell_high` | Sell source token into target token as price moves up toward target. |
| `buy_low` | Sell quote token into base token as price moves down toward target. |
| `passive_exit` | Gradually exit an existing asset position at or beyond target. |
| `rebalance_step` | Move a bounded amount from overweight asset to underweight asset. |

DCA and grid strategies are composed from multiple orders by the
`strategy-composer` skill.

## Required Inputs

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

`risk_profile` is optional, but if it is accepted by an integration it must map
to explicit adapter policy values rather than free-form heuristics.

## Construction Rules

1. Resolve deployment, tokens, adapters, and candidate pools with
   `protocol-discovery`.
2. Convert `amount` into raw token units using the source token decimals.
3. Canonically sort the pool pair into `token0` and `token1`.
4. Set `isSell = true` when the source token is `token0`; otherwise set it to
   `false`.
5. Convert `target_price` into `targetTick` using canonical pool token order.
6. Convert `trigger_bps` into `triggerTicks`, or default to the tick distance
   between current price and target.
7. Resolve `risk_profile` into concrete defaults before encoding `adapterConfig`.
8. Encode adapter config with pool, fee tier, TWAP settings, tick drift policy,
   and slippage policy.
9. Call `previewOpen(owner, params)`.
10. Return unsigned transaction parameters only after preview succeeds.

## Risk Profile Defaults

If the integrating app exposes `risk_profile`, use a deterministic mapping such as:

```json
{
  "conservative": {
    "max_slippage_bps": 50,
    "max_twap_deviation_ticks": 50,
    "max_tick_deviation": 50
  },
  "moderate": {
    "max_slippage_bps": 100,
    "max_twap_deviation_ticks": 100,
    "max_tick_deviation": 100
  },
  "aggressive": {
    "max_slippage_bps": 150,
    "max_twap_deviation_ticks": 150,
    "max_tick_deviation": 150
  }
}
```

If no mapping is configured, ignore `risk_profile` and require the concrete
adapter policy fields directly.

## CreateOrderParams Mapping

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

## Output Shape

```json
{
  "status": "previewed",
  "chain_id": "<chain-id-from-deployments>",
  "hub": "<hub-address-from-deployments>",
  "method": "open",
  "params": {
    "vault": "<vault-address-or-zero-address>",
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
  },
  "preview": {
    "vault": "<resolved-vault-address>",
    "current_tick": -196200,
    "lower_tick": -196200,
    "upper_tick": -195000,
    "tick_spacing": 60,
    "activates_immediately": true
  },
  "preflight": {
    "approval_required": true,
    "permit2_supported": true,
    "estimated_gas": "0"
  }
}
```

Interpret preview results carefully:

- `previewOpen` is an informative preview of vault resolution and market state.
- If the returned activation plan is empty, the agent must label the order as
  deferred or inactive rather than immediately executable.
- For immediate-open UX, require a non-empty activation plan before presenting
  the order as ready to submit.

## Execution Methods

- Use `open(params)` after ERC20 approval or when the vault is prefunded.
- Use `open2(params, permit, signature)` when the owner provides Permit2.
- Use `previewOpen(owner, params)` every time before transaction submission.

## Funding Modes

`open` resolves the vault, then requires the vault to hold `capital` in the
source token by the time execution starts. Agents must choose one funding path:

- prefund the resolved vault with the source token,
- approve the hub so `open` can transfer only the missing source-token amount,
- send native value only when the source token is the configured WETH and the
  flow intentionally wraps native ETH,
- use `open2` with a valid Permit2 signature for the source token.

If allowance is missing and the vault is not prefunded, `open` will not create a
funded order. Treat funding failure as a blocking preflight error, not as a
recoverable strategy state.

## Agent Refusals

Do not build or submit an order when:

- the target price is on the wrong side of current price for the stated intent,
- `capital` is zero or below the user's minimum practical order size,
- hub is paused,
- adapter is not allowed,
- `previewOpen` reverts, or returns an empty activation plan for a flow that
  requires immediate activation,
- current tick has drifted materially since preview,
- funding cannot be proven through vault balance, ERC20 allowance, native ETH
  wrap, or Permit2,
- the user asks the agent to bypass slippage, TWAP, or liquidity checks.
