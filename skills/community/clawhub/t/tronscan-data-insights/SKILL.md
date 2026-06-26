---
name: tronscan-data-insights
description: |
  TRON network insights: new accounts, daily tx count, tx type distribution,
  hot tokens, hot contracts, top accounts by tx count or staked TRX.
  Use when user asks "what is happening on TRON", "new accounts", "daily new addresses", "hot tokens", "network activity", "accounts with most TRX transfers yesterday", "TRX staking rankings".
  Do NOT use for single token details (use tronscan-token-scanner); single address profiling (use tronscan-account-profiler); non-TRX token transfer count rankings; non-TRX token transfer volume rankings.
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Data Insights

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getDailyNewAccounts | Daily new accounts | Daily new addresses (newAddressSeen), up to 2000 days |
| getTransactionStatistics | Tx statistics | Total tx, token tx volume, aggregates |
| getTransferStatistics | Transfer stats | Transfer activity by token type |
| getTriggerStatistic | Contract triggers | Daily contract call count |
| getTop10 | Top10 rankings | Multiple dimensions (time, category) |
| getHotSearch | Hot tokens/contracts | Hot tokens and contracts with metrics |
| getHomepageData | Homepage data | TPS, node count, overview, TVL, frozen |
| getCurrentTps | Current TPS | Current TPS, latest height, historical max TPS |
| getTriggerAmountStatistic | Trigger by date | Contract call volume distribution by date |
| getContractCallerStatisticOverview | Caller overview | Contract caller stats (default 7d) |
| getActiveStatistic | Active accounts | Active account count per day/week/month |
| getDailyAvgBlockSize | Avg block size | Daily average block size |
| getDailyTransactionNum | Daily tx trend | Transaction trend data |
| getDefiTvl | DeFi TVL | Daily DeFi TVL statistics |
| getEnergyDailyStatistic | Energy daily stats | Daily energy consumption ranked by contract |
| getEnergyStatistic | Energy distribution | Energy consumption by day/month/quarter |
| getMultipleChainQuery | Cross-chain query | TRON address mapping on other chains |
| getNetStatistic | Bandwidth stats | Bandwidth consumption per day/month/quarter |
| getStatsOverview | Stats overview | Daily stats: transfers, accounts, resources, tokens |
| getTotalBlockchainSize | Blockchain size | Cumulative on-chain size |
| getTransactionNum | Cumulative txs | Cumulative transactions per day |
| getAcquisitionCostStatistic | Resource cost | Energy and bandwidth acquisition cost |

## Use Cases

1. **New accounts**: Use `getDailyNewAccounts` for daily new addresses (newAddressSeen).
2. **Active accounts**: Use `getActiveStatistic` for daily active addresses.
3. **Daily transaction count**: Use `getTransactionStatistics` and `getTriggerStatistic` for tx and contract call volume.
4. **Transaction type distribution**: Use `getTransactionStatistics` and `getTransferStatistics` for type/segment distribution.
5. **Hot tokens**: Use `getHotSearch` for trending tokens with price and activity.
6. **Hot contracts**: Use `getHotSearch` and `getTriggerStatistic` or `getTop10` for hot contracts.
7. **Top accounts by tx count**: Use `getTop10` with appropriate category (e.g. by tx count).
8. **Top account by staked TRX**: Use `getTop10` or account list sorted by frozen/stake (category as per API).

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getDailyNewAccounts

- **API**: `getDailyNewAccounts` — Get daily new account data (default last 15 days, max 2000 days)
- **Data source**: Returns `newAddressSeen` (daily new addresses). This is an activity proxy, not precise DAU.
- **Use when**: User asks for "new accounts", "daily new addresses", or "new accounts per day".
- **If user asks for DAU / daily active**: First declare that "this API returns daily new addresses, not precise DAU; it can be used as a reference but must not be presented as exact DAU".
- **Input**: Optional start/end or day count.
- **Response**: Daily new account series.

### getTransactionStatistics

- **API**: `getTransactionStatistics` — Get transaction statistics (total tx, token tx volume, etc.)
- **Use when**: User asks for "transaction count", "tx volume", or "network activity".
- **Response**: Aggregated tx and token volume.

### getTransferStatistics

- **API**: `getTransferStatistics` — Get transfer statistics by token type
- **Use when**: User asks for "transfer distribution" or "tx type distribution".
- **Response**: Transfer activity by type.

### getTriggerStatistic

- **API**: `getTriggerStatistic` — Get daily contract trigger data in a time range
- **Use when**: User asks for "contract calls per day" or "smart contract activity".
- **Input**: Time range.
- **Response**: Daily trigger count.

### getTop10

- **API**: `getTop10` — Get Top10 rankings (multiple time/category dimensions)
- **Use when**: User asks for "top 10 accounts", "most tx", "most staked TRX", or similar rankings.
- **Input**: Category, time range (as per API).
- **Response**: Top 10 list for selected dimension.

### getHotSearch

- **API**: `getHotSearch` — Get hot tokens and contracts (trading metrics and price data)
- **Use when**: User asks for "hot tokens", "hot contracts", or "trending on TRON".
- **Response**: Hot tokens/contracts with price and activity.

### getHomepageData

- **API**: `getHomepageData` — Get homepage data (TPS, node count, overview, frozen, TVL, etc.)
- **Use when**: User asks for "TRON overview" or "network summary".
- **Response**: TPS, nodes, overview, TVL, frozen.

### getCurrentTps

- **API**: `getCurrentTps` — Get current TPS, latest block height, and historical max TPS
- **Use when**: User asks for "current TPS" or "network throughput".
- **Response**: currentTps, latest block, max TPS.

### getTriggerAmountStatistic

- **API**: `getTriggerAmountStatistic` — Get contract call volume distribution by date
- **Use when**: User asks for "contract call distribution by date".
- **Response**: Contract call volume distribution by date.

### getContractCallerStatisticOverview

- **API**: `getContractCallerStatisticOverview` — Get contract caller statistics (default last 7 days)
- **Use when**: User asks for "who is calling contracts" or "caller overview".
- **Response**: Caller count, call frequency, and aggregate stats for contract callers.

### getActiveStatistic

- **API**: `getActiveStatistic` — Get active account data on the TRON blockchain by day/week/month
- **Use when**: User asks for "active accounts", "daily active users", "DAU", "WAU", "MAU", or "active address count".
- **Input**: `type` (required: DAY | WEEK | MONTH), `startTimestamp` (required: milliseconds).
- **Response**: Active account dataset for the selected time granularity.

### getDailyAvgBlockSize

- **API**: `getDailyAvgBlockSize` — Get daily average block size on TRON
- **Use when**: User asks for "block size trend" or "average block size".
- **Input**: Optional `days`.

### getDailyTransactionNum

- **API**: `getDailyTransactionNum` — Get transaction trend data on TRON
- **Use when**: User asks for "daily transaction count" or "tx trend".
- **Input**: Optional `type`, `days`.

### getDefiTvl

- **API**: `getDefiTvl` — Get daily DeFi TVL statistics on TRON
- **Use when**: User asks for "DeFi TVL", "total value locked", or "TVL trend".
- **Input**: Optional `type`, `startTime`, `endTime`, `project`.

### getEnergyDailyStatistic

- **API**: `getEnergyDailyStatistic` — Get daily energy consumption statistics ranked by contract
- **Use when**: User asks for "which contracts consume the most energy" or "daily energy ranking".
- **Input**: `day` (required), optional `limit`.

### getEnergyStatistic

- **API**: `getEnergyStatistic` — Get energy consumption distribution by day/month/quarter
- **Use when**: User asks for "energy consumption trend" or "network energy usage over time".
- **Input**: `startTimestamp`, `endTimestamp`, `type` (all required); optional `size`.

### getMultipleChainQuery

- **API**: `getMultipleChainQuery` — Query a TRON address's corresponding info on other blockchains
- **Use when**: User asks for "cross-chain address", "is this address on Ethereum too", or "multi-chain lookup".
- **Input**: `address` (required).

### getNetStatistic

- **API**: `getNetStatistic` — Get bandwidth consumption per day/month/quarter
- **Use when**: User asks for "bandwidth usage trend" or "network bandwidth statistics".
- **Input**: `startTimestamp`, `endTimestamp` (required); optional `type`, `limit`.

### getStatsOverview

- **API**: `getStatsOverview` — Get daily TRON stats: transfers, accounts, resources, tokens
- **Use when**: User asks for "TRON daily statistics overview" or "overall network stats".
- **Input**: Optional `days`.

### getTotalBlockchainSize

- **API**: `getTotalBlockchainSize` — Get cumulative on-chain block size
- **Use when**: User asks for "blockchain size" or "how large is the TRON chain".
- **Input**: Optional `days`.

### getTransactionNum

- **API**: `getTransactionNum` — Get cumulative transaction count per day
- **Use when**: User asks for "total transactions" or "cumulative tx count".
- **Input**: Optional `days`.

### getAcquisitionCostStatistic

- **API**: `getAcquisitionCostStatistic` — Get Energy and Bandwidth resource acquisition cost data
- **Use when**: User asks for "energy price", "bandwidth cost", or "resource acquisition cost trend".
- **Input**: Optional `startTimestamp`, `endTimestamp`, `limit`.

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

### Empty or unexpected results
Check time range parameters; some APIs have default limits (e.g. getDailyNewAccounts max 2000 days).

## Notes

- `getDailyNewAccounts` returns `newAddressSeen` (daily new addresses)—an activity proxy, not precise DAU. When the user asks for DAU / daily active, you must first declare that this is a new-address metric and must not be presented as exact DAU.
- Top accounts by "staked TRX" use `getTop10` with the appropriate category (see TronScan API list for category values).
- For a single dashboard of "what's happening", combine: `getHomepageData` + `getCurrentTps` + `getHotSearch` + `getTop10` + `getTransactionStatistics`.
