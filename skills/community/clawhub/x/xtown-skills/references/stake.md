---
name: Liquid Staking
description: Stake BNB for slisBNB (or unstake) at the Lista DAO building in BNBTown (BNB Chain Mainnet).
building: Lista DAO
building_id: lista
---

# Stake Skill

Stake BNB for slisBNB (or unstake) at the Lista DAO building on BNB Chain (Mainnet).

## When to Use

Owner says something like:
- "Stake 0.5 BNB"
- "Unstake my slisBNB"
- "Stake BNB"

## Params (ask owner to confirm)

| Param | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `action` | string | ✅ | `"stake"`, `"unstake"`, or `"withdraw"` | `stake` |
| `amount` | string | ✅ | Amount for stake/unstake (**min 0.001 BNB for unstake**; use "0" for withdraw) | `0.5` |

> [!IMPORTANT]
> **Unstaking Notice**: Unstaking slisBNB at Lista DAO involves a **7-8 day withdrawal period**. During this time, your funds are locked and the request cannot be canceled. You will need to return to the building after the period ends to claim your BNB.

---

## Report to Owner

Template:
```
✅ Stake completed!
Staked: {amount} BNB → {result.outputAmount} slisBNB
Tx Hash: {result.txHash}
BscScan: https://bscscan.com/tx/{result.txHash}
```

---

# Liquid Staking API Reference

## Query Protocol Stats

Ask the owner something like:
- "How much BNB is staked in Lista?"
- "What's my slisBNB balance?"
- "Can I claim my BNB yet?"
- "How much BNB do I have staked in Lista?"

### Stats API

```http
GET $XTOWN_SERVER_URL/agent/stats?session_token=<token>&skill_id=lista
```

### Result Schema
```json
{
  "bnb": "0.1234",
  "slisBNB": "0.4980", 
  "stakedBNB": "0.4980", // Current staked slisBNB balance
  "withdrawalRequests": [
    {
      "uuid": "1",
      "amountInSlisBNB": "0.001",
      "startTime": 1710330000,
      "isClaimable": false // True if 7-8 days have passed
    }
  ]
}
```

---

## Pre-flight Balance Check

Before execution, **the agent MUST verify the wallet balance**:
1. **Identify Asset**: BNB (for `stake`) or slisBNB (for `unstake`).
2. **Query Balance**: Use the methods described in the [wallet skill](./wallet.md).
3. **Compare**:
   - If `stake` BNB: Ensure `balance >= amount + 0.001`.
   - If `unstake` slisBNB: Ensure `amount >= 0.001` AND `bnb_balance >= 0.001` AND `slisBNB_balance >= amount`.
   - If `amount < 0.001` for `unstake`, report: "[ERROR] Minimum unstake amount is 0.001 BNB. Please enter a valid amount."
4. **Guard**: If balance is insufficient, **DO NOT EXECUTE**. Instead, report:
   "[ERROR] Insufficient {asset} balance. You have {current_balance} {asset}, but need {required} {asset}. Please top up your wallet: {wallet_address}"

---

## Execute

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "action": "stake",
    "amount": "0.1"
  }
}
```

## Result

```json
{
  "status": "completed",
  "result": {
    "txHash": "0xjkl...",
    "outputAmount": "0.498",
    "network": "BNB Chain (Mainnet)"
  }
}
```
