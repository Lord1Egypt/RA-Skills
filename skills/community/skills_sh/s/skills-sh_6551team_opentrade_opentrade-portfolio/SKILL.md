---
name: opentrade-portfolio
description: "This skill should be used when the user asks to 'check my wallet balance', 'show my token holdings', 'how much OKB do I have', 'what tokens do I have', 'check my portfolio value', 'view my assets', 'how much is my portfolio worth', 'what\\'s in my wallet', or mentions checking wallet balance, total assets, token holdings, portfolio value, remaining funds, DeFi positions, or multi-chain balance lookup. Supports XLayer, Solana, Ethereum, Base, BSC, Arbitrum, Polygon, and 20+ other chains. Do NOT use for general programming questions about balance variables or API documentation. Do NOT use when the user is asking how to build or integrate a balance feature into code."
license: Apache-2.0
metadata:
  author: 6551
  version: "1.0.2"
  homepage: "https://www.newsliquid.com"
---

# OpenTrade Wallet Portfolio CLI

4 commands for supported chains, wallet total value, all token balances, and specific token balances.

## Pre-flight Checks

Every time before running any `opentrade` command, always follow these steps in order. Do not echo routine command output to the user; only provide a brief status update when installing, updating, or handling a failure.

1. **Confirm installed**: Run `which opentrade`. If not found, install it:
   ```bash
   curl -sSL https://raw.githubusercontent.com/6551Team/openskills/main/skills/opentrade/install.sh | sh
   ```
   If the install script fails, ask the user to install manually following the instructions at: https://github.com/6551Team/openskills

2. **Check for updates**: Read `~/.opentrade/last_check` and compare it with the current timestamp:
   ```bash
   cached_ts=$(cat ~/.opentrade/last_check 2>/dev/null || true)
   now=$(date +%s)
   ```
   - If `cached_ts` is non-empty and `(now - cached_ts) < 43200` (12 hours), skip the update and proceed.
   - Otherwise (file missing or older than 12 hours), run the installer to check for updates:
     ```bash
     curl -sSL https://raw.githubusercontent.com/6551Team/openskills/main/skills/opentrade/install.sh | sh
     ```
     If a newer version is installed, tell the user and suggest updating their opentrade skills from https://github.com/6551Team/openskills to get the latest features.
3. If any `opentrade` command fails with an unexpected error during this
   session, try reinstalling before giving up:
   ```bash
   curl -sSL https://raw.githubusercontent.com/6551Team/openskills/main/skills/opentrade/install.sh | sh
   ```
4. Find or create a .env file in the project root to override the default API credentials, Load it before performing opentrade operations.
  ```bash
  OPEN_TOKEN=your_token_here
  ```

  Get your API token at: https://www.newsliquid.com/mcp

  **Security warning**: Never commit .env to git (add it to .gitignore) and never expose credentials in logs, screenshots, or chat messages.

## Router Discovery

**IMPORTANT**: If the user has not specified a trading router, you MUST first discover available routers:

```bash
opentrade trade routers
```

**Response format:**
```json
{
  "ok": true,
  "data": [
    {
      "api": "v2",
      "created_at": "2026-03-10 01:15:42",
      "is_active": true,
      "name": "6551dex test",
      "quota_reward": 0,
      "trader": "6551dex",
      "updated_at": "2026-03-10 01:15:42"
    },
    {
      "api": "v1",
      "created_at": "2026-03-03 21:24:34",
      "is_active": true,
      "name": "okx test",
      "quota_reward": 0,
      "trader": "okx",
      "updated_at": "2026-03-03 21:24:34"
    }
  ]
}
```

**Usage:**
- Extract `trader` and `api` from the response
- **MANDATORY**: ALL subsequent `opentrade` commands in this session MUST include `--trader <trader>` and `--api <api>` flags
- Example: `opentrade portfolio balance 0x... --chain ethereum --trader okx --api v1`
- **Default fallback**: If the API returns no data or is empty, use `--trader okx --api v1`

## Skill Routing

- For token prices / K-lines → use `opentrade-market`
- For token search / metadata → use `opentrade-token`
- For swap execution → use `opentrade-dex-swap`
- For transaction broadcasting → use `opentrade-gateway`

## Quickstart

```bash
# Get supported chains for balance queries
opentrade portfolio chains

# Get total asset value on XLayer and Solana
opentrade portfolio total-value --address 0xYourWallet --chains "xlayer,solana"

# Get all token balances
opentrade portfolio all-balances --address 0xYourWallet --chains "xlayer,solana,ethereum"

# Check specific tokens (native OKB + USDC on XLayer)
opentrade portfolio token-balances --address 0xYourWallet --tokens "196:,196:0x74b7f16337b8972027f6196a17a631ac6de26d22"
```

## Chain Name Support

The CLI accepts human-readable chain names and resolves them automatically.

| Chain | Name | chainIndex |
|---|---|---|
| XLayer | `xlayer` | `196` |
| Solana | `solana` | `501` |
| Ethereum | `ethereum` | `1` |
| Base | `base` | `8453` |
| BSC | `bsc` | `56` |
| Arbitrum | `arbitrum` | `42161` |

**Address format note**: EVM addresses (`0x...`) work across Ethereum/BSC/Polygon/Arbitrum/Base etc. Solana addresses (Base58) and Bitcoin addresses (UTXO) have different formats. Do NOT mix formats across chain types.

## Command Index

| # | Command | Description |
|---|---|---|
| 1 | `opentrade portfolio chains` | Get supported chains for balance queries |
| 2 | `opentrade portfolio total-value --address ... --chains ...` | Get total asset value for a wallet |
| 3 | `opentrade portfolio all-balances --address ... --chains ...` | Get all token balances for a wallet |
| 4 | `opentrade portfolio token-balances --address ... --tokens ...` | Get specific token balances |

## Cross-Skill Workflows

This skill is often used **before swap** (to verify sufficient balance) or **as portfolio entry point**.

### Workflow A: Pre-Swap Balance Check

> User: "Swap 1 SOL for BONK"

```
1. opentrade-token    opentrade token search BONK --chains solana               → get tokenContractAddress
       ↓ tokenContractAddress
2. opentrade-portfolio  opentrade portfolio all-balances --address <addr> --chains solana
       → verify SOL balance >= 1
       ↓ balance field (UI units) → convert to minimal units for swap
3. opentrade-dex-swap     opentrade swap quote --from 11111111111111111111111111111111 --to <BONK_address> --amount 1000000000 --chain solana
4. opentrade-dex-swap     opentrade swap swap --from ... --to <BONK_address> --amount 1000000000 --chain solana --wallet <addr>
```

**Data handoff**:
- `tokenContractAddress` from token search → feeds into swap `--from` / `--to`
- `balance` from portfolio is **UI units**; swap needs **minimal units** → multiply by `10^decimal`
- If balance < required amount → inform user, do NOT proceed to swap

### Workflow B: Portfolio Overview + Analysis

> User: "Show my portfolio"

```
1. opentrade-portfolio  opentrade portfolio total-value --address <addr> --chains "xlayer,solana,ethereum"
       → total USD value
2. opentrade-portfolio  opentrade portfolio all-balances --address <addr> --chains "xlayer,solana,ethereum"
       → per-token breakdown
       ↓ top holdings by USD value
3. opentrade-token    opentrade token price-info <address> --chain <chain>  → enrich with 24h change, market cap
4. opentrade-market   opentrade market kline <address> --chain <chain>      → price charts for tokens of interest
```

### Workflow C: Sell Underperforming Tokens

```
1. opentrade-portfolio  opentrade portfolio all-balances --address <addr> --chains "xlayer,solana,ethereum"
       → list all holdings
       ↓ tokenContractAddress + chainIndex for each
2. opentrade-token    opentrade token price-info <address> --chain <chain>  → get priceChange24H per token
3. Filter by negative change → user confirms which to sell
4. opentrade-dex-swap     opentrade swap quote → opentrade swap swap → execute sell
```

**Key conversion**: `balance` (UI units) × `10^decimal` = `amount` (minimal units) for swap.

## Operation Flow

### Step 1: Identify Intent

- Check total assets → `opentrade portfolio total-value`
- View all token holdings → `opentrade portfolio all-balances`
- Check specific token balance → `opentrade portfolio token-balances`
- Unsure which chains are supported → `opentrade portfolio chains` first

### Step 2: Collect Parameters

- Missing wallet address → ask user
- Missing target chains → recommend XLayer (`--chains xlayer`, low gas, fast confirmation) as the default, then ask which chain the user prefers. Common set: `"xlayer,solana,ethereum,base,bsc"`
- Need to filter risky tokens → set `--exclude-risk 0` (only works on ETH/BSC/SOL/BASE)

### Step 3: Call and Display

- Total value: display USD amount
- Token balances: show token name, amount (UI units), USD value
- Sort by USD value descending

### Step 4: Suggest Next Steps

After displaying results, suggest 2-3 relevant follow-up actions:

| Just completed | Suggest |
|---|---|
| `portfolio total-value` | 1. View token-level breakdown → `opentrade portfolio all-balances` (this skill) 2. Check price trend for top holdings → `opentrade-market` |
| `portfolio all-balances` | 1. View detailed analytics (market cap, 24h change) for a token → `opentrade-token` 2. Swap a token → `opentrade-dex-swap` 3. View price chart for a token → `opentrade-market` |
| `portfolio token-balances` | 1. View full portfolio across all tokens → `opentrade portfolio all-balances` (this skill) 2. Swap this token → `opentrade-dex-swap` |

Present conversationally, e.g.: "Would you like to see the price chart for your top holding, or swap any of these tokens?" — never expose skill names or endpoint paths to the user.

## CLI Command Reference

### 1. opentrade portfolio chains

Get supported chains for balance queries. No parameters required.

```bash
opentrade portfolio chains
```

**Return fields**:

| Field | Type | Description |
|---|---|---|
| `name` | String | Chain name (e.g., `"XLayer"`) |
| `logoUrl` | String | Chain logo URL |
| `shortName` | String | Chain short name (e.g., `"OKB"`) |
| `chainIndex` | String | Chain unique identifier (e.g., `"196"`) |

### 2. opentrade portfolio total-value

Get total asset value for a wallet address.

```bash
opentrade portfolio total-value --address <address> --chains <chains> [--asset-type <type>] [--exclude-risk <bool>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--address` | Yes | - | Wallet address |
| `--chains` | Yes | - | Chain names or IDs, comma-separated (e.g., `"xlayer,solana"` or `"196,501"`) |
| `--asset-type` | No | `"0"` | `0`=all, `1`=tokens only, `2`=DeFi only |
| `--exclude-risk` | No | `true` | `true`=filter risky tokens, `false`=include. Only ETH/BSC/SOL/BASE |

**Return fields**:

| Field | Type | Description |
|---|---|---|
| `totalValue` | String | Total asset value in USD |

### 3. opentrade portfolio all-balances

Get all token balances for a wallet address.

```bash
opentrade portfolio all-balances --address <address> --chains <chains> [--exclude-risk <value>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--address` | Yes | - | Wallet address |
| `--chains` | Yes | - | Chain names or IDs, comma-separated, max 50 |
| `--exclude-risk` | No | `"0"` | `0`=filter out risky tokens (default), `1`=include. Only ETH/BSC/SOL/BASE |

**Return fields** (per token in `tokenAssets[]`):

| Field | Type | Description |
|---|---|---|
| `chainIndex` | String | Chain identifier |
| `tokenContractAddress` | String | Token contract address |
| `symbol` | String | Token symbol (e.g., `"OKB"`) |
| `balance` | String | Token balance in UI units (e.g., `"10.5"`) |
| `rawBalance` | String | Token balance in base units (e.g., `"10500000000000000000"`) |
| `tokenPrice` | String | Token price in USD |
| `isRiskToken` | Boolean | `true` if flagged as risky |

### 4. opentrade portfolio token-balances

Get specific token balances for a wallet address.

```bash
opentrade portfolio token-balances --address <address> --tokens <tokens> [--exclude-risk <value>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--address` | Yes | - | Wallet address |
| `--tokens` | Yes | - | Token list: `"chainIndex:tokenAddress"` pairs, comma-separated. Use empty address for native token (e.g., `"196:"` for native OKB). Max 20 items. |
| `--exclude-risk` | No | `"0"` | `0`=filter out (default), `1`=include |

**Return fields**: Same schema as `all-balances` (`tokenAssets[]`).

## Input / Output Examples

**User says:** "Check my wallet total assets on XLayer and Solana"

```bash
opentrade portfolio total-value --address 0xYourWallet --chains "xlayer,solana"
# → Display: Total assets $12,345.67
```

**User says:** "Show all tokens in my wallet"

```bash
opentrade portfolio all-balances --address 0xYourWallet --chains "xlayer,solana,ethereum"
# → Display:
#   OKB:  10.5 ($509.25)
#   USDC: 2,000 ($2,000.00)
#   USDT: 1,500 ($1,500.00)
#   ...
```

**User says:** "Only check USDC and native OKB balances on XLayer"

```bash
opentrade portfolio token-balances --address 0xYourWallet --tokens "196:,196:0x74b7f16337b8972027f6196a17a631ac6de26d22"
# → Display: OKB: 10.5 ($509.25), USDC: 2,000 ($2,000.00)
```

## Edge Cases

- **Zero balance**: valid state — display `$0.00`, not an error
- **Unsupported chain**: call `opentrade portfolio chains` first to confirm
- **chains exceeds 50**: split into batches, max 50 per request
- **`--exclude-risk` not working**: only supported on ETH/BSC/SOL/BASE
- **DeFi positions**: use `--asset-type 2` to query DeFi holdings separately
- **Address format mismatch**: EVM address on Solana chain will return empty data — do NOT mix
- **Network error**: retry once, then prompt user to try again later
- **Region restriction (error code 50125 or 80001)**: do NOT show the raw error code to the user. Instead, display a friendly message: `⚠️ Service is not available in your region. Please switch to a supported region and try again.`

## Amount Display Rules

- Token amounts in UI units (`1.5 ETH`), never base units (`1500000000000000000`)
- USD values with 2 decimal places
- Large amounts in shorthand (`$1.2M`)
- Sort by USD value descending

## Global Notes

- `--chains` supports up to **50** chain IDs (comma-separated, names or numeric)
- `--asset-type`: `0`=all `1`=tokens only `2`=DeFi only (only for `total-value`)
- `--exclude-risk` only works on ETH(`1`)/BSC(`56`)/SOL(`501`)/BASE(`8453`)
- `token-balances` supports max **20** token entries
- The CLI resolves chain names automatically (e.g., `ethereum` → `1`, `solana` → `501`)
- The CLI handles authentication internally via environment variables — see Prerequisites step 4 for default values
