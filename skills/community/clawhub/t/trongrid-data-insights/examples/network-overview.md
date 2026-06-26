# Example: Network Overview

## User Prompt

```
How is the TRON network doing today?
```

## Expected Workflow

1. **Latest Block** → `getBlock()` (no params) → Current block height and timestamp
2. **Chain Params** → `getChainParameters()` → Network configuration
3. **Node Info** → `getNodeInfo()` → Node status
4. **Burn Stats** → `getBurnTrx()` → Total TRX burned
5. **Recent Blocks** → loop `getBlock(id_or_num)` × 20 (decrement from latest) → Last 20 blocks
6. **Block Transactions** → `getTransactionInfoByBlockNum(N)` × 20 → Transaction receipts for each block
7. **Latest Events** → `getEventsByLatestBlock()` → Contract events
8. **SR List** → `getPaginatedNowWitnessList()` → Super Representatives
9. **Energy Prices** → `getEnergyPrices()` → Energy price history
10. **Bandwidth Prices** → `getBandwidthPrices()` → Bandwidth price history

## Expected Output (Sample)

```
## TRON Network Insights

### Network Overview
- Current Block Height: #70,123,500
- Estimated Daily Transactions: ~8,640,000
- Average Block Time: 3.0 seconds
- Transaction Success Rate: 98.2%
- Total TRX Burned (All Time): 16,234,567,890 TRX
- Network Nodes: 1,200+

### Daily Activity Estimate (from recent 20 blocks)
- Transactions per Block: ~300
- Smart Contract Calls: ~195 per block
- TRX Transferred: ~45,000 TRX per block

### Transaction Type Distribution
| Type                | Percentage | Est. Daily Count |
|---------------------|-----------|-----------------|
| Smart Contract Calls | 65.0%     | ~5,616,000      |
| TRX Transfers       | 20.0%     | ~1,728,000      |
| TRC-10 Transfers    | 5.0%      | ~432,000        |
| Staking Ops         | 6.5%      | ~561,600        |
| Other               | 3.5%      | ~302,400        |

### Hot Contracts (Most Called)
| Rank | Contract | Name      | Calls (20 blocks) | Category    |
|------|----------|-----------|-------------------|-------------|
| 1    | TR7N...  | USDT      | 2,400             | Stablecoin  |
| 2    | TKcE...  | SunSwap   | 850               | DEX         |
| 3    | TXJg...  | JustLend  | 420               | Lending     |

### Governance
- Total SRs/SR Partners: 27/100
- Top SR: Binance Staking (1.2B votes)
- Total Votes Cast: ~38,500,000,000

### Resource Economics
- Current Energy Price: 420 sun
- Current Bandwidth Price: 1,000 sun
- Energy Price Trend (7d): Stable
- Bandwidth Price Trend (7d): Stable

### Key Takeaways
- Network activity: Growing (8.6M est. daily transactions)
- Dominant activity: Smart contract calls (65%), driven by USDT transfers
- Notable patterns: SunSwap DEX activity increasing
- Ecosystem health: Strong — high transaction throughput, stable resource pricing
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBlock` | 1 | Current block height (no params) |
| `getChainParameters` | 1 | Network params |
| `getNodeInfo` | 1 | Node status |
| `getBurnTrx` | 1 | Total burned TRX |
| `getBlock` | 20 | Recent 20 blocks (loop, decrement `id_or_num`) |
| `getTransactionInfoByBlockNum` | 20 | Transaction receipts |
| `getEventsByLatestBlock` | 1 | Latest events |
| `getPaginatedNowWitnessList` | 1 | SR list |
| `getEnergyPrices` | 1 | Energy pricing |
| `getBandwidthPrices` | 1 | Bandwidth pricing |
