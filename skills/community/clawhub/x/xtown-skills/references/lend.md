---
name: Lending & Borrowing
description: Supply or borrow assets at the Venus Protocol building in BNBTown (BSC Mainnet).
building: Venus
building_id: venus
---

# Lend Skill

Supply or borrow assets at the Venus Protocol building on BSC Mainnet.

## When to Use

Owner says something like:
- "Supply 0.1 BNB to Venus"
- "Borrow 100 USDT"
- "Supply assets" / "Borrow"

## Params (ask owner to confirm)

| Param | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `action` | string | ✅ | `"supply"` or `"borrow"` | `supply` |
| `asset` | string | ✅ | Asset symbol | `BNB`, `USDT`, `BTCB` |
| `amount` | string | ✅ | Amount to supply or borrow | `0.1` |

---

## Report to Owner

Template:
```
✅ {action} completed!
Asset: {amount} {asset}
APY: {result.apy}
Tx Hash: {result.txHash}
BscScan: https://bscscan.com/tx/{result.txHash}
```

---

# Lending & Borrowing API Reference

## Query Protocol Stats

Ask the owner something like:
- "How much BNB do I have in Venus?"
- "What's my borrow balance?"
- "How much do I have in Venus?"

### Stats API

```http
GET $XTOWN_SERVER_URL/agent/stats?session_token=<token>&skill_id=venus
```

### Result Schema
```json
{
  "bnb": "1.5000",
  "vbnb": "75.12345678",
  "vbnbValueBNB": "1.4950", // This is your REDEEMABLE BNB balance
  "wbnb": "0.0000"
}
```

---

## Pre-flight Balance Check

Before execution, **the agent MUST verify the wallet balance**:
1. **Identify Asset**: Determine if it's BNB or an ERC20 asset.
2. **Query Balance**: Use the methods described in the [wallet skill](./wallet.md).
3. **Compare**:
   - If `supply` BNB: Ensure `balance >= amount + 0.001`.
   - If `supply` ERC20: Ensure `bnb_balance >= 0.001` AND `token_balance >= amount`.
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
    "action": "supply",
    "asset": "BNB",
    "amount": "0.1"
  }
}
```

## Result

```json
{
  "status": "completed",
  "result": {
    "txHash": "0xdef...",
    "apy": "3.2%",
    "network": "BSC Mainnet"
  }
}
```
