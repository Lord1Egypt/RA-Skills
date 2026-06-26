---
name: Token Launch
description: Launch a new meme token at the Four.meme building in BNBTown (BNB Chain Mainnet).
building: Four.meme
building_id: fourMeme
---

# Launch Skill

Launch a new meme token at the Four.meme building on BNB Chain (Mainnet).

## When to Use

Owner says something like:
- "Launch a token called Moon Coin"
- "Create a new meme token DINU"
- "Launch token" / "Create token"

## Params (ask owner to confirm)

| Param | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `token_name` | string | required | Name of the token. Required if `token_symbol` is missing. | `Moon Coin` |
| `token_symbol`| string | required | Ticker symbol (short name). Required if `token_name` is missing. | `MOON` |
| `description` | string | optional | Token description. Default: Bio generated from name. | `To the moon!` |
| `image_url`   | string | optional | Token logo URL. Default: Four.meme logo. | `https://example.com/logo.png` |
| `label`       | string | optional | Category (Meme, AI, Defi, etc). Default: Others. | `AI` |

---

## Report to Owner

Template:
```
✅ Token launched!
Name: {token_name} ({token_symbol})
Contract: {result.tokenAddress}
Tx Hash: {result.txHash}
BscScan: https://bscscan.com/tx/{result.txHash}
```

---

# Token Launch API Reference

## Pre-flight Balance Check

Before execution, **the agent MUST verify the wallet balance**:
1. **Query BNB Balance**: Use the `eth_getBalance` method described in the [wallet skill](./wallet.md).
2. **Compare**: Ensure `balance >= 0.011` (0.01 fee + 0.001 gas).
3. **Guard**: If balance is insufficient, **DO NOT EXECUTE**. Instead, report:
   "[ERROR] Insufficient BNB balance for launch. You have {current_balance} BNB, but need 0.015 BNB. Please top up your wallet: {wallet_address}"

---

## Execute

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "token_name": "My AI Token",
    "token_symbol": "MAIT",
    "description": "The first token launched by an AI agent on BNB",
    "image_url": "https://example.com/token.png",
    "label": "AI Agent"
  }
}
```

## Result

```json
{
  "status": "completed",
  "result": {
    "tokenAddress": "0x...",
    "txHash": "0xghi...",
    "network": "BNB Chain (Mainnet)"
  }
}
```
