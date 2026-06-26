---
name: tronscan-realtime-network
description: |
  Query TRON real-time network data: latest block height, current TPS, node count,
  latest TVL, total transaction count, real-time vote count.
  Use when user asks "real-time TPS", "current block height", "node count", "TVL", "total tx count", or network status.
  Do NOT use for historical trends (use tronscan-data-insights); block details (use tronscan-block-info).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Realtime Network Data

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getLatestBlock | Latest solidified block | Solidified block height, hash, timestamp, witness, tx count |
| getCurrentTps | TPS & height | Current TPS, latest block height, historical max TPS |
| getHomepageData | Homepage summary | TPS, node count, chain overview, TVL, frozen |
| getNodeMap | Node map | Real-time node info and geographic distribution |
| getWitnessGeneralInfo | Witness aggregate | Total vote count, block stats, witness count |
| getTransactionStatistics | Tx statistics | Total tx count, token tx volume aggregates |

## Use Cases

1. **Latest solidified block / confirmed block height**: Use `getLatestBlock` for solidified block (not chain-head latest); use `getCurrentTps` for latest block height.
2. **Real-time TPS**: Use `getCurrentTps` for current TPS; use `getHomepageData` for overview TPS.
3. **Real-time node count**: Use `getHomepageData` for node count; use `getNodeMap` for node list and distribution.
4. **Latest TVL**: Use `getHomepageData` for latest TVL in homepage overview.
5. **Total transaction count**: Use `getTransactionStatistics` for total tx count and token tx volume.
6. **Real-time vote count**: Use `getWitnessGeneralInfo` for total vote count and witness stats.


## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getLatestBlock

- **API**: `getLatestBlock` — Calls `/api/block/latest`; returns latest **solidified** block (number, hash, size, timestamp, witness, tx count). Note: Returns solidified block, not the chain-head latest block.
- **Use when**: User asks for "confirmed block", "solidified block height", or needs a stable block number. If user asks "latest block height" or "current block", clarify that the response is the solidified block and may lag behind the chain head.
- **Response**: number (block height), hash, size, timestamp, witness, tx count, etc.
- **Note**: Fields such as `witnessName`, `fee`, `energyUsage`, `blockReward`, `voteReward`, `confirmations`, `netUsage` may be 0 or null (underlying API does not return them)—ignore them. Use **tronscan-block-info** `getBlocks` when these fields are needed.

### getCurrentTps

- **API**: `getCurrentTps` — Get current TPS, latest block height, and historical max TPS
- **Use when**: User asks for "real-time TPS", "current TPS", "throughput", or "latest block height".
- **Response**: currentTps, latest block height, historical max TPS.

### getHomepageData

- **API**: `getHomepageData` — Get homepage data (TPS, node count, overview, frozen, TVL, etc.)
- **Use when**: User asks for "network overview", "node count", "TVL", or "homepage stats".
- **Response**: TPS, node count, chain overview, frozen resources, TVL, etc.

### getNodeMap

- **API**: `getNodeMap` — Get current node info and geographic distribution
- **Use when**: User asks for "node count", "node distribution", or "node map".
- **Response**: Current node info and geographic distribution.

### getWitnessGeneralInfo

- **API**: `getWitnessGeneralInfo` — Get witness aggregate stats (total votes, block stats, witness count)
- **Use when**: User asks for "real-time vote count", "total votes", or "witness stats".
- **Response**: Total vote count, block stats, witness count.

### getTransactionStatistics

- **API**: `getTransactionStatistics` — Get transaction statistics (total tx, token tx volume, etc.)
- **Use when**: User asks for "total transaction count" or "tx volume".
- **Response**: Total tx count, token tx volume, and other aggregates.

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

## Notes

- For a single "real-time network" dashboard, prefer `getHomepageData` first (covers TPS, nodes, TVL); then add `getCurrentTps` for precise TPS/height, `getWitnessGeneralInfo` for votes, and `getTransactionStatistics` for total tx count.
- All tools are invoked via TronScan MCP `tools/call` with the tool name and required arguments.
- `getLatestBlock` may return 0/null for `witnessName`, `blockReward`, `voteReward`, `fee`, `energyUsage`, `netUsage`, `confirmations`; use **tronscan-block-info** `getBlocks` when these fields are needed.
