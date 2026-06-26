---
name: trongrid-block-info
description: "Query and analyze TRON blocks including producer info, transaction breakdown, rewards, burns, and network load. Use when a user asks about a specific block, latest block, block height, block rewards, block producer, transaction count, or network status. Supports single block lookup, block ranges, confirmed blocks, and multi-block trend analysis."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Block Info

Query and analyze TRON blocks — latest block data, block rewards, producer info, TRX burns, resource consumption, transaction breakdown, and network load trends.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Fetch Block Data

Choose the right tool based on the query:

| Query Type | Tool | Parameters |
|-----------|------|------------|
| Latest block | `getBlock` | none (omit `id_or_num`) |
| Latest confirmed block | `solidityGetBlock` | none (omit `id_or_num`) |
| Block by number | `getBlock` | `id_or_num=<height>`, `detail=false` |
| Block range | loop `getBlock` | `id_or_num=<height>` incrementing, `detail=false` |
| Latest N blocks | loop `getBlock` N times | start from latest, decrement `id_or_num` |
| Block statistics | `getBlockStatistics` | `blockNum` |

### Step 2: Parse Block Header

Extract from the block response:

- **Block Number** (height), **Block Hash**, **Timestamp**
- **Parent Hash** (link to previous block)
- **Witness Address** (producer SR)
- **Version** number

### Step 3: Identify Block Producer

1. Extract witness address from block header
2. Call `getPaginatedNowWitnessList` to match address to SR name/URL
3. Call `getBrokerage` for the producing SR to get reward distribution ratio

### Step 4: Analyze Block Transactions

1. Count and categorize transactions from block data: TRX transfers, TRC-10 transfers, smart contract calls, contract deployments, staking, voting, other
2. Call `getTransactionInfoByBlockNum` for receipts — reveals total fees, energy consumed, bandwidth consumed, success/failure counts

### Step 5: Calculate Rewards & Burns

From transaction receipts:
- **Block Reward**: 16 TRX per block (current parameter)
- **TRX Burned**: Sum of energy/bandwidth/account creation fees burned
- **SR Revenue**: Block reward + allocated transaction fees

### Step 6: Assess Network Load

Compare block metrics against capacity:
- Transaction density vs. block capacity
- Energy/bandwidth utilization rates
- For trends, loop `getBlock` 10–20 times (decrementing `id_or_num`) and compare

### Step 7: Check Block Events

Call `getEventsByBlockNumber` for smart contract events (DeFi swaps, token transfers, governance actions).

### Step 8: Compile Block Report

```
## Block #[number]

### Overview
- Hash: [hash]
- Time: [timestamp]
- Producer: [SR name] ([address])
- Brokerage: [X%]

### Transactions
- Total: [count] (Success: [X], Failed: [Y])

| Type | Count | % |
|------|-------|---|
| TRX Transfer | XX | XX% |
| Contract Call | XX | XX% |
| Staking | XX | XX% |

### Economics
- Block Reward: [X] TRX
- Fees: [X] TRX | Burned: [X] TRX

### Resources
- Energy Used: [amount]
- Bandwidth Used: [amount]
- Network Load: [Low/Medium/High]
```

For multi-block trend queries:

```
## Network Status (Last [N] Blocks)
- Avg Transactions/Block: [count]
- Avg Block Time: [X.X]s
- Total TRX Burned: [amount]
- Current Height: #[number]
- Load Trend: [Increasing/Stable/Decreasing]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Block not found | Future block number or invalid hash | Check current height with `getBlock` (no params) first |
| Empty block | Block with zero transactions | Report as empty block — this is normal for low-activity periods |
| Range too large | Looping `getBlock` for many blocks | Split into smaller batches; avoid requesting more than 100 blocks in a single flow |
| No events | Block has no smart contract activity | Skip events section, note "No contract events in this block" |

## Examples

- [Get latest block details](examples/latest-block-details.md)
- [Analyze block rewards](examples/block-reward-analysis.md)
