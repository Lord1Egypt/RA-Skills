# Example: Latest Block Details

## User Prompt

```
What is the latest block on TRON?
```

## Expected Workflow

1. **Latest Block** → `getBlock()` (no params) → Block header + transactions
2. **Confirmed Block** → `solidityGetBlock()` (no params) → Latest irreversible block for comparison
3. **Block Transactions** → `getTransactionInfoByBlockNum(blockNum)` → Fee and receipt details
4. **SR List** → `getPaginatedNowWitnessList()` → Match witness address to SR name
5. **SR Brokerage** → `getBrokerage(witnessAddress)` → Reward distribution ratio

## Expected Output (Sample)

```
## Block Report

### Block Overview
- Block Number: #70,123,456
- Block Hash: 0000000004304560...
- Timestamp: 2026-03-11 10:30:00 UTC
- Block Version: 30

### Producer
- SR Address: TLyqzVGLV1srkB7dZ...
- SR Name: Binance Staking
- Brokerage Ratio: 20% (SR keeps 20%, voters get 80%)

### Transactions
- Total Transactions: 185
- Successful: 182 (98.4%)
- Failed: 3 (1.6%)

### Transaction Breakdown
| Type            | Count | Percentage |
|-----------------|-------|-----------|
| Contract Call   | 120   | 64.9%     |
| TRX Transfer    | 35    | 18.9%     |
| TRC-10 Transfer | 10    | 5.4%      |
| Staking         | 12    | 6.5%      |
| Other           | 8     | 4.3%      |

### Economics
- Block Reward: 16 TRX
- Total Fees: 42.5 TRX
- TRX Burned: 38.2 TRX
- Net SR Revenue: 20.3 TRX

### Resource Consumption
- Total Energy Used: 12,450,000
- Total Bandwidth Used: 185,000
- Network Load: Medium
```

## MCP Tools Used

| Tool | Call Count | Purpose |
|------|-----------|---------|
| `getBlock` | 1 | Latest block data (no params) |
| `solidityGetBlock` | 1 | Latest confirmed block (no params) |
| `getTransactionInfoByBlockNum` | 1 | Transaction receipts |
| `getPaginatedNowWitnessList` | 1 | SR identification |
| `getBrokerage` | 1 | SR reward ratio |
