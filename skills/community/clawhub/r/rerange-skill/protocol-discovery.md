---
skill: protocol-discovery
version: 1.0.0
category: rerange_core
---

# Protocol Discovery Skill

Use this skill before any other Rerange action. It resolves the chain,
deployment, adapters, tokens, pools, vaults, order keys, and live hub config
needed by higher-level skills.

## When To Use

- The agent receives an intent such as "sell WETH into USDC above 3500".
- The agent needs to monitor or rerange an order but only knows an owner, vault,
  or order index.
- The agent needs to verify whether a chain, adapter, token pair, or pool is
  supported.
- The agent needs current protocol configuration before sending a transaction.

## Required Inputs

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

Only `chain_id` is always required. Other fields are used when available.

Interpret optional identifiers in this priority order:

1. `order_key`
2. `(vault, order_index)`
3. `vault`
4. `owner`

## Required Reads

- Deployment metadata from the SDK config or generated deployment exports.
- `RerangeHub.hubConfig()`
- `RerangeHub.adapters(adapter)`
- `RerangeHub.vaults(owner)` as the next vault index upper bound, not a vault array
- `RerangeHub.predictVault(owner, vaultIndex)`
- `RerangeHub.vaultOrderCount(vault)`
- `RerangeHub.getOrderKey(vault, orderIndex)`
- `RerangeHub.getOrder(orderKey)` when reconstructing order metadata from an existing order
- `RerangeHub.getOrderState(orderKey)`

## Output Shape

```json
{
  "chain_id": "<chain-id-from-deployments>",
  "network": "<network-from-deployments>",
  "hub": "<hub-address-from-deployments>",
  "adapters": {
    "uniswap_v3": "<v3-adapter-address-from-deployments>",
    "uniswap_v4": "<v4-adapter-address-from-deployments>"
  },
  "hub_config": {
    "paused": false,
    "rerange_cooldown": 300,
    "completion_threshold_bps": 8,
    "resolver_share_bps": 5000,
    "referrer_share_bps": 1000
  },
  "tokens": {
    "source": {
      "symbol": "WETH",
      "address": "<source-token-address-from-token-catalog>",
      "decimals": 18
    },
    "target": {
      "symbol": "USDC",
      "address": "<target-token-address-from-token-catalog>",
      "decimals": 6
    }
  },
  "vaults": ["<vault-address>"],
  "candidate_pools": [
    {
      "pool": "<pool-address-from-pool-catalog-or-indexer>",
      "fee_tier": 500,
      "adapter": "uniswap_v3"
    }
  ]
}
```

## Pool Selection Rules

Prefer pools that satisfy all of:

- pool token order matches canonical token order,
- adapter is allowed by the hub,
- pool has usable liquidity near the current tick,
- fee tier fits the user's execution horizon,
- route avoids unsupported or unknown tokens.

If several pools are valid, rank by live liquidity first, then historical volume,
then fee tier suitability. For large orders, do not choose a pool using static
metadata alone; require live or indexed liquidity data.

## Vault Resolution

For a new order with no explicit vault:

1. Read `vaults(owner)` to get the next vault index upper bound.
2. Call `predictVault(owner, vaultIndex)`.
3. Use that predicted address in `previewOpen`.
4. Let `open` create the vault if needed, or create it explicitly with
   `createVault`.

For an existing order:

1. If `(vault, orderIndex)` is known, compute or read `getOrderKey`.
2. If only `orderKey` is known, use `getOrderState`.
3. If only owner is known, enumerate `vaultIndex` from `0` up to `vaults(owner) - 1`,
   derive each vault with `predictVault(owner, vaultIndex)`, then inspect
   `vaultOrderCount(vault)` and `getOrderKey(vault, orderIndex)`.

## External Data Sources

Use this source priority so agents resolve the same pair consistently:

1. Canonical Rerange deployments and SDK exports for chain, hub, and adapter addresses.
2. A chain-specific token catalog controlled by the integrating app.
3. Live adapter or pool reads for current tick, tick spacing, and usable liquidity.
4. Indexed liquidity and volume data only as a ranking aid when live reads are insufficient.

If the token catalog or pool index is app-specific, the agent should report which
source it used in its output metadata.

## Failure Conditions

Return a blocking error when:

- chain is unsupported,
- hub is paused,
- adapter is not allowed,
- token is unsupported or ambiguous,
- no valid pool exists for the pair,
- order key cannot be resolved,
- required reads fail after retrying through a healthy RPC.
