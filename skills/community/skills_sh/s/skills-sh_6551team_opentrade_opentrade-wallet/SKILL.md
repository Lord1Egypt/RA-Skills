---
name: opentrade-wallet
description: "This skill should be used when the user asks to 'create a custodial wallet', 'create a managed wallet', 'get my wallet address', 'show my custodial account', 'custodial swap', 'swap with managed wallet', 'withdraw from custodial wallet', 'withdraw BNB', 'withdraw SOL', 'send native tokens from custodial wallet', or mentions creating, managing, swapping, or withdrawing with a custodial (managed/hosted) wallet. Only supports BSC and Solana networks. Do NOT use for non-custodial wallet operations, general balance queries (use opentrade-portfolio), or swap quotes without custodial execution (use opentrade-dex-swap)."
license: Apache-2.0
metadata:
  author: 6551
  version: "1.0.1"
  homepage: "https://www.newsliquid.com"
---

# OpenTrade Custodial Wallet

4 API endpoints for custodial wallet creation, account query, swap execution, and native token withdrawal.

> **IMPORTANT**: Custodial wallet only supports **BSC** and **Solana** networks.
>
> **IMPORTANT**: Newly created wallets have zero balance. You must deposit **BNB** (to the BSC address) or **SOL** (to the Solana address) before you can swap or withdraw. Do NOT send tokens from other chains (e.g., Ethereum, Polygon, Arbitrum) to these addresses — funds sent from unsupported chains will be lost.

## Pre-flight Checks

Every time before running any custodial wallet command, always follow these steps in order:

1. Find or create a `.env` file in the project root to load the API credentials:
  ```bash
  OPEN_TOKEN=your_token_here
  ```

  Get your API token at: https://www.newsliquid.com/mcp

  **Security warning**: Never commit .env to git (add it to .gitignore) and never expose credentials in logs, screenshots, or chat messages.

2. Set the base URL and auth header:
  ```bash
  BASE_URL="https://ai.6551.io"
  AUTH_HEADER="Authorization: Bearer $OPEN_TOKEN"
  ```

## Skill Routing

- For swap quotes (read-only price estimate) → use `opentrade-dex-swap`
- For token search / metadata → use `opentrade-token`
- For market prices → use `opentrade-market`
- For wallet balances / portfolio → use `opentrade-portfolio`
- For transaction broadcasting (non-custodial) → use `opentrade-gateway`
- For custodial wallet management → use this skill (`opentrade-wallet`)

## Quickstart

```bash
# 1. Create a custodial wallet (EVM + Solana)
curl -s -X POST "$BASE_URL/open/trader/custodial/create" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json"

# 2. Get custodial account addresses
curl -s "$BASE_URL/open/trader/custodial/account" \
  -H "$AUTH_HEADER"

# 3. Custodial swap (auto-sign + broadcast)
curl -s -X POST "$BASE_URL/open/trader/custodial/swap" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"chainIndex":"56","fromTokenAddress":"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","toTokenAddress":"0x55d398326f99059fF775485246999027B3197955","amount":"1000000000000000000","slippagePercent":"1"}'

# 4. Withdraw native tokens
curl -s -X POST "$BASE_URL/open/trader/custodial/withdraw" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"network":"bsc","to":"0xRecipientAddress","amount":1000000000000000000}'
```

## Command Index

| # | Endpoint | Method | Description |
|---|---|---|---|
| 1 | `/open/trader/custodial/create` | POST | 创建托管钱包（同时生成 EVM 和 Solana 地址） |
| 2 | `/open/trader/custodial/account` | GET | 获取托管钱包地址 |
| 3 | `/open/trader/custodial/swap` | POST | 托管钱包执行 DEX swap（自动签名+广播） |
| 4 | `/open/trader/custodial/withdraw` | POST | 从托管钱包提现原生代币（BSC/SOL） |

## Supported Networks

> **Custodial wallet only supports BSC and Solana.**

| Chain | chainIndex | Native Token | Withdraw Network |
|---|---|---|---|
| BSC | `56` | BNB | `bsc` |
| Solana | `501` | SOL | `sol` |

## Cross-Skill Workflows

### Workflow A: Create Wallet → Deposit → Check Balance → Swap

> User: "Create a custodial wallet and swap 1 BNB for USDT"

```
1. opentrade-wallet         POST /open/trader/custodial/create              → get evm_address, sol_address
       → Tell user to deposit BNB (BSC) or SOL (Solana) to the new address
       → WARNING: only accept BNB/SOL, do NOT send other chain assets
2. opentrade-portfolio opentrade portfolio all-balances --address <evm_address> --chains bsc
       → verify BNB balance >= 1 (user must have deposited first)
3. opentrade-wallet         POST /open/trader/custodial/swap
       {"chainIndex":"56","fromTokenAddress":"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
        "toTokenAddress":"0x55d398326f99059fF775485246999027B3197955",
        "amount":"1000000000000000000","slippagePercent":"1"}
       → returns tx_hash
```

**Data handoff**:
- `evm_address` from step 1 → `--address` in step 2
- Custodial swap auto-signs and broadcasts — no manual signing needed

### Workflow B: Swap Quote → Custodial Swap

> User: "Get a quote for swapping BNB to USDT, then execute with custodial wallet"

```
1. opentrade-dex-swap  opentrade swap quote \
       --from 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee \
       --to 0x55d398326f99059fF775485246999027B3197955 \
       --amount 1000000000000000000 --chain bsc
       → display quote: expected output, price impact
       ↓ user confirms
2. opentrade-wallet         POST /open/trader/custodial/swap
       → auto-sign and broadcast, returns tx_hash
```

### Workflow C: Withdraw After Swap

> User: "Swap BNB to USDT, then withdraw BNB to my external wallet"

```
1. opentrade-wallet         POST /open/trader/custodial/swap → swap tokens
2. opentrade-wallet         POST /open/trader/custodial/withdraw
       {"network":"bsc","to":"0xExternalWallet","amount":1000000000000000000}
       → returns tx_hash
```

**Note**: Withdraw only supports native tokens (BNB on BSC, SOL on Solana).

## Operation Flow

### Step 1: Identify Intent

- Create a new custodial wallet → `POST /open/trader/custodial/create`
- View custodial wallet addresses → `GET /open/trader/custodial/account`
- Execute a swap automatically → `POST /open/trader/custodial/swap`
- Withdraw native tokens → `POST /open/trader/custodial/withdraw`

### Step 2: Collect Parameters

- Missing wallet address → call `GET /open/trader/custodial/account` first, or create one with `POST /open/trader/custodial/create`
- Missing token addresses → use `opentrade-token` to search token by name
- Missing amount → ask user, remind to convert to minimal units
- Missing slippage → suggest 1% default
- Missing network for withdraw → ask user, only `bsc` or `sol` supported
- **User requests unsupported chain** → inform user that custodial wallet only supports BSC and Solana

### Step 3: Execute & Display

- Run the API call
- Parse JSON response
- Display human-readable summary

### Step 4: Suggest Next Steps

| Just completed | Suggest |
|---|---|
| Wallet created | 1. Deposit BNB (BSC) or SOL (Solana) to the new address — do NOT send other chain assets 2. Check balance → `opentrade-portfolio` |
| Account queried | 1. Check balance → `opentrade-portfolio` 2. Execute a swap → custodial swap (this skill) |
| Swap executed | 1. Check updated balance → `opentrade-portfolio` 2. Withdraw to external wallet → custodial withdraw (this skill) |
| Withdraw completed | 1. Check remaining balance → `opentrade-portfolio` 2. Swap another token → custodial swap (this skill) |

Present conversationally — never expose endpoint paths to the user.

## API Reference

### 1. Create Custodial Wallet

创建托管钱包，同时生成 EVM（BSC）和 Solana 地址。每个用户只能创建一个钱包。

```bash
curl -s -X POST "$BASE_URL/open/trader/custodial/create" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json"
```

**Parameters**: None (user identity from JWT token)

**Response:**
```json
{
  "success": true,
  "data": {
    "evm_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "sol_address": "7EcDhSYGxXyscszYEp35KHN8vvw3svAuLKTzXwCFLtV"
  }
}
```

**Return fields:**

| Field | Type | Description |
|---|---|---|
| `evm_address` | String | BSC 链地址 |
| `sol_address` | String | Solana 链地址 |

**Display to user:**
- "Custodial wallet created!"
- "BSC Address: 0x742d..."
- "Solana Address: 7EcD..."
- "Please deposit BNB to your BSC address or SOL to your Solana address before trading."
- "WARNING: Only send BNB (BSC network) or SOL (Solana network). Do NOT send tokens from other chains — funds will be lost."

---

### 2. Get Custodial Account

获取当前用户的托管钱包地址。

```bash
curl -s "$BASE_URL/open/trader/custodial/account" \
  -H "$AUTH_HEADER"
```

**Parameters**: None

**Response:**
```json
{
  "success": true,
  "data": {
    "evm_address": "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb",
    "sol_address": "7EcDhSYGxXyscszYEp35KHN8vvw3svAuLKTzXwCFLtV"
  }
}
```

**Return fields:**

| Field | Type | Description |
|---|---|---|
| `evm_address` | String | BSC 链地址 |
| `sol_address` | String | Solana 链地址 |

---

### 3. Custodial Swap

使用托管钱包执行 DEX swap。服务端自动完成签名和广播。仅支持 BSC（chainIndex: 56）和 Solana（chainIndex: 501）。

```bash
curl -s -X POST "$BASE_URL/open/trader/custodial/swap" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{
    "chainIndex": "56",
    "fromTokenAddress": "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",
    "toTokenAddress": "0x55d398326f99059fF775485246999027B3197955",
    "amount": "1000000000000000000",
    "slippagePercent": "1"
  }'
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `chainIndex` | String | Yes | 链 ID：`"56"`（BSC）或 `"501"`（Solana） |
| `fromTokenAddress` | String | Yes | 源代币合约地址 |
| `toTokenAddress` | String | Yes | 目标代币合约地址 |
| `amount` | String | Yes | 交易数量（最小单位） |
| `slippagePercent` | String | No | 滑点百分比（默认 `"1"`，即 1%） |

**Response:**
```json
{
  "success": true,
  "data": {
    "tx_hash": "0xabc123def456...",
    "error": ""
  }
}
```

**Return fields:**

| Field | Type | Description |
|---|---|---|
| `tx_hash` | String | 交易哈希（成功时返回） |
| `error` | String | 错误信息（失败时返回） |

**Display to user:**
- "Swap executed successfully!"
- "Tx Hash: 0xabc123..."
- If `error` is non-empty, display the error message

---

### 4. Custodial Withdraw

从托管钱包提现原生代币。仅支持 BSC (BNB) 和 Solana (SOL)。

```bash
curl -s -X POST "$BASE_URL/open/trader/custodial/withdraw" \
  -H "$AUTH_HEADER" \
  -H "Content-Type: application/json" \
  -d '{
    "network": "bsc",
    "to": "0xRecipientAddress",
    "amount": 1000000000000000000
  }'
```

**Parameters:**

| Field | Type | Required | Description |
|---|---|---|---|
| `network` | String | Yes | 网络类型：`bsc` 或 `sol` |
| `to` | String | Yes | 接收地址 |
| `amount` | Integer | Yes | 提现数量（最小单位，必须大于 0）。BSC 单位为 wei（1 BNB = 10^18 wei），Solana 单位为 lamports（1 SOL = 10^9 lamports） |

**Response:**
```json
{
  "success": true,
  "data": {
    "tx_hash": "0xdef789...",
    "network": "bsc"
  }
}
```

**Return fields:**

| Field | Type | Description |
|---|---|---|
| `tx_hash` | String | 提现交易哈希 |
| `network` | String | 执行提现的网络 |

**Display to user:**
- "Withdrawal successful!"
- "Tx Hash: 0xdef789..."
- "Network: BSC"

## Native Token Addresses

| Chain | Native Token Address |
|---|---|
| BSC | `0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee` |
| Solana | `11111111111111111111111111111111` |

## Input / Output Examples

**User says:** "Create a custodial wallet for me"

```bash
curl -s -X POST "$BASE_URL/open/trader/custodial/create" -H "$AUTH_HEADER" -H "Content-Type: application/json"
# → Wallet created! BSC: 0x742d..., Solana: 7EcD...
```

**User says:** "Swap 0.1 BNB for USDT on BSC using my custodial wallet"

```bash
# Amount: 0.1 BNB = 100000000000000000 wei
curl -s -X POST "$BASE_URL/open/trader/custodial/swap" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"chainIndex":"56","fromTokenAddress":"0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee","toTokenAddress":"0x55d398326f99059fF775485246999027B3197955","amount":"100000000000000000","slippagePercent":"1"}'
# → Swap executed! Tx Hash: 0xabc...
```

**User says:** "Withdraw 1 SOL to my external wallet"

```bash
# Amount: 1 SOL = 1000000000 lamports
curl -s -X POST "$BASE_URL/open/trader/custodial/withdraw" \
  -H "$AUTH_HEADER" -H "Content-Type: application/json" \
  -d '{"network":"sol","to":"ExternalSolanaAddress","amount":1000000000}'
# → Withdrawal successful! Tx Hash: 5xYz...
```

## Edge Cases

- **Wallet already exists**: `POST /open/trader/custodial/create` will return an error if the user already has a wallet. Use `GET /open/trader/custodial/account` to retrieve existing addresses.
- **New wallet has zero balance**: After creating a wallet, the user must deposit BNB (via BSC network) or SOL (via Solana network) before performing any swap or withdraw. Do NOT deposit tokens from other chains (Ethereum, Polygon, Arbitrum, etc.) — those funds will be permanently lost.
- **Unsupported chain**: Custodial wallet **only supports BSC (chainIndex: 56) and Solana (chainIndex: 501)**. If the user requests another chain (e.g., Ethereum, Arbitrum), inform them that the custodial wallet does not support that chain and suggest using a non-custodial workflow with `opentrade-dex-swap` + `opentrade-gateway`.
- **Insufficient balance**: Swap or withdraw will fail if the custodial wallet has insufficient funds. Check balance with `opentrade-portfolio` first.
- **Unsupported network for withdraw**: Only `bsc` and `sol` are supported for withdraw.
- **Amount must be positive**: The `amount` field for withdraw must be greater than 0.
- **High slippage swap**: If slippage is too low, the swap may fail. Suggest increasing slippage for volatile tokens.
- **Network error**: Retry once, then prompt user to try again later.
- **Region restriction (error code 50125 or 80001)**: Do NOT show the raw error code to the user. Instead, display a friendly message: `Service is not available in your region. Please switch to a supported region and try again.`

## Amount Display Rules

- Input/output amounts in UI units (`0.1 BNB`, `50 USDT`)
- Internal API params use minimal units (`1 BNB` = `"1000000000000000000"`, `1 SOL` = `1000000000`)
- Display tx hash as clickable link when possible

## Global Notes

- All endpoints require `Authorization: Bearer <token>` header
- **Only BSC and Solana are supported** — do not attempt other chains
- Amounts must be in **minimal units** (wei for BSC, lamports for Solana)
- EVM contract addresses must be **all lowercase**
- Custodial swap handles signing and broadcasting automatically — no need to call sign or broadcast separately
- Withdraw only supports native tokens (BNB/SOL)
- The custodial wallet is powered by Turnkey with **AWS KMS** for delegated key custody — **6551 does NOT store your private keys**
