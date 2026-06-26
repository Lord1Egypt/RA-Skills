---
name: trongrid-data-insights
description: "Provide TRON network analytics including transaction volume, type distribution, hot contracts, trending tokens, active accounts, staking metrics, and resource economics. Use when a user asks about TRON network health, daily stats, trending activity, top contracts, most active accounts, ecosystem overview, or on-chain analytics."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Data Insights

Comprehensive TRON network analytics — activity metrics, transaction patterns, trending tokens/contracts, top accounts, governance status, and resource economics.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

## Instructions

### Step 1: Network Snapshot

Fetch current state (run in parallel):

1. `getBlock` (no params) — Current block height and timestamp
2. `getChainParameters` — Network configuration
3. `getNodeInfo` — Node count and sync status
4. `getBurnTrx` — Total TRX burned to date

### Step 2: Recent Block Activity

1. Get latest block height from `getBlock` (no params), then loop `getBlock` 20 times with decrementing `id_or_num`
2. For each block, call `getTransactionInfoByBlockNum` for transaction details

Calculate:
- **Avg transactions/block**: total txs / 20
- **Estimated daily transactions**: avg * ~28,800 (blocks/day at 3s interval)
- **Avg block time**: time delta between consecutive blocks
- **Success rate**: successful / total

### Step 3: Transaction Type Distribution

Categorize all transactions from the sample blocks:
- TRX Transfers, Smart Contract Calls, TRC-10 Transfers
- Staking Operations, Resource Delegation, Voting
- Account Creation, Other

### Step 4: Hot Contracts

1. Aggregate contract calls across recent blocks by contract address
2. For top contracts, call `getContractInfo` for names
3. Call `getTrc20Info` if the contract is a token
4. Rank by call frequency

### Step 5: Trending Tokens

1. From `getEventsByLatestBlock`, identify Transfer events
2. Aggregate transfer volume per token contract
3. For top tokens, call `getTrc20Info` for metadata
4. Use web search for price data if needed

### Step 6: Most Active Accounts

From recent transactions:
1. Rank addresses by transaction count sent
2. Rank by TRX value transferred
3. For top accounts, call `getAccount` to classify (exchange/bot/whale)

### Step 7: Governance & Staking

1. `getPaginatedNowWitnessList` — All Super Representatives, votes, block production stats
2. From chain parameters, derive staking metrics
3. `getEnergyPrices` and `getBandwidthPrices` — Resource price trends

### Step 8: Compile Insights Report

```
## TRON Network Insights

### Overview
- Block Height: #[number]
- Est. Daily Transactions: ~[count]
- Avg Block Time: [X.X]s
- Success Rate: [X.X%]
- Total Burned (All Time): [amount] TRX

### Transaction Distribution
| Type | % | Est. Daily |
|------|---|-----------|
| Contract Calls | XX% | ~XXX,XXX |
| TRX Transfers | XX% | ~XXX,XXX |
| Staking | XX% | ~XX,XXX |

### Hot Contracts
| Contract | Name | Calls | Category |
|----------|------|-------|----------|
| TXxx... | USDT | X,XXX | Stablecoin |

### Trending Tokens
| Token | Symbol | Transfers | Volume |
|-------|--------|----------|--------|

### Most Active Accounts
| Address | Tx Count | Type |
|---------|----------|------|

### Governance
- Top SR: [name] ([votes] votes)
- Total Votes: [amount]

### Resource Economics
- Energy Price: [X] sun | Trend: [Up/Down/Stable]
- Bandwidth Price: [X] sun | Trend: [Up/Down/Stable]

### Key Takeaways
- [Activity trend]
- [Dominant activity driver]
- [Notable patterns]
```

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| Block fetch timeout | Network congestion or large blocks | Reduce block count (try 10 instead of 20) |
| Incomplete tx info | Some `getTransactionInfoByBlockNum` calls fail | Use available data, note sample size in report |
| No events in latest block | Low activity period | Expand to more blocks or note "Low activity detected" |
| Energy/bandwidth price API returns long string | Historical data is comma-separated | Parse only the last entry for current price |

## Examples

- [Network overview dashboard](examples/network-overview.md)
- [Trending activity analysis](examples/trending-activity.md)
