---
name: stableops-lifi-treasury
description: Use this skill when a team, DAO, or builder wants to deploy USDC from a stablecoin treasury into LI.FI Earn vaults under explicit treasury policy limits, prepare a Composer deposit, and produce a receipt-token execution report.
---

# StableOps LI.FI Treasury

Use this skill for governed treasury execution powered by `LI.FI Earn` and `Composer`.

StableOps is for small teams, DAOs, and indie builders. It should not be framed as a personal wallet yield helper. The workflow starts from treasury rules and only then moves to vault discovery and Composer execution.

## When To Use

- The user wants to manage a team, DAO, builder, or stablecoin treasury.
- The user gives rules like reserve target, max per execution, allowed chains, safe vaults only, or minimum TVL.
- The user wants to deploy USDC into an Earn vault with a policy-backed explanation.
- The user wants a report describing vault, protocol, chain, transaction hash, and receipt token.

Example requests:

```text
Use StableOps to deploy 1 USDC from our team treasury into a safe LI.FI Earn vault on Base.
Run a treasury policy check: keep 60% reserve, max 5 USDC per execution, Base or Arbitrum only.
Prepare a Composer deposit for our builder treasury and explain the receipt token after execution.
```

## Workflow

1. Extract the treasury policy:
   - treasury name
   - treasury size in USDC
   - deploy amount in USDC
   - reserve target
   - max per execution
   - allowed chains
   - risk mode
   - minimum TVL

2. Build a StableOps plan:

```bash
curl -sS -X POST http://localhost:3017/api/plan \
  -H 'Content-Type: application/json' \
  -d '{
    "policy": {
      "treasuryName": "Builder Treasury",
      "treasurySizeUsd": 100,
      "deployAmountUsd": 1,
      "reservePct": 60,
      "maxPerExecutionUsd": 5,
      "minTvlUsd": 5000000,
      "riskMode": "conservative",
      "allowedChainIds": [8453, 42161]
    }
  }'
```

3. Use the returned `plan` fields:
   - `recommendedVault`
   - `approvedVaults`
   - `rejectedVaults`
   - `checks`
   - `agents`
   - `reportPreview`

4. Only prepare Composer quote when all blocking checks pass:

```bash
curl -sS -X POST http://localhost:3017/api/quote \
  -H 'Content-Type: application/json' \
  -d '{
    "chainId": 8453,
    "vaultAddress": "<vault-address>",
    "walletAddress": "<treasury-wallet>",
    "fromAmountUsd": 1,
    "fromTokenAddress": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
    "assetDecimals": 6
  }'
```

5. For execution:
   - connect the treasury wallet
   - switch to the selected chain
   - approve USDC if required
   - submit the Composer transaction
   - wait for confirmation

6. After execution, return a treasury report:
   - deployed amount
   - vault name
   - protocol
   - chain
   - deposit transaction hash
   - receipt token symbol
   - plain-language explanation of what the receipt token represents

## Output Rules

- Lead with the treasury decision: approved or blocked.
- Mention policy checks before APY.
- Do not recommend a vault that fails the policy.
- Do not create a Composer quote if reserve, max execution, chain, TVL, or Composer support fails.
- Explain receipt tokens plainly: a receipt token represents the treasury's position in the selected vault.
- If live LI.FI Earn discovery is unavailable, say that seeded examples are being used.

