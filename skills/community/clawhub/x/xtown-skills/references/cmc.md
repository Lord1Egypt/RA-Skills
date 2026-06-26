---
name: CoinMarketCap MCP
description: Fetches cryptocurrency market data, prices, technical analysis, news, and trends from the CoinMarketCap building in BNBTown.
building: CoinMarketCap
building_id: coinMarketCap
---

# CoinMarketCap Skill

Use this skill when the owner asks about a cryptocurrency's price, market analysis, coin comparisons, holder metrics, technical indicators, or news.

## When to Use

Owner says something like:
- "How is Solana doing?"
- "What's the price of BTC?"
- "Compare BTC, ETH, and SOL"
- "What are the latest trending cryptos?"

## Execution Protocol

To use this skill, the agent must physically walk to the CoinMarketCap building (`coinMarketCap`) and execute specific tools. 

### Step 1: Submit Task
```http
POST $XTOWN_SERVER_URL/agent/task
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{ "session_token": "<token>", "skill_id": "coinMarketCap" }
```
→ Wait for status `awaiting_params`.

### Step 2: Execute Tool
Call `/agent/task/execute` with the tool you want.

```http
POST $XTOWN_SERVER_URL/agent/task/execute
Authorization: Bearer <UNIBASE_PROXY_AUTH>
{
  "session_token": "<token>",
  "task_id": "<task_id>",
  "params": {
    "tool_name": "<name of tool>",
    "tool_args": { 
       <arguments>
    }
  }
}
```

## Available Tools (Direct CMC API)

### `search_cryptos`
Search for a coin and get its CMC `id`.
- **Args:** `query` (string) - Name or symbol to search for.
- **Endpoint:** `/v1/cryptocurrency/map`

### `get_crypto_quotes_latest`
Get current price, market cap, and volume data.
- **Args:** `id` (string) - Comma separated CMC IDs (e.g., "1,1027"). Or use `symbol` (e.g., "BTC,ETH").
- **Endpoint:** `/v2/cryptocurrency/quotes/latest`

### `get_crypto_info`
Get background info, logo, and links.
- **Args:** `id` (string) - Comma separated CMC IDs.
- **Endpoint:** `/v2/cryptocurrency/info`

### `get_trending_latest`
Get currently trending cryptocurrencies based on CMC search volume.
- **Args:** `limit` (number) - Default 10.
- **Endpoint:** `/v1/cryptocurrency/trending/latest`

### `get_gainers_losers`
Get top gainers/losers by price change.
- **Args:** `limit` (number), `time_period` (string: 1h, 24h, 7d), `sort_dir` (string: desc for gainers, asc for losers).
- **Endpoint:** `/v1/cryptocurrency/trending/gainers-losers`

---

## Example Prompt Workflow
```
User: "How is Solana doing?"
1. Walk to coinMarketCap building
2. Execute search_cryptos with query "solana" -> Get ID: 5426
3. Execute get_crypto_quotes_latest with id "5426" -> Get price
4. Execute get_crypto_info with id "5426" -> Get description/links
5. Reply back to user with a rich summary.
```
