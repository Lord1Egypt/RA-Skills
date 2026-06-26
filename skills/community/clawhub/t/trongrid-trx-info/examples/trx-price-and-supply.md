# Example: TRX Price and Supply

## User Prompt

```
How is TRX doing? What's the current price and supply?
```

## Expected Workflow

1. **Burn Data** → `getBurnTrx()` → Total TRX burned (in sun)
2. **Latest Block** → `getBlock()` → Current block height and network activity
3. **Chain Params** → `getChainParameters()` → Block rewards, fee settings
4. **Web Search** → "TRX price market cap CoinGecko 2026" → Current market data
5. **Energy Prices** → `getEnergyPrices()` → Latest energy price
6. **Bandwidth Prices** → `getBandwidthPrices()` → Latest bandwidth price
7. **SR List** → `getPaginatedNowWitnessList()` → Top SRs for staking yield calculation
8. **SR Brokerage** → `getBrokerage(topSR)` × 3 → Reward distribution ratios

## Expected Output (Sample)

```
## TRX Overview

### Price & Market
- Current Price: $0.228
- Market Cap: $19.8B
- 24h Volume: $650M
- 24h Change: +2.3%
- 7d Change: +5.1%
- Rank: #9 by market cap

### Supply Dynamics
- Total Genesis Supply: ~100,000,000,000 TRX
- Total Burned: 16,234,567,890 TRX (16.2%)
- Estimated Circulating Supply: ~86,800,000,000 TRX
- Daily Burn Rate: ~4,500,000 TRX
- Daily SR Rewards: ~460,800 TRX (16 TRX × 28,800 blocks)
- Net Daily Supply Change: -4,039,200 TRX (deflationary)

### Network Economics
- Current Energy Price: 420 sun
- Current Bandwidth Price: 1,000 sun
- SR Block Rewards: 16 TRX/block
- Average Staking Yield: ~4.2% APR

### Value Assessment
- Supply Trend: Deflationary (burn >> issuance)
- Key Drivers: USDT transfer activity, DeFi growth, staking demand
- Network Activity: ~8.6M daily transactions
- Ecosystem Health: Strong — TRON is the #1 chain for USDT transfers
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBurnTrx` | 1 | Total burned TRX |
| `getBlock` | 1 | Current block |
| `getChainParameters` | 1 | Network params |
| `getEnergyPrices` | 1 | Energy pricing |
| `getBandwidthPrices` | 1 | Bandwidth pricing |
| `getPaginatedNowWitnessList` | 1 | SR list |
| `getBrokerage` | 3 | SR reward ratios |
