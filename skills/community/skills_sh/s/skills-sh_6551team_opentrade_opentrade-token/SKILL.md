---
name: opentrade-token
description: "This skill should be used when the user asks to 'find a token', 'search for a token', 'look up PEPE', 'what's trending', 'top tokens', 'trending tokens on Solana', 'token rankings', 'who holds this token', 'holder distribution', 'token market cap', 'token liquidity', 'research a token', 'tell me about this token', 'token info', or mentions searching for tokens by name or address, discovering trending tokens, viewing token rankings, checking holder distribution, or analyzing token market cap and liquidity. Covers token search, metadata, market cap, liquidity, volume, trending token rankings, and holder analysis across XLayer, Solana, Ethereum, Base, BSC, Arbitrum, Polygon, and 20+ other chains. Do NOT use when the user says only a single generic word like 'tokens' or 'crypto' without specifying a token name, action, or question. For simple current price checks, price charts, candlestick data, or trade history, use opentrade-market instead. For meme token safety analysis, developer reputation, rug pull checks, bundle/sniper detection, or finding tokens by same creator, use opentrade-market instead."
license: Apache-2.0
metadata:
  author: 6551
  version: "1.0.2"
  homepage: "https://www.newsliquid.com"
---

# OpenTrade DEX Token Info CLI

5 commands for token search, metadata, detailed pricing, rankings, and holder distribution.

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
- Example: `opentrade token search USDC --chains ethereum --trader okx --api v1`
- **Default fallback**: If the API returns no data or is empty, use `--trader okx --api v1`

## Skill Routing

- For real-time prices / K-lines / trade history → use `opentrade-market`
- For swap execution → use `opentrade-dex-swap`
- For transaction broadcasting → use `opentrade-gateway`
- For wallet balances / portfolio → use `opentrade-portfolio`
- For meme token safety (dev reputation, rug pull, bundlers, similar tokens by same dev) → use `opentrade-market`
- For smart money / whale / KOL signals → use `opentrade-market`

## Quickstart

```bash
# Search token
opentrade token search xETH --chains "ethereum,solana"

# Get detailed price info
opentrade token price-info 0xe7b000003a45145decf8a28fc755ad5ec5ea025a --chain xlayer

# What's trending on Solana by volume?
opentrade token toplist --chains solana --sort-by 5 --time-frame 4

# Check holder distribution
opentrade token holders 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee --chain xlayer
```

## Chain Name Support

The CLI accepts human-readable chain names (e.g., `ethereum`, `solana`, `xlayer`) and resolves them automatically.

| Chain | Name | chainIndex |
|---|---|---|
| XLayer | `xlayer` | `196` |
| Solana | `solana` | `501` |
| Ethereum | `ethereum` | `1` |
| Base | `base` | `8453` |
| BSC | `bsc` | `56` |
| Arbitrum | `arbitrum` | `42161` |
| Polygon | `polygon` | `137` |
| Optimism | `optimism` | `10` |
| Avalanche | `avalanche` | `43114` |
| Fantom | `fantom` | `250` |
| Cronos | `cronos` | `25` |
| Gnosis | `gnosis` | `100` |
| Klaytn | `klaytn` | `8217` |
| Aurora | `aurora` | `1313161554` |
| Harmony | `harmony` | `1666600000` |
| Moonbeam | `moonbeam` | `1284` |
| Moonriver | `moonriver` | `1285` |
| Celo | `celo` | `42220` |
| Fuse | `fuse` | `122` |
| OKC | `okc` | `66` |
| Heco | `heco` | `128` |
| Metis | `metis` | `1088` |
| Boba | `boba` | `288` |
| zkSync Era | `zksync` | `324` |
| Polygon zkEVM | `polygon-zkevm` | `1101` |
| Linea | `linea` | `59144` |
| Mantle | `mantle` | `5000` |
| Scroll | `scroll` | `534352` |
| Blast | `blast` | `81457` |

## Command Index

| # | Command | Description |
|---|---|---|
| 1 | `opentrade token search <query>` | Search for tokens by name, symbol, or address |
| 2 | `opentrade token info <address>` | Get token basic info (name, symbol, decimals, logo) |
| 3 | `opentrade token price-info <address>` | Get detailed price info (price, market cap, liquidity, volume, 24h change) |
| 4 | `opentrade token toplist` | Get trending / top tokens |
| 5 | `opentrade token holders <address>` | Get token holder distribution (top 20) |

## Boundary: token vs market skill

| Need | Use this skill (`opentrade-token`) | Use `opentrade-market` instead |
|---|---|---|
| Search token by name/symbol | `opentrade token search` | - |
| Token metadata (decimals, logo) | `opentrade token info` | - |
| Price + market cap + liquidity + multi-timeframe change | `opentrade token price-info` | - |
| Token ranking (trending) | `opentrade token toplist` | - |
| Holder distribution | `opentrade token holders` | - |
| Raw real-time price (single value) | - | `opentrade market price` |
| K-line / candlestick chart | - | `opentrade market kline` |
| Trade history (buy/sell log) | - | `opentrade market trades` |
| Index price (multi-source aggregate) | - | `opentrade market index` |
| Meme token dev reputation / rug pull | - | `opentrade market memepump-token-dev-info` |
| Bundle/sniper detection | - | `opentrade market memepump-token-bundle-info` |
| Similar tokens by same creator | - | `opentrade market memepump-similar-tokens` |

**Rule of thumb**: `opentrade-token` = token discovery & enriched analytics (search, trending, holders, market cap). `opentrade-market` = raw price feeds, charts, smart money signals & meme pump scanning (including dev reputation, rug pull checks, bundler analysis).

## Cross-Skill Workflows

This skill is the typical **entry point** — users often start by searching/discovering tokens, then proceed to swap.

### Workflow A: Search → Research → Buy

> User: "Find BONK token, analyze it, then buy some"

```
1. opentrade-token    opentrade token search BONK --chains solana              → get tokenContractAddress, chain, price
       ↓ tokenContractAddress
2. opentrade-token    opentrade token price-info <address> --chain solana      → market cap, liquidity, volume24H, priceChange24H
3. opentrade-token    opentrade token holders <address> --chain solana         → top 20 holders distribution
4. opentrade-market   opentrade market kline <address> --chain solana --bar 1H → hourly price chart
       ↓ user decides to buy
5. opentrade-dex-swap opentrade swap quote --from ... --to <address> --amount ... --chain solana
6. opentrade-dex-swap opentrade swap swap --from ... --to <address> --amount ... --chain solana --wallet <addr>
```

**Data handoff**:
- `tokenContractAddress` from step 1 → reused in all subsequent steps
- `chain` from step 1 → reused in all subsequent steps
- `decimal` from step 1 or `opentrade token info` → needed for minimal unit conversion in swap

### Workflow B: Discover Trending → Investigate → Trade

> User: "What's trending on Solana?"

```
1. opentrade-token    opentrade token toplist --chains solana --sort-by 5 --time-frame 4  → top tokens by 24h volume
       ↓ user picks a token
2. opentrade-token    opentrade token price-info <address> --chain solana                  → detailed analytics
3. opentrade-token    opentrade token holders <address> --chain solana                     → check if whale-dominated
4. opentrade-market   opentrade market kline <address> --chain solana                      → K-line for visual trend
       ↓ user decides to trade
5. opentrade-dex-swap opentrade swap swap --from ... --to ... --amount ... --chain solana --wallet <addr>
```

### Workflow C: Token Verification Before Swap

Before swapping an unknown token, always verify:

```
1. opentrade-token    opentrade token search <name>                            → find token
2. Check communityRecognized:
   - true → proceed with normal caution
   - false → warn user about risk
3. opentrade-token    opentrade token price-info <address> → check liquidity:
   - liquidity < $10K → warn about high slippage risk
   - liquidity < $1K → strongly discourage trade
4. opentrade-dex-swap opentrade swap quote ... → check isHoneyPot and taxRate
5. If all checks pass → proceed to swap
```

## Operation Flow

### Step 1: Identify Intent

- Search for a token → `opentrade token search`
- Get token metadata → `opentrade token info`
- Get price + market cap + liquidity → `opentrade token price-info`
- View rankings → `opentrade token toplist`
- View holder distribution → `opentrade token holders`

### Step 2: Collect Parameters

- Missing chain → recommend XLayer (`--chain xlayer`, low gas, fast confirmation) as the default, then ask which chain the user prefers
- Only have token name, no address → use `opentrade token search` first
- For search, `--chains` defaults to `"1,501"` (Ethereum + Solana)
- For toplist, `--sort-by` defaults to `5` (volume), `--time-frame` defaults to `4` (24h)

### Step 3: Call and Display

- Search results: show name, symbol, chain, price, 24h change
- Indicate `communityRecognized` status for trust signaling
- Price info: show market cap, liquidity, and volume together

### Step 4: Suggest Next Steps

After displaying results, suggest 2-3 relevant follow-up actions based on the command just executed:

| Just called | Suggest |
|---|---|
| `token search` | 1. View detailed analytics (market cap, liquidity) → `opentrade token price-info` (this skill) 2. View price chart → `opentrade-market` 3. Buy/swap this token → `opentrade-dex-swap` |
| `token info` | 1. View price and market data → `opentrade token price-info` (this skill) 2. Check holder distribution → `opentrade token holders` (this skill) |
| `token price-info` | 1. View K-line chart → `opentrade-market` 2. Check holder distribution → `opentrade token holders` (this skill) 3. Buy/swap this token → `opentrade-dex-swap` |
| `token toplist` | 1. View details for a specific token → `opentrade token price-info` (this skill) 2. View price chart → `opentrade-market` 3. Buy a trending token → `opentrade-dex-swap` |
| `token holders` | 1. View price trend → `opentrade-market` 2. Buy/swap this token → `opentrade-dex-swap` |

Present conversationally, e.g.: "Would you like to see the price chart or check the holder distribution?" — never expose skill names or endpoint paths to the user.

## CLI Command Reference

### 1. opentrade token search

Search for tokens by name, symbol, or contract address.

```bash
opentrade token search <query> [--chains <chains>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `<query>` | Yes | - | Keyword: token name, symbol, or contract address (positional) |
| `--chains` | No | `"1,501"` | Chain names or IDs, comma-separated (e.g., `"ethereum,solana"` or `"196,501"`) |

**Return fields**:

| Field | Type | Description |
|---|---|---|
| `tokenContractAddress` | String | Token contract address |
| `tokenSymbol` | String | Token symbol (e.g., `"ETH"`) |
| `tokenName` | String | Token full name |
| `tokenLogoUrl` | String | Token logo image URL |
| `chainIndex` | String | Chain identifier |
| `decimal` | String | Token decimals (e.g., `"18"`) |
| `price` | String | Current price in USD |
| `change` | String | 24-hour price change percentage |
| `marketCap` | String | Market capitalization in USD |
| `liquidity` | String | Liquidity in USD |
| `holders` | String | Number of token holders |
| `explorerUrl` | String | Block explorer URL for the token |
| `tagList.communityRecognized` | Boolean | `true` = listed on Top 10 CEX or community verified |

### 2. opentrade token info

Get token basic info (name, symbol, decimals, logo).

```bash
opentrade token info <address> [--chain <chain>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `<address>` | Yes | - | Token contract address (positional) |
| `--chain` | No | `ethereum` | Chain name |

**Return fields**:

| Field | Type | Description |
|---|---|---|
| `tokenContractAddress` | String | Contract address |
| `tokenSymbol` | String | Token symbol |
| `tokenName` | String | Full name |
| `chainIndex` | String | Chain identifier |
| `decimal` | String | Token decimals |
| `totalSupply` | String | Total supply |
| `logoUrl` | String | Token logo URL |
| `websiteUrl` | String | Official website |
| `twitterUrl` | String | Twitter/X profile |
| `telegramUrl` | String | Telegram group |
| `discordUrl` | String | Discord server |
| `communityRecognized` | Boolean | Verification status |

### 3. opentrade token price-info

Get detailed price, market cap, liquidity, volume, and multi-timeframe changes.

```bash
opentrade token price-info <address> [--chain <chain>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `<address>` | Yes | - | Token contract address (positional) |
| `--chain` | No | `ethereum` | Chain name |

**Return fields**:

| Field | Type | Description |
|---|---|---|
| `price` | String | Current price in USD |
| `priceChange1h` | String | 1h price change % |
| `priceChange4h` | String | 4h price change % |
| `priceChange12h` | String | 12h price change % |
| `priceChange24h` | String | 24h price change % |
| `volume24h` | String | 24h trading volume |
| `liquidity` | String | Total liquidity in USD |
| `liquidityChange24h` | String | 24h liquidity change % |
| `marketCap` | String | Market capitalization |
| `fullyDilutedValuation` | String | FDV |
| `holders` | String | Number of token holders |
| `transactions24h` | String | 24h transaction count |
| `buys24h` | String | 24h buy count |
| `sells24h` | String | 24h sell count |

### 4. opentrade token toplist

Get trending / top tokens by various metrics.

```bash
opentrade token toplist [--chains <chains>] [--sort-by <n>] [--time-frame <n>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--chains` | No | `"1,501"` | Chain names or IDs, comma-separated |
| `--sort-by` | No | `5` | Sort metric: `2` = price change, `5` = volume, `6` = market cap |
| `--time-frame` | No | `4` | Time window: `1` = 5min, `2` = 1h, `3` = 4h, `4` = 24h |

**Return fields** (array of tokens):

| Field | Type | Description |
|---|---|---|
| `tokenContractAddress` | String | Token contract address |
| `tokenSymbol` | String | Token symbol |
| `chainIndex` | String | Chain identifier |
| `price` | String | Current price |
| `change` | String | Price change % for selected time frame |
| `volume` | String | Volume for selected time frame |
| `marketCap` | String | Market capitalization |
| `liquidity` | String | Liquidity in USD |

### 5. opentrade token holders

Get token holder distribution (top 20).

```bash
opentrade token holders <address> [--chain <chain>]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `<address>` | Yes | - | Token contract address (positional) |
| `--chain` | No | `ethereum` | Chain name |

**Return fields** (top 20 holders):

| Field | Type | Description |
|---|---|---|
| `data[].holdAmount` | String | Token amount held |
| `data[].holderWalletAddress` | String | Holder wallet address |

## Input / Output Examples

**User says:** "Search for xETH token on XLayer"

```bash
opentrade token search xETH --chains xlayer
# → Display:
#   xETH (0xe7b0...) - XLayer
#   Price: $X,XXX.XX | 24h: +X% | Market Cap: $XXM | Liquidity: $XXM
#   Community Recognized: Yes
```

**User says:** "What's trending on Solana by volume?"

```bash
opentrade token toplist --chains solana --sort-by 5 --time-frame 4
# → Display top tokens sorted by 24h volume:
#   #1 SOL  - Vol: $1.2B | Change: +3.5% | MC: $80B
#   #2 BONK - Vol: $450M | Change: +12.8% | MC: $1.5B
#   ...
```

**User says:** "Who are the top holders of this token?"

```bash
opentrade token holders 0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee --chain xlayer
# → Display top 20 holders with amounts and addresses
```

## Edge Cases

- **Token not found**: suggest verifying the contract address (symbols can collide)
- **Same symbol on multiple chains**: show all matches with chain names
- **Unverified token**: `communityRecognized = false` — warn user about risk
- **Too many results**: name/symbol search caps at 100 — suggest using exact contract address
- **Network error**: retry once
- **Region restriction (error code 50125 or 80001)**: do NOT show the raw error code to the user. Instead, display a friendly message: `⚠️ Service is not available in your region. Please switch to a supported region and try again.`

## Amount Display Rules

- Use appropriate precision: 2 decimals for high-value, significant digits for low-value
- Market cap / liquidity in shorthand ($1.2B, $45M)
- 24h change with sign and color hint (+X% / -X%)

## Global Notes

- Use contract address as **primary identity** — symbols can collide across tokens
- `communityRecognized = true` means listed on Top 10 CEX or community verified
- The CLI resolves chain names automatically (e.g., `ethereum` → `1`, `solana` → `501`)
- EVM addresses must be **all lowercase**
- The CLI handles authentication internally via environment variables — see Pre-flight Checks step 4 for authentication setup
- Get your API token at https://www.newsliquid.com/mcp
