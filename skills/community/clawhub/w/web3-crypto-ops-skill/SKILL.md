---
name: web3-crypto-ops
description: >
  Universal Web3 & Crypto operating skill for AI agents. 12 domains, 60+ API endpoints,
  5 providers: OKX DEX aggregator, Binance Web3 intelligence, Binance/Gate.io/Bitget Spot.
  Production-grade patterns: RPC health failover, 10-point token safety scoring, honeypot
  round-trip simulation, V2/V3 smart routing, direct pool turbo execution, Pump.fun/Jupiter
  auto-dispatch. Commercial risk gates and compliance controls built-in.
license: Apache-2.0
# ── Invocation policy ───────────────────────────────────────────────────────
# always:false → skill is user-invocable only; NOT silently auto-triggered.
# Platform must prompt the user before any mainnet fund movement.
always: false
metadata:
  version: "1.0.3"
  tags: [web3, crypto, dex, cex, swap, portfolio, audit, smart-money, meme, signals, gate, bitget]
  categories: [trading, defi, analytics, security, market-intelligence]
  compatibility: [openclaw, gemini-cli]
  providers: [okx-dex, binance-web3, binance-spot, gate-spot, bitget-spot]
  chains: [ethereum, bsc, solana, base, arbitrum, polygon, xlayer]

# ── Required environment variables (surfaced to platform registry) ───────────
# CRITICAL: This block MUST match §XVI of the skill body exactly.
# A mismatch between this list and §XVI is a security red flag — keep in sync.
requiredEnv:
  # ── CEX API keys (trade-only, NO withdrawal permission) ──
  - OKX_API_KEY
  - OKX_SECRET_KEY
  - OKX_PASSPHRASE
  - BINANCE_API_KEY
  - BINANCE_SECRET_KEY
  - GATE_API_KEY
  - GATE_SECRET_KEY
  - BITGET_API_KEY
  - BITGET_SECRET_KEY
  - BITGET_PASSPHRASE
  # ── Blockchain RPC endpoints ──
  - RPC_ETH
  - RPC_BSC
  - RPC_BASE
  - RPC_ARB
  - RPC_SOL
  # ── On-chain signing keys (CRITICAL — highest privilege) ──
  - DEPLOYER_PRIVATE_KEY
  - SOL_PRIVATE_KEY
  # ── Feature flags & configs ──
  - VAULT_TIMEOUT_MS
  - ENABLE_TESTNET
---

# Web3 Crypto Ops v3.0.0

## Trigger Phrases

Token search / trending / rankings | Price / K-line / charts | Security audit / honeypot scan |
Wallet balance / holdings | DEX swap / on-chain trade | Gas estimate / broadcast / track |
Binance / Gate / Bitget spot order | Smart money signals / social hype |
Meme Rush / Pump.fun / Four.meme | PnL leaderboard / KOL tracking

---

## I. Authentication

> **⚠️ SECURITY**: All credentials below are 🔴 Secret-level. They MUST be loaded from
> environment variables via `process.env.*`, NEVER hardcoded in source, logged, or
> transmitted in chat. See §XVI for the complete credential registry and agent rules.

### OKX (HMAC-SHA256)
```
Headers: OK-ACCESS-KEY, OK-ACCESS-SIGN, OK-ACCESS-PASSPHRASE, OK-ACCESS-TIMESTAMP
SIGN = Base64(HMAC-SHA256(timestamp+method+requestPath+body, SECRET))
GET: body="", requestPath includes queryString
POST: body=JSON, requestPath is path only
Env: OKX_API_KEY, OKX_SECRET_KEY, OKX_PASSPHRASE
```

### Binance Spot (HMAC-SHA256)
```
Header: X-MBX-APIKEY
Query: timestamp(ms) + signature=HMAC-SHA256(queryString, secret)
Mainnet: api.binance.com | Testnet: testnet.binance.vision
Env: BINANCE_API_KEY, BINANCE_SECRET_KEY
```

### Gate.io v4 (HMAC-SHA512)
```
Headers: KEY, Timestamp(seconds), SIGN
SIGN = HMAC-SHA512(secret, METHOD\n/api/v4/path\nqueryString\nSHA512(body)\ntimestamp)
Base: api.gateio.ws/api/v4
Env: GATE_API_KEY, GATE_SECRET_KEY
Rate limit: 900 req/s (private spot)
Note: Spot and Futures use SEPARATE API key pairs
```

### Bitget v2 (HMAC-SHA256)
```
Headers: ACCESS-KEY, ACCESS-SIGN, ACCESS-TIMESTAMP(ms), ACCESS-PASSPHRASE
SIGN = Base64(HMAC-SHA256(timestamp+METHOD+path+body, SECRET))
With queryString: timestamp+METHOD+path+?+queryString+body
Base: api.bitget.com
Env: BITGET_API_KEY, BITGET_SECRET_KEY, BITGET_PASSPHRASE
Note: Timestamp drift must be within ±10 seconds
```

### Binance Web3 (No Auth)
```
Public endpoints. Required header: Accept-Encoding: identity
POST also needs: Content-Type: application/json
Base: web3.binance.com
Warning: /bapi/defi/* are undocumented APIs — may change without notice, implement fallback
```

---

## II. Chain ID Mapping

| Chain    | OKX   | Binance | K-Line Platform | Native Token Address             |
| -------- | ----- | ------- | --------------- | -------------------------------- |
| Ethereum | 1     | 1       | eth             | 0xeeee...eeee                    |
| BSC      | 56    | 56      | bsc             | 0xeeee...eeee                    |
| Solana   | 501   | CT_501  | solana          | 11111111111111111111111111111111 |
| Base     | 8453  | 8453    | base            | 0xeeee...eeee                    |
| Arbitrum | 42161 | —       | —               | 0xeeee...eeee                    |
| Polygon  | 137   | —       | —               | 0xeeee...eeee                    |

**CRITICAL**: Solana native SOL uses `11111111111111111111111111111111`. Do NOT use wSOL (`So111...112`) — causes `custom program error: 0xb`.
Exception: candles and trades endpoints require the wSOL address. Binance Solana chainId is `CT_501`, not `501`.

**Wrapped Native**: BSC `0xbb4CdB9CBd36B01bD1cBaEBF2De08d9173bc095c` | ETH `0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2` | Base `0x4200000000000000000000000000000000000006`

---

## III. Domain 1 — Token Discovery

| API                  | Method | Path                                                                      | Purpose                                   |
| -------------------- | ------ | ------------------------------------------------------------------------- | ----------------------------------------- |
| OKX Search           | GET    | /api/v6/dex/market/token/search?chains=&search=                           | Search by name/symbol/address             |
| OKX Ranking          | GET    | /api/v6/dex/market/token/toplist?chains=&sortBy={2\|5\|6}&timeFrame={1-4} | Rank by change/volume/mcap                |
| OKX Basic Info       | POST   | /api/v6/dex/market/token/basic-info                                       | Batch metadata                            |
| OKX Holders          | GET    | /api/v6/dex/market/token/holder?chainIndex=&tokenContractAddress=         | Top 20 holder distribution                |
| Binance Search       | GET    | bapi/.../market/token/search?keyword=&chainIds=&orderBy=volume24h         | Alternative search source                 |
| Binance Unified Rank | POST   | bapi/.../pulse/unified/rank/list                                          | Trending/Alpha/Stock ranking with filters |

Unified Rank rankType: 10=Trending 11=Top Search 20=Alpha 40=Stock
period: 10=1m 20=5m 30=1h 40=4h 50=24h
sortBy: 40=marketCap 50=priceChange 70=volume 100=uniqueTraders

---

## IV. Domain 2 — Market Data

| API                | Method   | Path                                                                     | Returns                                             |
| ------------------ | -------- | ------------------------------------------------------------------------ | --------------------------------------------------- |
| OKX Price Info     | POST     | /api/v6/dex/market/price-info                                            | price, marketCap, liquidity, volume24H, priceChange |
| OKX Realtime Price | POST     | /api/v6/dex/market/price                                                 | price (USD)                                         |
| OKX Candles        | GET      | /api/v6/dex/market/candles?bar={interval}&limit=                         | [ts,o,h,l,c,vol,volUsd,confirm]                     |
| OKX Historical     | GET      | /api/v6/dex/market/historical-candles                                    | Same format, older data                             |
| OKX Trades         | GET      | /api/v6/dex/market/trades                                                | type, price, volume, dexName                        |
| OKX Index          | POST/GET | /api/v6/dex/index/current-price \| historical-price                      | Multi-source aggregated price                       |
| Binance Dynamic    | GET      | bapi/.../token/dynamic/info?chainId=&contractAddress=                    | price, fdv, kolHolders, smartMoneyHolders           |
| Binance Metadata   | GET      | bapi/.../token/meta/info?chainId=&contractAddress=                       | creatorAddress, links, auditInfo                    |
| Binance K-Line     | GET      | dquery.sintral.io/u-kline/v1/k-line/candles?platform=&address=&interval= | [o,h,l,c,vol,ts,count]                              |

Intervals: 1s, 1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 12H, 1D, 1W, 1M, 3M

---

## V. Domain 3 — Security Audit & Safety Scoring

### Binance Token Audit
POST `bapi/.../security/token/audit`
Body: `{ "binanceChainId": "56|8453|CT_501|1", "contractAddress": "...", "requestId": "uuid" }`
**Results valid ONLY when hasResult=true AND isSupported=true**
riskLevel: 0-1=LOW 2-3=MEDIUM 4=HIGH 5=**BLOCK TRADE**

### Production 10-Point Safety Scoring

| #   | Check                      | Safe Threshold |
| --- | -------------------------- | -------------- |
| 1   | LP Lock Rate               | ≥80%           |
| 2   | Top10 Holder Concentration | ≤45%           |
| 3   | Liquidity (USD)            | ≥$15,000       |
| 4   | Market Cap (USD)           | ≥$20,000       |
| 5   | Holder Count               | ≥150           |
| 6   | Insider Holding %          | ≤10%           |
| 7   | Sniper Holding %           | ≤8%            |
| 8   | 24h Transaction Count      | ≥80            |
| 9   | Dev Rug-Pull History       | = 0            |
| 10  | Dev Coins Launched         | ≤5             |

Score = passedCount / totalChecks × 100. Pass requires: all checks passed AND totalChecks ≥ 3.

### Honeypot Detection (Round-Trip Simulation)
1. Simulate BUY: WNATIVE → Token (record amountOut)
2. Simulate SELL: Token → WNATIVE (use amountOut as input)
3. Recovery ratio = sellOut / originalAmount × 100
4. <50% = honeypot (85% confidence) | =0 = honeypot (90%) | 50-80% = suspicious | >80% = normal

### Contract Risk Flags
isHoneypot → **BLOCK** | hasMintMethod → HIGH risk | isLpNotLocked → Rug risk | hasNotRenounced → MEDIUM | isInBlacklist → MEDIUM

---

## VI. Domain 4 — Wallet & Portfolio

| API               | Method | Path                                                                 |
| ----------------- | ------ | -------------------------------------------------------------------- |
| OKX Total Value   | GET    | /api/v6/dex/balance/total-value-by-address?address=&chains=          |
| OKX All Balances  | GET    | /api/v6/dex/balance/all-token-balances-by-address?address=&chains=   |
| OKX Token Balance | POST   | /api/v6/dex/balance/token-balances-by-address                        |
| Binance Positions | GET    | bapi/.../address/pnl/active-position-list?address=&chainId=&offset=0 |

Note: OKX excludeRiskToken is Boolean for total-value but String("0"/"1") for token-balances.
Native token: tokenContractAddress = "" (empty string).

---

## VII. Domain 5 — DEX Swap Execution

### OKX Aggregator (all GET)
| Endpoint                                                                                    | Purpose                          |
| ------------------------------------------------------------------------------------------- | -------------------------------- |
| /api/v6/dex/aggregator/quote?chainIndex=&fromTokenAddress=&toTokenAddress=&amount=          | Get quote                        |
| /api/v6/dex/aggregator/approve-transaction?chainIndex=&tokenContractAddress=&approveAmount= | ERC20 approval                   |
| /api/v6/dex/aggregator/swap?chainIndex=&...&slippagePercent=1&userWalletAddress=            | Swap calldata                    |
| /api/v6/dex/aggregator/swap-instruction?chainIndex=501&...                                  | Solana deserialized instructions |

Amount must be in minimal units (wei/lamports). Default slippage: 1%.

### Smart Router (V2/V3 Auto-Selection)
Query all routes in parallel → pick highest amountOut:
1. V2 Router `getAmountsOut(amountIn, [tokenIn, tokenOut])`
2. V3 Quoter `quoteExactInputSingle` across ALL fee tiers (100, 500, 3000, 10000)
3. Sort by amountOut descending → select best

**V2 Routers**: BSC `0x10ED43C718714eb63d5aA57B78B54704E256024E` | ETH `0x7a250d5630B4cF539739dF2C5dAcb4c659F2488D` | Base `0x4752ba5DBc23f44D87826276BF6Fd6b1C372aD24`
**V3 Routers**: ETH `0xE592427A0AEce92De3Edee1F18E0157C05861564` | Base `0x2626664c2603336E57B271c5C0b26F421741e481` | BSC `0x13f4EA83D0bd40E75C8222255bc855a974568Dd4`
**V3 Fees**: 100 (0.01% stables), 500 (0.05%), 3000 (0.3% most pairs), 10000 (1% exotic)

### Turbo Direct Pool (~15k-30k gas savings)
Bypass router, call pool contracts directly:
- V2: transfer token to pair → pair.swap(amount0Out, amount1Out, to, 0x)
- V3: fallback to SwapRouter exactInputSingle (EOA can't call pool.swap callback)
- V2 formula: `amountOut = amountIn×997×reserveOut / (reserveIn×1000 + amountIn×997)`

### Solana Auto-Dispatch
isPumpToken? → Pump.fun direct buy/sell : Jupiter aggregator

### Safety Patterns
- Approve ONLY required amount — **never maxUint256**
- Quote failure → **BLOCK trade** (prevents sandwich attacks)
- Slippage: `amountOutMin = expectedOut × (10000 - slippageBps) / 10000`

---

## VIII. Domain 6 — Broadcast & Tracking

| Endpoint                                                 | Method | Purpose               |
| -------------------------------------------------------- | ------ | --------------------- |
| /api/v6/dex/pre-transaction/gas-price?chainIndex=        | GET    | Gas price             |
| /api/v6/dex/pre-transaction/gas-limit                    | POST   | Gas limit estimate    |
| /api/v6/dex/pre-transaction/simulate                     | POST   | Tx simulation         |
| /api/v6/dex/pre-transaction/broadcast-transaction        | POST   | Broadcast signed tx   |
| /api/v6/dex/post-transaction/orders?address=&chainIndex= | GET    | Order status tracking |

Broadcast body: `{ "signedTx": "0x...", "chainIndex": "1", "address": "0x..." }`
MEV protection: `extraData: { "enableMevProtection": true }` (ETH/BSC/SOL/BASE)
txStatus: 1=Pending 2=Success 3=Failed

---

## IX. Domain 7 — Binance Spot

| Endpoint             | Method | Purpose              |
| -------------------- | ------ | -------------------- |
| /api/v3/order        | POST   | Place order          |
| /api/v3/order        | GET    | Query order          |
| /api/v3/order        | DELETE | Cancel order         |
| /api/v3/order/test   | POST   | Test order (no exec) |
| /api/v3/openOrders   | GET    | Open orders          |
| /api/v3/account      | GET    | Account info         |
| /api/v3/myTrades     | GET    | Trade history        |
| /api/v3/ticker/price | GET    | Ticker               |
| /api/v3/klines       | GET    | K-line               |
| /api/v3/depth        | GET    | Order book           |

Order types: MARKET, LIMIT, STOP_LOSS, STOP_LOSS_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT, LIMIT_MAKER
Advanced: OCO, OTO, OTOCO conditional orders

---

## X. Domain 8 — Gate.io Spot

Auth: HMAC-SHA512 (see Section I)

| Endpoint                | Method | Auth | Purpose                                     |
| ----------------------- | ------ | ---- | ------------------------------------------- |
| /spot/orders            | POST   | Yes  | Create order                                |
| /spot/orders            | GET    | Yes  | List orders (params: status, market, limit) |
| /spot/orders/{order_id} | GET    | Yes  | Get single order                            |
| /spot/orders/{order_id} | DELETE | Yes  | Cancel single order                         |
| /spot/orders            | DELETE | Yes  | Cancel all orders                           |
| /spot/accounts          | GET    | Yes  | Spot balance                                |
| /spot/tickers           | GET    | No   | Tickers                                     |
| /spot/order_book        | GET    | No   | Order book                                  |
| /spot/candlesticks      | GET    | No   | K-line                                      |
| /spot/currency_pairs    | GET    | No   | Trading pair rules                          |
| /wallet/total_balance   | GET    | Yes  | Total balance across all accounts           |

**Order params**: currency_pair ("BTC_USDT" underscore format), side (buy/sell), type (limit/market), amount, price, time_in_force (gtc/ioc/poc/fok), account ("spot")

Rate limit headers: `X-Gate-RateLimit-Requests-Remain`, `X-Gate-RateLimit-Limit`

---

## XI. Domain 9 — Bitget Spot

Auth: HMAC-SHA256 (see Section I)

| Endpoint                              | Method | Auth | Purpose                                   |
| ------------------------------------- | ------ | ---- | ----------------------------------------- |
| /api/v2/spot/trade/place-order        | POST   | Yes  | Place order                               |
| /api/v2/spot/trade/cancel-order       | POST   | Yes  | Cancel order (NOTE: uses POST not DELETE) |
| /api/v2/spot/trade/batch-orders       | POST   | Yes  | Batch place (max 50)                      |
| /api/v2/spot/trade/batch-cancel-order | POST   | Yes  | Batch cancel                              |
| /api/v2/spot/trade/orderInfo          | GET    | Yes  | Query single order                        |
| /api/v2/spot/trade/unfilled-orders    | GET    | Yes  | Open orders                               |
| /api/v2/spot/trade/history-orders     | GET    | Yes  | Order history                             |
| /api/v2/spot/trade/fills              | GET    | Yes  | Trade fills                               |
| /api/v2/spot/account/assets           | GET    | Yes  | Spot assets                               |
| /api/v2/spot/account/info             | GET    | Yes  | Account info                              |
| /api/v2/spot/market/tickers           | GET    | No   | Tickers                                   |
| /api/v2/spot/market/orderbook         | GET    | No   | Order book                                |
| /api/v2/spot/market/candles           | GET    | No   | K-line                                    |
| /api/v2/spot/market/fills             | GET    | No   | Recent trades                             |
| /api/v2/account/all-account-balance   | GET    | Yes  | All account balances                      |

**Order params**: symbol ("BTCUSDT" no separator), side (buy/sell), orderType (limit/market), force (gtc/ioc/fok/post_only), price, size, clientOid (idempotency key)

---

## XII. Domain 10 — Smart Money Signals

### Smart Money Trading Signals
POST `bapi/.../web/signal/smart-money`
Body: `{ "smartSignalType":"", "page":1, "pageSize":100, "chainId":"CT_501" }`
Chains: BSC (56), Solana (CT_501)

Key fields: direction (buy/sell), smartMoneyCount, alertPrice, currentPrice, maxGain (%), exitRate (%), status (active/timeout/completed)

Quality: Higher smartMoneyCount = more reliable. Low exitRate on active = smart money still holding.

### Smart Money Inflow Rank
POST `bapi/.../tracker/wallet/token/inflow/rank/query`
Body: `{ "chainId":"56", "period":"24h", "tagType":2 }`

### Social Hype Leaderboard
GET `bapi/.../pulse/social/hype/rank/leaderboard?chainId=&sentiment=All&targetLanguage=en&timeRange=1`
Returns AI-generated multilingual sentiment summaries.

---

## XIII. Domain 11 — Meme Rush

### Meme Rush Rank
POST `bapi/.../pulse/rank/list`
Body: `{ "chainId":"CT_501", "rankType":10, "limit":40 }`
rankType: 10=New (bonding curve) 20=Finalizing 30=Migrated to DEX

Protocols: Pump.fun (1001), Four.meme (2001), Moonshot (1010), Raydium (1005-1007), BONK (1008), Flap (2002)

Advanced filters: progress (curve %), holdersDevPercent, holdersSniperPercent, devSellPercent, tagDevWashTrading, excludeDevWashTrading

### Meme Exclusive Rank
GET `bapi/.../pulse/exclusive/rank/list?chainId=56`
Algorithm-scored Top 100 breakout potential memes.

### Topic Rush
GET `bapi/.../social-rush/rank/list?chainId=&rankType={10|20|30}&sort={10|20|30}`
rankType: 10=Latest 20=Rising (ATH $1k-$20k) 30=Viral (ATH >$20k)

---

## XIV. Domain 12 — PnL Leaderboard

GET `bapi/.../market/leaderboard/query?chainId=&period={7d|30d|90d}&tag={ALL|KOL}&pageNo=1&pageSize=25`
Filters: PNLMin/Max, winRateMin/Max, txMin/Max, volumeMin/Max
Returns: address, realizedPnl, winRate, totalVolume, topEarningTokens[], dailyPNL[]

---

## RPC Health-Aware Failover

Per-chain node health map: `{ url, healthy, latencyMs, failCount }`
1. Select: healthy nodes → sort by latency → return lowest
2. All unhealthy: return node with fewest failures (graceful degradation)
3. On success: reset failCount, update latencyMs
4. On failure: failCount++; ≥3 consecutive → mark unhealthy
5. Background probe every 30s: eth_blockNumber to all nodes, 5s timeout

---

## Risk Gates

| Condition                                        | Action                                |
| ------------------------------------------------ | ------------------------------------- |
| riskLevel=5 OR isHoneypot OR recovery<50%        | **BLOCK TRADE**                       |
| tax>10% OR quote failure OR priceImpact>30%      | **BLOCK TRADE**                       |
| riskLevel=4                                      | Strongly discourage, require override |
| 5%<tax≤10% OR impact>5%                          | Warn + confirm                        |
| liquidity<$1k                                    | Strongly discourage                   |
| $1k≤liquidity<$10k                               | Warn slippage                         |
| Safety score<60 OR checks<3                      | Warn, show failed items               |
| devWashTrading=1 OR devPercent>20% OR sniper>30% | Warn manipulation                     |
| Still on bonding curve                           | Warn high risk                        |
| Mainnet fund movement                            | **Require user CONFIRM**              |

---

## Workflows

**A: Discover → Verify → Execute**: Search → market data → 10-point safety scoring → honeypot sim → balance check → smart route quote → user CONFIRM → exact-amount approve → execute → track
**B: Portfolio Analysis**: Balance query → enrich holdings → flag risk → suggest actions
**C: Signal-Driven**: Smart money signals → inflow rank → safety filter → watchlist → execute via A
**D: CEX Spot**: Select exchange (Binance/Gate/Bitget) → validate params → mainnet CONFIRM → place order → status. Cross-CEX price comparison
**E: Meme Sniping**: Monitor rankType=10 → filter wash/social → 70-90% curve → smart money cross-ref → safety score → execute via A
**F: Copy-Trading**: PnL leaderboard → filter winRate>60% → query positions → cross-ref signals → research → report
**G: Topic Narrative**: Viral topics → AI summaries → lead tokens → quality verify → execute via A

---

## Error Handling

| Source       | Code          | Meaning           | Action                               |
| ------------ | ------------- | ----------------- | ------------------------------------ |
| OKX          | 50011         | Rate limited      | Exponential backoff + jitter         |
| OKX          | 81104         | Chain unsupported | Check /supported/chain               |
| OKX          | 81451         | Node failed       | Check gas/nonce/revert               |
| Binance Spot | -1021         | Timestamp drift   | Sync clock                           |
| Binance Spot | -2010         | Order rejected    | Check balance/permissions            |
| Gate.io      | 401           | Auth failed       | Verify KEY + SIGN                    |
| Gate.io      | 429           | Rate limited      | Check X-Gate-RateLimit headers       |
| Bitget       | 401           | Auth failed       | Verify KEY + SIGN + timestamp (±10s) |
| Solana       | 0xb           | Wrong address     | Use native SOL address               |
| EVM          | nonce too low | Already mined     | Fetch latest nonce                   |

**Timeout**: All APIs 10s timeout. On broadcast/order timeout → **check status before retry** (prevent double-spend).

---

## Core Rules

**Security**: Never output raw keys. Approve only required amounts. Mainnet ops require CONFIRM. Quote failure = block. See §XVI–§XVII for full credential handling rules.
**Units**: APIs use minimal units (wei/lamports); display uses UI units. amount_min = amount_ui × 10^decimal.
**Formats**: Gate.io uses underscore pairs "BTC_USDT"; Bitget uses no separator "BTCUSDT".
**Fallback**: OKX search ↔ Binance search, OKX candles ↔ Sintral K-line, OKX balance ↔ Binance positions. CEX failure → suggest alternative exchange.
**RPC**: Auto-failover via health manager. 30s probe, 5s timeout, 3 consecutive failures = unhealthy.
**Output**: Concise decision summaries → risk flags first → blocked trades get reason + alternatives → disclaimer at end.

**Defaults**: slippage=1% | ranking pageSize=20-50 | signals=active only | meme default=rankType=20 (migration) | PnL=30d | V3 fee=3000 | tx deadline=300s

---

## XVI. Credential & Environment Variable Registry

This skill requires credentials for 5 providers. Below is the **complete registry** of all
environment variables, their purpose, and security classification.

### Required Environment Variables

| Variable               | Provider          | Purpose                  | Sensitivity |
| ---------------------- | ----------------- | ------------------------ | ----------- |
| `OKX_API_KEY`          | OKX DEX           | HMAC signing (key)       | 🔴 Secret    |
| `OKX_SECRET_KEY`       | OKX DEX           | HMAC signing (secret)    | 🔴 Secret    |
| `OKX_PASSPHRASE`       | OKX DEX           | API passphrase           | 🔴 Secret    |
| `BINANCE_API_KEY`      | Binance Spot      | Request header auth      | 🔴 Secret    |
| `BINANCE_SECRET_KEY`   | Binance Spot      | HMAC signing             | 🔴 Secret    |
| `GATE_API_KEY`         | Gate.io           | Request header auth      | 🔴 Secret    |
| `GATE_SECRET_KEY`      | Gate.io           | HMAC-SHA512 signing      | 🔴 Secret    |
| `BITGET_API_KEY`       | Bitget            | Request header auth      | 🔴 Secret    |
| `BITGET_SECRET_KEY`    | Bitget            | HMAC signing             | 🔴 Secret    |
| `BITGET_PASSPHRASE`    | Bitget            | API passphrase           | 🔴 Secret    |
| `RPC_ETH`              | Ethereum RPC      | Chain interaction        | 🟡 Sensitive |
| `RPC_BSC`              | BSC RPC           | Chain interaction        | 🟡 Sensitive |
| `RPC_BASE`             | Base RPC          | Chain interaction        | 🟡 Sensitive |
| `RPC_ARB`              | Arbitrum RPC      | Chain interaction        | 🟡 Sensitive |
| `RPC_SOL`              | Solana RPC        | Chain interaction        | 🟡 Sensitive |
| `DEPLOYER_PRIVATE_KEY` | EVM tx signing    | On-chain trade execution | 🔴 Critical  |
| `SOL_PRIVATE_KEY`      | Solana tx signing | On-chain trade execution | 🔴 Critical  |
| `VAULT_TIMEOUT_MS`     | Vault             | Auto-lock duration       | ⚪ Config    |
| `ENABLE_TESTNET`       | Routing           | Route through testnets   | ⚪ Config    |

### Sensitivity Levels

```
⚪ Config:     Safe to commit to .env.example as placeholder values
🟡 Sensitive:  Must be in .env (gitignored), contains API keys or RPC endpoints with keys
🔴 Secret:     Must NEVER appear in logs, code, or git history
🔴 Critical:   Private keys — highest security; compromise = total fund loss
```

### Agent Behavior: When to Request Credentials

```
Rule 1: NEVER invent, generate, or hardcode real API keys or secrets.
        Use placeholder values in .env.example only.
Rule 2: When scaffolding, create .env.example with descriptive placeholders:
        OKX_API_KEY=your-okx-api-key
        OKX_SECRET_KEY=your-okx-secret-key
        DEPLOYER_PRIVATE_KEY=0x_DO_NOT_COMMIT_REAL_KEY
Rule 3: Add .env to .gitignore BEFORE any .env file is created.
Rule 4: When a feature needs a credential not yet configured:
        → Tell the user which variable is needed and which provider dashboard to get it from
        → Provide the provider's API key management URL:
          - OKX: https://www.okx.com/account/my-api
          - Binance: https://www.binance.com/en/my/settings/api-management
          - Gate.io: https://www.gate.io/myaccount/apikeys
          - Bitget: https://www.bitget.com/account/newapi
          - Alchemy (RPC): https://dashboard.alchemy.com
        → Ask the user to set it in .env
        → NEVER ask the user to paste secrets into chat
Rule 5: For DEPLOYER_PRIVATE_KEY / SOL_PRIVATE_KEY:
        → Recommend generating locally (cast wallet new, solana-keygen new)
        → For mainnet: use hardware wallet or the project Vault system
        → NEVER use a funded mainnet key in .env on a dev machine
Rule 6: When implementing auth signing functions:
        → Load secrets with process.env.* at module init
        → Validate presence at startup: if (!key) throw new Error('Missing OKX_API_KEY')
        → NEVER pass secrets as function parameters through the call stack
Rule 7: Agent Scope Limits (Infrastructure):
        → The agent runs purely as a trading helper. Infrastructure secrets 
          (e.g., DATABASE_URL, REDIS_URL, JWT_SECRET) are EXPLICITLY OUT OF SCOPE.
        → NEVER attempt to read, request, or persist data directly using backend services.
        → All state must be passed through safe API layers, never via direct DB connections.
```

---

## XVII. Security: Agent Rules for Sensitive Key Handling

Mandatory rules for any AI agent following this skill when handling API keys, private keys,
and credential material during development, testing, and deployment.

### Agent MUST Rules (Non-Negotiable)

```
1. NEVER echo, log, print, or return API keys/secrets to stdout, stderr, or chat.
   Masking rule: key.slice(0,4) + '****' + key.slice(-4)
2. NEVER include real secrets in code, comments, commit messages, or artifacts.
3. NEVER store secrets in source-controlled files.
   Only .env (which MUST be in .gitignore) may contain real credentials.
4. NEVER transmit secrets over unencrypted channels or embed in URLs.
5. When writing HMAC signing utilities:
   → Secret key MUST come from process.env exclusively
   → The signing function MUST NOT log the computed signature in production
   → Timestamp synchronization: use server time diff calibration
6. When writing trade execution code:
   → Private keys MUST be decrypted from Vault at execution time only
   → Zero-fill key Buffer after use: keyBuffer.fill(0)
   → NEVER cache decrypted private keys in global scope
7. When writing Docker/CI configs:
   → Use secrets managers (Docker secrets, GitHub Actions secrets)
   → NEVER bake API keys into Docker images or CI YAML
8. When implementing CEX API clients:
   → Use IP whitelisting where the exchange supports it (all 4 do)
   → Enable TRADE-ONLY permissions — WITHDRAWAL PERMISSION MUST BE DISABLED on all keys
   → Implement separate key pairs for spot vs futures (Gate.io requirement)
   → Verify no withdrawal permission is enabled before any integration test
9. Principle of Least Privilege enforcement:
   → OKX:     Read + Trade. Withdrawal = OFF. IP whitelist = REQUIRED.
   → Binance:  Read + Trade. Withdrawal = OFF. Margin = OFF unless explicitly needed.
   → Gate.io:  Spot trade only. Futures = SEPARATE key. Withdrawal = OFF.
   → Bitget:   Read + Trade. Withdrawal = OFF. IP whitelist recommended.
   → EVM key:  Dedicated wallet, minimal balance, never a primary wallet.
   → SOL key:  Dedicated wallet, minimal balance, never a primary wallet.
10. Testnet-first mandate:
    → Set ENABLE_TESTNET=true and test ALL workflows on testnets BEFORE mainnet.
    → Binance testnet: testnet.binance.vision
    → Only after successful testnet validation may the agent proceed to mainnet.
```

### Exchange-Specific Security Notes

| Exchange | Key Rotation       | IP Whitelist           | Permission Granularity                 | Notes                                           |
| -------- | ------------------ | ---------------------- | -------------------------------------- | ----------------------------------------------- |
| OKX      | 90-day recommended | ✅ Required for trade   | Read / Trade / Withdraw                | Passphrase adds extra layer                     |
| Binance  | No expiry, manual  | ✅ Strongly recommended | Read / Trade / Withdraw / Margin       | Enable HMAC-only (no Ed25519) for compatibility |
| Gate.io  | No expiry, manual  | ✅ Available            | Spot / Futures / Withdrawal (separate) | Spot and Futures need SEPARATE key pairs        |
| Bitget   | No expiry, manual  | ✅ Available            | Read / Trade / Withdraw                | Passphrase required; ±10s timestamp tolerance   |

### Credential Lifecycle

```
┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐
│   GENERATION     │───▶│    STORAGE       │───▶│     USAGE        │
│                  │    │                  │    │                  │
│ Exchange UI      │    │ .env file (dev)  │    │ process.env.*    │
│ cast wallet new  │    │ Vault (prod)     │    │ Vault decrypt    │
│ solana-keygen    │    │ Docker secrets   │    │ HMAC sign()      │
└──────────────────┘    └──────────────────┘    └───────┬──────────┘
                               │                        │
                         ┌─────▼──────┐          ┌──────▼─────┐
                         │  ROTATION  │          │  CLEANUP   │
                         │ API: 90d   │          │ Zero-fill  │
                         │ JWT: 15m   │          │ Buffer     │
                         │ Refresh:7d │          │ after use  │
                         └────────────┘          └────────────┘
```

### .env.example Template

The agent MUST generate this file when scaffolding a project using this skill:

```bash
# === OKX DEX Aggregator (https://www.okx.com/account/my-api) ===
OKX_API_KEY=your-okx-api-key
OKX_SECRET_KEY=your-okx-secret-key
OKX_PASSPHRASE=your-okx-passphrase

# === Binance Spot (https://www.binance.com/en/my/settings/api-management) ===
BINANCE_API_KEY=your-binance-api-key
BINANCE_SECRET_KEY=your-binance-secret-key

# === Gate.io Spot (https://www.gate.io/myaccount/apikeys) ===
# NOTE: Spot and Futures require SEPARATE key pairs
GATE_API_KEY=your-gate-spot-api-key
GATE_SECRET_KEY=your-gate-spot-secret-key

# === Bitget Spot (https://www.bitget.com/account/newapi) ===
BITGET_API_KEY=your-bitget-api-key
BITGET_SECRET_KEY=your-bitget-secret-key
BITGET_PASSPHRASE=your-bitget-passphrase

# === Blockchain RPC (https://dashboard.alchemy.com) ===
RPC_ETH=https://eth-mainnet.g.alchemy.com/v2/YOUR_KEY
RPC_BSC=https://bsc-dataseed1.binance.org
RPC_BASE=https://base-mainnet.g.alchemy.com/v2/YOUR_KEY
RPC_ARB=https://arb-mainnet.g.alchemy.com/v2/YOUR_KEY
RPC_SOL=https://api.mainnet-beta.solana.com

# === On-Chain Signing (NEVER commit funded mainnet keys) ===
# Generate a fresh dedicated wallet: cast wallet new (EVM) | solana-keygen new (Solana)
# Use a SMALL-BALANCE ONLY wallet. NEVER use a primary/funded mainnet wallet here.
DEPLOYER_PRIVATE_KEY=
# ↑ Leave blank. Populate ONLY with a freshly generated, isolated dev/test wallet key.
SOL_PRIVATE_KEY=
# ↑ Leave blank. Base58 key — generate with: solana-keygen new --no-bip39-passphrase

# === Infrastructure ===
# NOTE: Trade_Tool backend services manage their own standalone configuration.
# Infrastructure secrets (DB, Redis, JWT) are completely isolated from this agent skill.
VAULT_TIMEOUT_MS=28800000
ENABLE_TESTNET=true
```

---

## XVIII. Pre-Install Security Checklist

Before activating this skill with live credentials, verify every item below:

| #   | Check                                                                                                                              | Status |
| --- | ---------------------------------------------------------------------------------------------------------------------------------- | ------ |
| 1   | **Testnet first** — `ENABLE_TESTNET=true` tested successfully before mainnet                                                       | ☐      |
| 2   | **Dedicated wallets** — `DEPLOYER_PRIVATE_KEY` / `SOL_PRIVATE_KEY` are fresh wallets with minimal balance, not your primary wallet | ☐      |
| 3   | **Withdrawal disabled** — All CEX API keys (OKX / Binance / Gate / Bitget) have withdrawal permission explicitly OFF               | ☐      |
| 4   | **IP whitelist enabled** — All exchange API keys locked to your server's IP address                                                | ☐      |
| 5   | **Trade-only scope** — No Margin, Futures, or Cross-account permissions granted unless required                                    | ☐      |
| 6   | **Secrets in .env only** — Credentials stored in `.env` (gitignored), never in source code or chat                                 | ☐      |
| 7   | **Vault for mainnet** — Production keys stored in the project Vault system, not plain `.env`                                       | ☐      |
| 8   | **Provenance verified** — Skill source confirmed at `https://github.com/StanPoldark/Trade_Tool`                                    | ☐      |
| 9   | **Metadata in sync** — `requiredEnv` in YAML frontmatter matches §XVI table (verify: diff the `name:` fields in the YAML block against the §XVI Variable column, zero delta expected) | ☐      |
| 10  | **Small balance test** — First mainnet trade uses smallest viable amount to validate integration                                   | ☐      |

> **How to use**: Copy this checklist into your project's `SECURITY.md` and confirm each item before
> going live. Skip any item only if that provider is not used in your deployment.

---

⚠️ This skill provides operational reference only and does not constitute investment advice. Always DYOR.
