---
name: Token Swap
description: Swap between mainstream tokens ($BNB, $USDT, etc.) and any ERC-20 token at the PancakeBank DEX building in BNBTown.
building: PancakeBank (DEX)
building_id: dex
---

# Swap Skill

Swap between mainstream tokens and any ERC-20 token at the PancakeBank DEX building using PancakeSwap on BSC.

## When to Use

Owner says something like:
- "Buy CAKE with 0.01 BNB" (BNB -> ERC20)
- "Sell my CAKE for USDT" (ERC20 -> USDT)
- "Swap 100 USDT for $UB" (Mainstream -> Mainstream)
- "Buy $CAKE with 0.1 BNB"
- "Swap all $CAKE for BNB"

> [!CAUTION]
> **PREVENT ACCIDENTAL BNB SPENDING**: When the user says **"Sell [Token]"**, the input is the [Token]. 
> - `token_in` = [Token Address]
> - `token_out` = "BNB"
> - `amount_in` = Amount of [Token] to sell
> **DO NOT** send BNB amount as `amount_in` for a sell order. If you do, the worker will try to swap BNB for the token instead.

## [WARNING] Execution Constraints (Anti-Hallucination)

To ensure transaction safety and prevent hallucinations, you **MUST** adhere to these rules:

1. **Network**: All transactions are executed strictly on the **BSC Chain** (`eip155:56`).
2. **Mandatory Token Match**: At least **one** side of the swap (`token_in` OR `token_out`) **MUST** be one of the following recognized assets:
    - **$BNB**: `0x0000000000000000000000000000000000000000`
    - **$WBNB**: `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c`
    - **$U**: `0xcE24439F2D9C6a2289F741120FE202248B666666`
    - **$UB**: `0x40b8129B786D766267A7a118cF8C07E31CDB6Fde`
    - **$USDC**: `0x8AC76a51cc950d9822D68b83fE1Ad97B32Cd580d`
    - **$USDT**: `0x55d398326f99059fF775485246999027B3197955`
    - **$CAKE**: `0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82`

**If neither token matches the list above, refuse the request and explain the safety constraint to the owner by showing the list of allowed assets.**

## Intent Mapping Rules

To accurately map the owner's request to parameters, follow these logic rules:

1. **"Buy [Token]"** (e.g., "Buy 1 CAKE with BNB"): 
   - `token_in` = "BNB"
   - `token_out` = [Token Address]
   - `amount_in` = Amount of **BNB** to spend

2. **"Sell [Token]"** (e.g., "Sell 10 CAKE"):
   - `token_in` = [Token Address]
   - `token_out` = "BNB"
   - `amount_in` = Amount of **[Token]** to spend/sell

3. **"Swap [TokenA] for [TokenB]"**:
   - `token_in` = [TokenA Address]
   - `token_out` = [TokenB Address]
   - `amount_in` = Amount of **[TokenA]** to spend

**CRITICAL**: In a "Sell" request, `token_in` is the asset the user is giving away. Always double-check the balance of `token_in` before proceeding.

## Params (ask owner to confirm)

| Param | Type | Required | Description | Example |
|-------|------|----------|-------------|---------|
| `token_in` | string | optional | Input token address or "BNB" (default: "BNB") | `BNB` or `0x000...0` |
| `token_out` | string | optional | Output token address or "BNB" (default: "BNB") | `0x0E09Fa...` or `BNB` |
| `amount_in` | string | required | Amount of **token_in** to spend/sell | `0.01` |
| `slippage` | number | optional | Slippage tolerance % (default: 5) | `5` |

> [!IMPORTANT]
> **At least one** of `token_in` or `token_out` **MUST** be explicitly provided in the request to define the swap pair. If both are missing, the trading pair cannot be determined.

---

## Report to Owner

Template:
```
✅ Swap completed!
Spent: {amount_in} {token_in}
Received: {result.amountOut} {token_out}

Transactions:
- Explorer Link: {result.explorerUrl}{result.txHashes[result.txHashes.length-1]}
```

On failure:
```
[ERROR] Swap failed: {errorMessage}
```

---

# Token Swap API Reference

## Pre-flight Balance Check

Before execution, **the agent MUST verify the wallet balance**:
1. **Query Balance**: Use `eth_getBalance` for BNB or `eth_call` (erc20 balance) for tokens.
2. **Ensure Sufficient**: Ensure you have enough of `token_in` to cover `amount_in` plus estimated gas.
3. **Guard**: If balance is insufficient, report:
   "[ERROR] Insufficient {token_in} balance. Please top up your wallet: {wallet_address}"

---

## Execute

### Example 1: BNB to ERC20 (Buy)
```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "token_in": "BNB",
    "token_out": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "amount_in": "0.01",
    "slippage": 5
  }
}
```

### Example 2: ERC20 to Mainstream (Sell)
```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "token_in": "0x0E09FaBB73Bd3Ade0a17ECC321fD13a19e81cE82",
    "token_out": "0x55d398326f99059fF775485246999027B3197955",
    "amount_in": "10",
    "slippage": 5
  }
}
```

## Result

```json
{
  "status": "completed",
  "result": {
    "txHashes": ["0x..."],
    "amountOut": "1.234",
    "network": "BSC"
  }
}
```
