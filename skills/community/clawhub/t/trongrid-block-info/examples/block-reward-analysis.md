# Example: Block Reward Analysis

## User Prompt

```
Who produced block #68000000 and how much TRX was burned?
```

## Expected Workflow

1. **Fetch Block** → `getBlock(68000000, detail=false)` → Block header with witness address
2. **Block Stats** → `getBlockStatistics(68000000)` → Fee stats, energy/net usage
3. **Transaction Info** → `getTransactionInfoByBlockNum(68000000)` → All transaction receipts
4. **SR Lookup** → `getPaginatedNowWitnessList()` → Match witness address to SR name
5. **SR Brokerage** → `getBrokerage(witnessAddress)` → Reward split

## Expected Output (Sample)

```
## Block #68,000,000 Report

### Block Overview
- Block Number: #68,000,000
- Timestamp: 2025-07-15 14:22:33 UTC

### Producer
- SR Address: TGj1Ej1qRzL9feLT...
- SR Name: Poloniex
- Brokerage: 20%

### Economics
- Block Reward: 16 TRX
- Transaction Fees: 28.3 TRX
- TRX Burned: 25.1 TRX
- SR Revenue: 16 + (28.3 - 25.1) = 19.2 TRX
  - SR keeps (20%): 3.84 TRX
  - Voter reward pool (80%): 15.36 TRX

### Transactions
- Total: 150 transactions
- Smart Contract Calls: 98 (65.3%)
- TRX Transfers: 30 (20.0%)
- Other: 22 (14.7%)

### Resource Consumption
- Total Energy Used: 9,800,000
- Total Bandwidth Used: 150,000
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBlock` | 1 | Block header data (`id_or_num=68000000, detail=false`) |
| `getBlockStatistics` | 1 | Block fee statistics |
| `getTransactionInfoByBlockNum` | 1 | Transaction receipts |
| `getPaginatedNowWitnessList` | 1 | SR name lookup |
| `getBrokerage` | 1 | Reward distribution |
