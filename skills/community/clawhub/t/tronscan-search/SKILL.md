---
name: tronscan-search
description: |
  Search TRON blockchain by name or keyword: resolve token/contract name to address,
  find accounts, transactions, or blocks.
  Use when user asks "USDT contract address", "token/contract address on TRON", "look up by name", or search by keyword.
  Do NOT use for token list (use tronscan-token-list); single token deep dive (use tronscan-token-scanner).
metadata:
  author: tronscan-mcp
  version: "1.0"
  mcp-server: https://mcp.tronscan.org/mcp
---

# Search

## Overview

| Tool | Function | Use Case |
|------|----------|----------|
| search | Blockchain search | Token/contract/account/tx/block by keyword or name |

## Use Cases

1. **Contract address by name**: User asks "USDT contract address" or "BTT contract on TRON" — use `search` with `term` (e.g. USDT, BTT) and optional `type: token` or `type: contract` to get matching tokens/contracts and their addresses (`token_id` / contract address).
2. **Token by symbol or name**: Same as above; filter by `type: token` for token-only results.
3. **Contract by name**: Use `search` with `type: contract` to find contracts by name or address.
4. **Account search**: Use `search` with `type: address` to search accounts.
5. **Transaction or block**: Use `search` with `type: transaction` or `type: block` when the user provides a tx hash or block number/keyword.

## MCP Server

- **Prerequisite**: [TronScan MCP Guide](https://mcpdoc.tronscan.org)

## Tools

### search

- **API**: `search` — Search the TRON blockchain for tokens, contracts, accounts, transactions, or blocks
- **Use when**: User asks for "USDT contract address", "find token by name", "search for contract X", or any lookup by name/keyword.
- **Input**: `term` (required, search keyword e.g. USDT, BTT, or contract name), optional `type` (token | address | contract | transaction | block), optional `start`, `limit`.
- **Response**: Matches per type; for tokens, each item includes `token_id` (contract address), `name`, `abbr`, `token_type`, and other metadata.

## Troubleshooting

- **MCP connection failed**: If you see "Connection refused", verify TronScan MCP is connected in Settings > Extensions.
- **API rate limit / 429**: TronScan API has call count and frequency limits when no API key is used. If you encounter rate limiting or 429 errors, go to [TronScan Developer API](https://tronscan.org/#/developer/api) to apply for an API key, then add it to your MCP configuration and retry.

### No results for search
Try broader keywords or different type filter (token | address | contract | transaction | block).

## Notes

- For "contract address by name" (e.g. USDT), call `search` with `term: "USDT"` and `type: "token"` (or omit type); the first or best match usually has `token_id` = TRC20 contract address (e.g. USDT = `TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t`).
- Use this skill before tronscan-token-scanner or tronscan-contract-analysis when the user only provides a name/symbol and you need the address to call other tools.
- Search result token items may include `tokenCanShow`. If a result has `tokenCanShow: false`, treat it as a risk signal and inform the user before proceeding. For full risk field semantics, see **tronscan-token-scanner**.
