---
name: sell-the-news
description: Use Sell The News for real-time market news, WallStreetBets analysis, stock news, options data, news search, and Trump Truth Social market-impact posts. Trigger when the user wants live financial news, wants to read or summarize data from sellthenews.org, wants to query the hosted Sell The News endpoint directly from shell/OpenClaw, or needs help debugging client compatibility issues such as Streamable HTTP vs SSE.
---

# Sell The News skill

Use this skill to interact with the official Sell The News hosted endpoint:

- Endpoint: `https://mcp.sellthenews.org/mcp`
- Protocol: Streamable HTTP
- Auth: none

Use the bundled shell wrappers instead of reimplementing ad hoc HTTP calls.

## Workflow

1. Use `scripts/stn_mcp_call.sh <tool_name> [json_args]` for generic calls.
2. Prefer the per-tool wrappers when the requested operation maps directly.
3. If a user reports connection issues in another client, check protocol mismatch first:
   - this server uses **Streamable HTTP**
   - do **not** configure it as SSE
4. If a direct MCP client is unavailable, these shell wrappers are the fallback.

## Available tools

- `get_live_news`
  - Latest WSJ/NYT/Bloomberg/FT news
  - Common params: `limit`, `offset`, `lang`, `sources`, `marketOnly`, `before`
- `get_wsb_analysis`
  - AI analysis of daily r/wallstreetbets discussion
  - Common params: `lang`, `offset`, `run`
- `get_wsb_discussion`
  - Raw WSB comments with scores/threading
  - Common params: `limit`, `date`
- `get_stock_news`
  - News for a ticker
  - Required: `ticker`
  - Common params: `limit`, `offset`
- `get_options_data`
  - Options chain + Greeks exposure
  - Required: `ticker`
  - Common params: `expiration`, `greeks`
- `search_news`
  - Full-text search across indexed news
  - Required: `query`
  - Common params: `lang`, `sources`, `limit`, `offset`, `sort`
- `get_trump_posts`
  - Trump Truth Social posts with market-impact analysis
  - Common params: `lang`, `limit`, `offset`, `showAll`

## Bundled wrappers

- `scripts/stn_mcp_call.sh <tool_name> [json_args]`
- `scripts/get_live_news.sh [json_args]`
- `scripts/get_wsb_analysis.sh [json_args]`
- `scripts/get_wsb_discussion.sh [json_args]`
- `scripts/get_stock_news.sh [json_args]`
- `scripts/get_options_data.sh [json_args]`
- `scripts/search_news.sh [json_args]`
- `scripts/get_trump_posts.sh [json_args]`

## Examples

```bash
# latest Chinese live news
skills/sell-the-news/scripts/get_live_news.sh '{"lang":"zh","limit":5}'

# NVDA news
skills/sell-the-news/scripts/get_stock_news.sh '{"ticker":"NVDA","limit":10}'

# search tariff-related news
skills/sell-the-news/scripts/search_news.sh '{"query":"tariff","lang":"en","sort":"time","limit":10}'

# options data for SPY
skills/sell-the-news/scripts/get_options_data.sh '{"ticker":"SPY","greeks":"gamma,vanna"}'
```

## Notes

- Use `curl` for transport. In testing, `curl` worked while some simpler HTTP clients hit Cloudflare friction.
- The wrapper performs a short-lived MCP initialize request followed by a tool call.
- The server returns `text/event-stream`; the wrapper extracts JSON from `data:` lines.
- Keep requests read-only. This MCP is for retrieval/analysis.
