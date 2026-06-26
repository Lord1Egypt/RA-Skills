---
name: trongrid-token-list
description: "Browse and rank TRC-20 and TRC-10 tokens on TRON with price, volume, market cap, holder count, and category filters. Use when a user wants to discover tokens, see token rankings, find trending tokens, compare tokens by market cap, or explore categories like stablecoins and DeFi tokens on TRON."
metadata:
  version: "1.0.0"
  mcp-server: trongrid
---

# Token List

List and profile TRC-20 and TRC-10 tokens on TRON using TronGrid MCP tools.

# MCP Server
- **Prerequisite**: [TronGrid MCP Guide](https://developers.tron.network/reference/mcp-api)

> **Scope note**: TronGrid has no "list all TRC-20" endpoint. TRC-20 queries require known contract addresses — either provided by the user or drawn from the built-in reference list below. TRC-10 assets can be listed in full via `listAllAssets`.

## Built-in TRC-20 Reference Addresses

Use these when the user asks for general token rankings without specifying addresses:

| Token | Symbol | Contract Address                     | Category   |
|-------|--------|--------------------------------------|------------|
| Tether | USDT   | `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t` | Stablecoin |
| USDD | USDD | `TXDk8mbtRbXeYuMNS83CfKPaYYT8XWv9Hz` | Stablecoin |
| SUN   | SUN    | `TSSMHYeV2uE9qYH95DqyoCuNCzEL1NvU3S` | DeFi       |
| JUST  | JST    | `TCFLL5dx5ZJdKnWuesXxi1VPwjLVmWZZy9` | DeFi       |
| WINkLink | WIN  | `TLa2f6VPqDgRE67v1736s7bJ8Ray5wYjU7` | Oracle     |
| USDJ  | USDJ   | `TMwFHYXLJaRUPeW6421aqXL4ZEzPRFGkGT` | Stablecoin |
| BitTorrent | BTT | `TAFjULxiVgT4qWk6UZwjqwZXTSaGaqnVp4` | Utility   |

## Instructions

### Step 1: Resolve Token Addresses

- If the user provides contract addresses → use them directly
- If the user asks for general rankings or categories → use the built-in reference list above, filtered by the requested category

### Step 2: Fetch TRC-20 Token Data

For each contract address, call in parallel:

1. `getTrc20Info` — Name, symbol, decimals, total supply
2. `getTrc20TokenHolders` (limit=5) — Top holders and total holder count estimate
3. `getContractInfo` — Contract settings, energy limit, origin address
4. `getContractTransactions` (limit=20) — Recent transaction activity

### Step 3: Fetch TRC-10 Asset List

For TRC-10 tokens (when requested):

1. `getPaginatedAssetIssueList` (limit=20-50) — Paginated TRC-10 list with supply, issuer, precision
2. `getAssetIssueByName` or `getAssetIssueById` — For specific TRC-10 lookups

### Step 4: Rank and Categorize

Since TronGrid returns no market price data, rank by available on-chain signals:

- **By holder count** (from `getTrc20TokenHolders`)
- **By recent activity** (transaction count from `getContractTransactions`)
- **By total supply** (from `getTrc20Info`)

**By Category**:
- Stablecoins: USDT, USDD, USDJ
- DeFi: SUN, JST, WIN
- Infrastructure / Utility: BTT

### Step 5: Compile Token List

```
## TRON Token Overview

### TRC-20 Tokens
| Token | Symbol | Total Supply | Holders (est.) | Recent Txs | Category |
|-------|--------|-------------|----------------|-----------|----------|

### TRC-10 Tokens (Top by Supply)
| Token | ID | Total Supply | Precision | Issuer |
|-------|----|-------------|-----------|--------|

> Note: Price and market cap data are not available via TronGrid. For market data, consult an external source.
```

## Quality Signals

When evaluating tokens, flag these patterns:
- Low holder count + high supply = potential wash trading or abandoned token
- Growing recent transaction count = active adoption
- Unverified contract (no ABI) + mint/pause functions = caution
- For "best" or "quality" queries, weigh holder count and tx activity heavily

## Error Handling

| Error | Cause | Resolution |
|-------|-------|------------|
| `getTrc20Info` returns empty | Invalid or non-TRC-20 contract address | Skip token, note "Not a valid TRC-20 contract" |
| `getTrc20TokenHolders` returns empty | Contract has no holders or very new token | Note "No holder data available" |
| User asks for token not in reference list | Unknown token | Ask user for the contract address |
| TRC-10 list very large | Thousands of TRC-10 assets exist | Use `getPaginatedAssetIssueList` with limit=20-50 |

## Examples

- [Top TRON tokens by market cap](examples/top-tron-tokens.md)
- [DeFi tokens on TRON](examples/defi-tokens.md)
