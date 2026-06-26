---
name: trongrid-trx-info
description: "Query TRX token fundamentals including price, supply, burn rate, market cap, staking yield, and network economics. Use when a user asks about TRX price, market cap, supply dynamics, burn trends, TRX value, or wants to assess TRX tokenomics and network economics."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# TRX Info

Comprehensive TRX token analysis — real-time price, supply dynamics, burn rate, market cap, staking yield, and long-term value drivers.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Gather Core On-Chain Data

Run in parallel:

1. `getBurnTrx` — Total TRX burned (essential for deflationary analysis)
2. `getChainParameters` — Network parameters affecting TRX economics (fees, resource pricing)
3. `getEnergyPrices` — Historical energy pricing (impacts TRX demand)
4. `getBandwidthPrices` — Historical bandwidth pricing
5. `getBlock` (no params) — Latest block for current network activity context

### Step 2: Calculate Supply Metrics

- **Circulating Supply**: ~100B genesis TRX - burned TRX - staked TRX
- **Burn Rate**: Parse recent energy/bandwidth price history for daily burn estimates
- **Net Supply Change**: Block rewards to SRs (~460,800 TRX/day at 16 TRX/block) minus daily burns

### Step 3: Fetch Market Data

Web search for off-chain data (CoinGecko, CoinMarketCap, TronScan):
- TRX/USD and TRX/BTC price
- 24h volume, market cap
- Price change (24h, 7d, 30d)

### Step 4: Assess Staking Economics

1. `getPaginatedNowWitnessList` — Current SR list, vote counts, block production
2. `getBrokerage` — Top SRs' reward distribution ratios
3. Calculate approximate staking yield from block rewards and brokerage

### Step 5: Compile TRX Report

```
## TRX Overview

### Price & Market
- Price: $X.XX
- Market Cap: $X.XX B
- 24h Volume: $X.XX M
- 24h Change: +/-X.XX%

### Supply Dynamics
- Total Supply: XX,XXX,XXX,XXX TRX
- Burned: X,XXX,XXX,XXX TRX
- Circulating: XX,XXX,XXX,XXX TRX
- Daily Burn Rate: ~X,XXX,XXX TRX

### Network Economics
- Energy Price: X sun
- Bandwidth Price: X sun
- SR Block Reward: 16 TRX/block
- Est. Staking Yield: ~X.X%

### Value Assessment
- Supply Trend: [Deflationary/Inflationary]
- Key Drivers: [list]
- Network Activity: [analysis]
```

## Key Economic Factors

- **Burn rate**: Higher network usage = more TRX burned = deflationary pressure
- **Staking (Stake 2.0)**: Locks TRX, reducing circulating supply
- **Resource pricing**: Energy/bandwidth costs drive TRX demand for network usage
- **SR rewards**: Create ongoing demand through voting incentives

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| No price data from web | Search fails or rate-limited | Report on-chain data only, note "Market data temporarily unavailable" |
| `getBurnTrx` returns sun value | All values are in sun (1 TRX = 1,000,000 sun) | Always divide by 1,000,000 for display |
| Energy price string format | Returns comma-separated `timestamp:price` pairs | Parse last entry for current price |
| Staking yield estimate varies | Depends on total votes and SR brokerage | Note as approximate, explain calculation assumptions |

## Examples

- [TRX price and supply analysis](examples/trx-price-and-supply.md)
- [TRX burn rate analysis](examples/trx-burn-analysis.md)
