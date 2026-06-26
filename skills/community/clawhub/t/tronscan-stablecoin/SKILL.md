---
name: tronscan-stablecoin
description: |
  Analyze TRON stablecoin ecosystem: supply, holders, transfers, large transactions, blacklist, liquidity pools, TVL, key events.
  Supported stablecoins: USDT, USDC, USDD, TUSD.
  Use when user asks "stablecoin overview", "USDT supply", "stablecoin holders", "stablecoin blacklist", "stablecoin pool", "stablecoin TVL", "large stablecoin transfers", or "stablecoin mint/burn events".
  Do NOT use for single token deep dive (use tronscan-token-scanner); general token list (use tronscan-token-list).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Stablecoin

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getStableCoinOverview | Stablecoin overview | Supply, holder count for a stablecoin |
| getStableCoinTotalSupply | Total supply | Current total circulating supply of all stablecoins |
| getStableCoinTotalSupplyChange | Supply change trend | Historical chart of total supply changes |
| getStableCoinTopHolders | Top holders | Top stablecoin holders ranked by USDT/USDC/USDD/TUSD |
| getStableCoinHolderChange | Holder count trend | Daily holder count change over time |
| getStableCoinHolderBalanceOverview | Market cap distribution | Total market cap distribution across all stablecoins |
| getStableCoinDistribution | Holder distribution | Holder distribution for a specific stablecoin |
| getStableCoinDistributionChange | Distribution change | Historical change in holding distribution |
| getStableCoinTransferAmount | Transfer volume trend | Stablecoin transfer amount changes over time |
| getStableCoinBigAmount | Large transactions | Large stablecoin transactions (swap, liquidity, loan, etc.) |
| getStableCoinBlackList | Blacklist | Frozen addresses and amounts |
| getStableCoinPoolInfo | Pool detail | All stablecoin liquidity pool details |
| getStableCoinPoolOverview | Pool overview | Basic info for a specific pool |
| getStableCoinPoolChange | Pool liquidity change | Liquidity change chart for a pool |
| getStableCoinPoolTrend | Pool trend | Trend data for pool liquidity changes |
| getStableCoinTvl | Pool TVL | Stablecoin TVL distribution across pools |
| getStableCoinTokenSupplyTurnover | Supply & turnover trend | Supply and circulation trend for a specific stablecoin |
| getStableCoinKeyEvents | Key events | Mint/burn/freeze and other major operations |

## Use Cases

1. **Stablecoin overview**: Use `getStableCoinOverview` (optionally with `tokenAddress`) for supply and holder count; `getStableCoinTotalSupply` for all stablecoins combined.
2. **Supply trends**: Use `getStableCoinTotalSupplyChange` for total supply history; `getStableCoinTokenSupplyTurnover` for a single stablecoin's supply and turnover trend.
3. **Holder analysis**: Use `getStableCoinTopHolders` for top holders (sort by USDT/USDC/USDD/TUSD); `getStableCoinHolderChange` for holder count trend; `getStableCoinHolderBalanceOverview` for market cap distribution; `getStableCoinDistribution` and `getStableCoinDistributionChange` for holding concentration.
4. **Transfer activity**: Use `getStableCoinTransferAmount` for transfer volume trends; `getStableCoinBigAmount` for large transaction monitoring (filter by types: 0=all, 1=in, 2=out, 3=swap, 4=add liquidity, 5=remove liquidity, 6=deposit, 7=loan, 8=repayment, 9=withdrawal).
5. **Blacklist / risk**: Use `getStableCoinBlackList` for frozen addresses; `getStableCoinKeyEvents` for mint/burn/freeze events.
6. **Liquidity pools**: Use `getStableCoinPoolInfo` for all pools; `getStableCoinPoolOverview`, `getStableCoinPoolChange`, `getStableCoinPoolTrend` for a specific pool; `getStableCoinTvl` for TVL distribution.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getStableCoinOverview

- **API**: `getStableCoinOverview` — Get basic overview for stablecoins (supply, holders)
- **Use when**: User asks for "stablecoin overview", "USDT supply", or general stablecoin stats.
- **Input**: Optional `tokenAddress`.

### getStableCoinTotalSupply

- **API**: `getStableCoinTotalSupply` — Get current total circulating supply for all stablecoins
- **Use when**: User asks for "total stablecoin supply" or "how much USDT/USDC/USDD is on TRON".
- **Input**: None required.

### getStableCoinTotalSupplyChange

- **API**: `getStableCoinTotalSupplyChange` — Get chart data for total supply changes
- **Use when**: User asks for "stablecoin supply trend" or "supply history".
- **Input**: Optional `startTime`, `endTime` (in seconds).

### getStableCoinTopHolders

- **API**: `getStableCoinTopHolders` — Get top stablecoin holders ranking
- **Use when**: User asks for "top stablecoin holders" or "who holds the most USDT".
- **Input**: Optional `sort` (USDT | USDC | USDD | TUSD), `direction` (1=asc, 2=desc), `viewContract` (1=include, 2=exclude).

### getStableCoinHolderChange

- **API**: `getStableCoinHolderChange` — Get stablecoin holder count change over time
- **Use when**: User asks for "stablecoin holder growth" or "holder count trend".
- **Input**: Optional `startDay`, `endDay` (yyyy-MM-dd).

### getStableCoinHolderBalanceOverview

- **API**: `getStableCoinHolderBalanceOverview` — Get market cap distribution across all stablecoins
- **Use when**: User asks for "stablecoin market cap distribution" or "USDT vs USDC market share".
- **Input**: None required.

### getStableCoinDistribution

- **API**: `getStableCoinDistribution` — Get holder distribution for a specific stablecoin
- **Use when**: User asks for "USDT holder distribution" or "stablecoin concentration".
- **Input**: Optional `token` (token address).

### getStableCoinDistributionChange

- **API**: `getStableCoinDistributionChange` — Get holding distribution change chart for a specific stablecoin
- **Use when**: User asks for "distribution change over time".
- **Input**: Optional `token` (token address).

### getStableCoinTransferAmount

- **API**: `getStableCoinTransferAmount` — Get stablecoin transfer amount trend
- **Use when**: User asks for "stablecoin transfer volume" or "transfer activity trend".
- **Input**: Optional `startTime`, `endTime` (seconds), `type` (set to "addLine" for line chart data).

### getStableCoinBigAmount

- **API**: `getStableCoinBigAmount` — Get large stablecoin transactions (up to 50 records)
- **Use when**: User asks for "large stablecoin transfers", "whale transactions", or "stablecoin swap/loan activity".
- **Input**: `types` (required: 0=all, 1=in, 2=out, 3=swap, 4=add liquidity, 5=remove liquidity, 6=deposit, 7=loan, 8=repayment, 9=withdrawal); optional: `address`, `txUsd`, `txAmount`, `relatedAddress`, `relatedToken`, `startTime`, `endTime`, `limit` (max 50), `sortBy` (time|amount|usd), `asc`.

### getStableCoinBlackList

- **API**: `getStableCoinBlackList` — Get stablecoin blacklist (frozen addresses)
- **Use when**: User asks for "stablecoin blacklist", "frozen addresses", or "sanctioned USDT addresses".
- **Input**: Optional `tokenAddress`, `blackAddress`, `sort` (1=amount, 2=time), `direction`, `start`, `limit`.

### getStableCoinPoolInfo

- **API**: `getStableCoinPoolInfo` — Get all stablecoin liquidity pool details
- **Use when**: User asks for "stablecoin pools" or "liquidity pool list".
- **Input**: None required.

### getStableCoinPoolOverview

- **API**: `getStableCoinPoolOverview` — Get basic info for a specific stablecoin pool
- **Use when**: User asks for "pool overview" or provides a pool address.
- **Input**: Optional `pool` (pool contract address).

### getStableCoinPoolChange

- **API**: `getStableCoinPoolChange` — Get liquidity change chart for a pool
- **Use when**: User asks for "pool liquidity changes".
- **Input**: Optional `pool` (pool address).

### getStableCoinPoolTrend

- **API**: `getStableCoinPoolTrend` — Get pool liquidity trend data
- **Use when**: User asks for "pool trend" or "historical pool liquidity".
- **Input**: Optional `pool`, `startTimestamp`, `endTimestamp` (milliseconds; start after 2022-11-21).

### getStableCoinTvl

- **API**: `getStableCoinTvl` — Get stablecoin TVL distribution across liquidity pools
- **Use when**: User asks for "stablecoin TVL" or "how much stablecoin is in DeFi pools".
- **Input**: Optional `token` (token address).

### getStableCoinTokenSupplyTurnover

- **API**: `getStableCoinTokenSupplyTurnover` — Get supply and circulation trend for a specific stablecoin
- **Use when**: User asks for "USDT supply trend", "stablecoin turnover", or supply/circulation history for USDD/USDC/TUSD.
- **Input**: Optional `tokenAddress` (USDD | USDC | TUSD), `startTime`, `endTime` (seconds).

### getStableCoinKeyEvents

- **API**: `getStableCoinKeyEvents` — Get key stablecoin events (mint/burn/freeze/major operations)
- **Use when**: User asks for "stablecoin mint events", "USDT freeze events", or "key stablecoin operations".
- **Input**: Optional `start`, `limit`, `sort` (1=amount, 2=time), `direction`, `operatorAddress`, `startTime`, `endTime`, `startAmount`, `endAmount`; per-token event type filters: `usdt`, `usdc`, `usdd`, `tusd` (comma-separated event types).

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

## Notes

- For a stablecoin dashboard, combine: `getStableCoinOverview` + `getStableCoinTotalSupply` + `getStableCoinTopHolders` + `getStableCoinPoolInfo`.
- `getStableCoinBigAmount` requires `types` parameter; use `types: "0"` for all transaction types.
- Time parameters vary by tool: some use seconds (`startTime`/`endTime`), others use milliseconds (`startTimestamp`/`endTimestamp`). Check per-tool notes.
