---
skill: vault-manager
version: 1.0.0
category: rerange_custody_boundary
---

# Vault Manager Skill

Use this skill for owner-authorized vault workflows: creating vaults, assigning
time-limited agents, selecting balance policy, closing orders, and reporting
vault balances.

Rerange vaults are non-custodial execution smart accounts. The vault owns LP
positions and may hold tokens, but only the owner can withdraw assets.

## Owner Actions

- `RerangeHub.createVault()`
- `RerangeVault.setAgent(agent, accessExpiresAt)`
- `RerangeHub.close(orderKey)` when owner-authorized
- `RerangeVault.withdraw(token, to, amount)`
- `RerangeVault.call(target, value, data)` for explicit owner-approved calls
- `RerangeVault.multicall(targets, values, data)` for explicit owner-approved
  batches

`RerangeVault.withdraw(token, amount)` and `withdrawNative(weth, amount)` are
hub-mediated return paths used by protocol close settlement. They are not direct
owner entry points.

## Manager Actions

A configured vault agent can manage orders where supported by the hub and vault,
but must not be given withdrawal authority.

Use `setAgent(agent, accessExpiresAt)` for session-key-like delegation:

```json
{
  "agent": "<agent-address>",
  "access_expires_at": 1760000000,
  "scope": "order_management_only"
}
```

## Balance Policy

When opening an order, choose:

- `keepBalancesInVault = false`: close flow returns attributable balances to
  the owner.
- `keepBalancesInVault = true`: final balances remain in vault for later
  strategies.
- `unwrapOut = true`: unwrap WETH output to native ETH where supported.

Treasury and portfolio agents should prefer `keepBalancesInVault = true` when
they plan chained strategies from the same vault.

## Required Reads

- `RerangeHub.vaults(owner)`
- `RerangeHub.predictVault(owner, vaultIndex)`
- `RerangeHub.vaultOrderCount(vault)`
- ERC20 `balanceOf(vault)` for supported tokens
- `RerangeVault.owner()`
- `RerangeVault.isManager(agent)`
- `RerangeVault.agents(agent)`

## Output Shape

```json
{
  "owner": "<owner-address>",
  "vaults": [
    {
      "address": "<vault-address>",
      "index": 0,
      "orders": 4,
      "balances": [
        {
          "token": "USDC",
          "raw_amount": "1500000000"
        }
      ],
      "managers": [
        {
          "agent": "<agent-address>",
          "access_expires_at": 1760000000,
          "active": true
        }
      ]
    }
  ]
}
```

## Close Policy

Before closing:

1. Read `getOrderState(orderKey)`.
2. Call `previewClose(orderKey)`.
3. Explain expected returned tokens, fees, and reward settlement.
4. Submit `close(orderKey)` only from an owner or authorized agent context.
5. Confirm with `OrderClosed` and final vault or owner token balances.

`close(orderKey)` is the owner or manager escape hatch and is available through
the hub even when new opens or reranges are paused. Agents should still preview
close and explain settlement before submitting.

## Do Not

- Do not request or store private keys.
- Do not ask users to delegate unlimited wallet authority.
- Do not call vault `withdraw` from an automation agent.
- Do not use arbitrary vault `call` unless the owner explicitly requested the
  exact target, value, calldata purpose, and risk.
