---
name: tronscan-token-list
description: |
  Get TRC20 token list on TRON with price, 24h change, 24h volume, market cap, holder count.
  Use when user asks "token list", "TRC20 list", "hot tokens", "trending tokens", or to discover quality projects.
  Do NOT use for single token deep dive (use tronscan-token-scanner).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Token List

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| getTokenList | Token list | Filter by type, sort by price/change/volume/mcap/holders |
| getPricedTokenList | Priced tokens | All tokens with price data |
| getTrc20TokenDetail | Single token | Full TRC20/721/1155 detail for list item |
| getHotSearch | Hot search | Hot tokens and contracts with metrics and price |
| getSearchBar | Search bar | Popular search results (hot token list) |

## Use Cases

1. **TRC20 Token List**: Use `getTokenList` with type filter for TRC20; use `getPricedTokenList` for tokens with price.
2. **Price & 24h Change**: Token list and priced list include price and change; use detail for full 24h data.
3. **24h Volume**: Available in list or detail (e.g. `getTrc20TokenDetail`) and in `getHotSearch`.
4. **Market Cap**: In token list/detail and hot search.
5. **Holder Count**: In token list/detail.
6. **Discover Quality Projects**: Sort by volume, market cap, or holders; combine with `getHotSearch` for trending.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### getTokenList

- **API**: `getTokenList` — Get token list with type filter and sort by price/change/volume/holders/mcap
- **Use when**: User asks for "token list", "TRC20 list", or "tokens by volume/mcap".
- **Input**: type, sort field, order, pagination.
- **Response**: List of tokens with key metrics.

### getPricedTokenList

- **API**: `getPricedTokenList` — Get all tokens with price data
- **Use when**: User asks for "tokens with price" or "priced token list".
- **Response**: Tokens with price and related fields.

### getTrc20TokenDetail

- **API**: `getTrc20TokenDetail` — Get TRC20/TRC721/TRC1155 token details (name, symbol, supply, holders, price, etc.)
- **Use when**: User needs full metrics for a token from the list (e.g. 24h volume, holders).
- **Input**: Contract address.

### getHotSearch

- **API**: `getHotSearch` — Get hot tokens and contracts (trading metrics and price data)
- **Use when**: User asks for "trending tokens" or "hot tokens on TRON".
- **Response**: Hot tokens/contracts with price and activity metrics.

### getSearchBar

- **API**: `getSearchBar` — Get popular search results (hot token list)
- **Use when**: User asks for "popular tokens" or "search suggestions".

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

## Notes

- For "quality projects", combine sort (volume, mcap, holders) with hot search and optional token detail for due diligence.
- List tools support pagination; use limit/skip or page/size as per TronScan MCP API.
- Token list items may include risk fields such as `tokenCanShow` and `tokenLevel`. If a token in the list has `tokenCanShow: false` or `tokenLevel` of `"3"` (Suspicious) / `"4"` (Unsafe), flag it to the user as potentially risky before recommending further analysis. See **tronscan-token-scanner** for full field semantics.
