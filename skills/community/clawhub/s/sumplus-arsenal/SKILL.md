---
name: arsenal
description: Execute DeFi skills on Ethereum, Sui, Solana, and 10+ chains via Arsenal. Use for swaps, lending, liquidity, portfolio queries, and any blockchain operation.
metadata: {"openclaw":{"emoji":"⚔️","primaryEnv":"ARSENAL_API_KEY","requires":{"env":["ARSENAL_API_KEY"]},"homepage":"https://arsenal.sumplus.xyz"}}
---

# Arsenal — DeFi Execution Layer

Arsenal is Sumplus's on-chain execution platform. When the user asks for anything blockchain-related — swaps, lending, balances, liquidity positions — call Arsenal.

**Base URL:** `https://arsenal.sumplus.xyz`
**Auth:** `Authorization: Bearer {ARSENAL_API_KEY}` (inject from env, never ask the user)

---

## Step 1 — Discover the right skill

```
GET /api/skills?search={intent}&limit=5
```

Always search first. Don't guess a skill_id.

```bash
# Example: user wants to swap on Sui
curl "https://arsenal.sumplus.xyz/api/skills?search=cetus+swap+sui&limit=5"
```

Response includes `id`, `name`, `schema.input` (what params to send), `schema.output` (what comes back).

---

## Step 2 — Execute the skill

```
POST /api/execute
Authorization: Bearer {ARSENAL_API_KEY}
Content-Type: application/json

{
  "skill_id": "<id from Step 1>",
  "input": {
    "action": "<action>",
    ... other params from schema.input
  }
}
```

**Every call requires `action`.** Check the skill's `schema.input` for the full list.

---

## Common input parameters

| Param | Description |
|---|---|
| `action` | Required. Which operation: `get_quote`, `build_swap_tx`, `get_markets`, etc. |
| `sender` | Wallet address. EVM: `0x...` (40 hex). Sui: `0x...` (64 hex). |
| `tokenIn` / `token_in` | Input token symbol (`ETH`, `USDC`) or contract address |
| `tokenOut` / `token_out` | Output token |
| `amountIn` / `amount_in` | Human-readable amount string: `"0.1"`, `"100"` |
| `slippage` | Decimal, default `0.01` (= 1%) |
| `chain` | Chain name: `ethereum`, `optimism`, `arbitrum`, `base`, `bsc`, `solana` |

---

## Reading the response

### Quote (`get_quote`)
```json
{
  "amount_in": "0.1",
  "amount_out": "243.52",
  "price_impact": "0.04%",
  "fee": "0.3%"
}
```
Show this to the user. Ask if they want to proceed before building a transaction.

### EVM transaction (`build_swap_tx`)
```json
{
  "transactions": [
    { "to": "0x...", "data": "0x...", "value": "0x0", "description": "Approve WETH" },
    { "to": "0x...", "data": "0x...", "value": "0x0", "description": "Swap WETH → USDC" }
  ],
  "amount_out_estimated": "243.52",
  "amount_out_minimum": "241.1"
}
```
**Execute `transactions` in order.** Each tx must confirm before sending the next.

### Sui transaction (`build_swap_tx`)
```json
{
  "tx_bytes": "<base64 PTB>",
  "instructions": ["Pass tx_bytes to any Sui wallet to sign and submit."]
}
```
Pass `tx_bytes` to Privy `send_sui_transaction` or the user's Sui wallet.

### Solana transaction (`build_swap_tx`)
```json
{
  "transaction": "<base64 VersionedTransaction>",
  "amount_in": "0.1",
  "amount_out": "14.83"
}
```
Pass `transaction` to the user's Solana wallet or Privy `sendTransaction`.

---

## Available skills (quick reference)

**EVM (Ethereum, Optimism, Arbitrum, Base, Polygon, BSC)**
- Uniswap V3 — `get_quote`, `build_swap_tx`
- Velodrome V2 — `get_quote`, `build_swap_tx` (Optimism only)
- PancakeSwap V3 — `get_quote`, `build_swap_tx`, `get_pool_info`
- Aave — `get_markets`, `get_reserves`, `get_user_account`, `get_user_supplies`, `get_user_borrows`
- GMX — `get_markets`, `get_position`, `get_funding_rates`
- Hyperliquid — `get_markets`, `get_orderbook`, `get_user_positions`

**Sui**
- Cetus CLMM — `get_quote`, `build_swap_tx`, `get_pool_info`, `get_pools`, `get_position`
- Bluefin Ember — `list_vaults`, `get_vault_info`, `get_user_position`, `deposit`, `withdraw`
- Aftermath Finance — `get_pools`, `get_pool_info`, `get_quote`, `build_swap_tx`
- Navi Protocol — `get_markets`, `get_user_position`, `get_reserve_data`
- Scallop — `get_markets`, `get_user_position`
- Suilend — `get_markets`, `get_user_position`
- SUI Blockchain Toolkit — `get_balance`, `get_tokens`, `get_nfts`, `get_transactions`

**Solana**
- Jupiter — `get_quote`, `build_swap_tx`, `get_token_price`
- Raydium — `get_pools`, `get_pool_info`, `get_quote`

**Cross-chain**
- Crypto Wallet Manager — `get_balance`, `get_tokens`, `get_transactions`
- Sumplus Yield Optimizer — `get_recommendations`, `compare_protocols`

---

## Error handling

| Status | Meaning | Action |
|---|---|---|
| 400 | Bad input / missing field | Check `details.fieldErrors`, fix params |
| 401 | Invalid or missing API key | Check `ARSENAL_API_KEY` env var |
| 404 | Skill not found | Re-search with different keywords |
| 422 | Skill ran but failed logically (no pool, bad amount) | Tell user, suggest alternatives |
| 500 | Infrastructure error | Retry once, then report to user |

---

## Workflow example

**User:** "Swap 0.5 SUI for USDC on Cetus"

1. Search: `GET /api/skills?search=cetus+swap+sui`
2. Find Cetus CLMM skill, note its `id`
3. Get quote: `POST /api/execute` with `action: "get_quote"`, `tokenIn: "SUI"`, `tokenOut: "USDC"`, `amountIn: "0.5"`
4. Show user: "You'll receive ~12.3 USDC. Proceed?"
5. Build tx: `POST /api/execute` with `action: "build_swap_tx"`, `sender: "<user_address>"`, same tokens + amount
6. Return `tx_bytes` to user's Sui wallet for signing

---

## Sign-up / API key

If the user needs an Arsenal API key:
```
POST https://arsenal.sumplus.xyz/api/auth/signup
{ "email": "...", "password": "...", "role": "agent" }
```
Then: `POST /api/auth/apikey` (with JWT) → `{ "api_key": "sk_live_..." }`
