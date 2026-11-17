---
name: unusual-whales-api
description: Query the Unusual Whales API for unusual options flow, dark pool prints, market tide, stock greek exposure, financial statements, and technical indicators.
version: 1.0.0
metadata:
  openclaw:
    primaryEnv: UW_API_KEY
    requires:
      env:
        - UW_API_KEY
    envVars:
      - name: UW_API_KEY
        required: true
        description: Unusual Whales API token (paid API plan or trial) from https://unusualwhales.com/dashboard/api. Sent only to https://api.unusualwhales.com as a Bearer token.
    homepage: https://api.unusualwhales.com/docs
---

# Unusual Whales API Skill

## Setup

- **Token:** read the Unusual Whales API token from the `UW_API_KEY` environment variable and send it as `Authorization: Bearer $UW_API_KEY`. Create a token at https://unusualwhales.com/dashboard/api. Never put the token in a URL.
- **Network:** API calls go only to `https://api.unusualwhales.com`. The "Available Skills" section links to optional extra skill files on `https://unusualwhales.com/skills/`.
- **MCP alternative:** the official Unusual Whales MCP server covers the same data. Hosted: `https://api.unusualwhales.com/api/mcp` with the same Bearer token. Local: `npx -y @unusualwhales/mcp` with `UW_API_KEY` set. Setup guide: https://unusualwhales.com/public-api/mcp
- **Source of truth:** the canonical copy of this skill lives at https://unusualwhales.com/skill.md

## When to use

Use this skill when the user asks for financial data related to:

- Unusual options activity, individual option trades, "whale" trades, flow alerts, or "hottest chains".
- Dark pool prints, trades, or levels.
- Market sentiment (Market Tide, Net Premium, Put/Call ratios).
- Insider trading, politician trading, or specific stock/option details (Greeks, IV).
- Company financial statements such as income statements, balance sheets, cash flows, earnings, or full financials.
- Stock technical indicators such as RSI, MACD, BBANDS, STOCH, VWAP, moving averages, and related indicator series.

## Instructions

You are an expert at querying the Unusual Whales API. Your primary goal is to **avoid widely common hallucinations** regarding this specific API.

### 1. Critical Rules (The "Anti-Hallucination" Protocol)

- **Base URL:** Always use `https://api.unusualwhales.com`
- **Authentication:** All requests MUST include the header: `Authorization: Bearer <API_TOKEN>`
- **Client Header:** All requests MUST include the header: `UW-CLIENT-API-ID: 100001`
- **Method:** All endpoints are `GET` requests. Never use POST, PUT, or DELETE.
- **Strict Whitelist:** You may **ONLY** use endpoints listed in the "Valid Endpoint Reference" section below. If a URL is not on that list, it does not exist.

### 2. Hallucination Blacklist (NEVER USE THESE)

These endpoints are fake but commonly hallucinated. Check your generated code against this list:

- ❌ `/api/options/flow` (Use `/api/option-trades/flow-alerts`)
- ❌ `/api/flow` or `/api/flow/live`
- ❌ `/api/stock/{ticker}/flow` (Use `/api/stock/{ticker}/flow-recent`)
- ❌ `/api/stock/{ticker}/options` (Use `/api/stock/{ticker}/option-contracts`)
- ❌ `/api/unusual-activity`
- ❌ Any URL containing `/api/v1/` or `/api/v2/`
- ❌ Query params `apiKey=` or `api_key=` (Use `Authorization` header only)

### 3. Concept Mapping

Translate user intent to the correct endpoint:

- "Individual Option Trades" / "Raw Option Tape" / "Live Options Flow" -> `/api/option-trades`
- "Flow Alerts" / "Unusual Activity Alerts" / "Whale Alerts" -> `/api/option-trades/flow-alerts`
- "Options Filter" / "Options Screener" / "Flow Filter" -> `/api/screener/option-contracts`
- "Market Sentiment" -> `/api/market/market-tide`
- "Dark Pool" -> `/api/darkpool/recent` or `/api/darkpool/{ticker}`
- "Contract Greeks" -> `/api/stock/{ticker}/greeks`
- "GEX" / "Gamma Exposure" -> `/api/stock/{ticker}/spot-exposures/strike`
- "Financials" / "Fundamentals" / "Statements" -> `/api/stock/{ticker}/financials`
- "Income Statement" -> `/api/stock/{ticker}/income-statements`
- "Balance Sheet" -> `/api/stock/{ticker}/balance-sheets`
- "Cash Flow" -> `/api/stock/{ticker}/cash-flows`
- "Earnings History" -> `/api/stock/{ticker}/earnings`
- "Technical Indicator" / "RSI" / "MACD" / "Moving Average" -> `/api/stock/{ticker}/technical-indicator/{function}`

## Valid Endpoint Reference

You must choose the endpoint from this list.

### Core Data & Flow

- **Option Trades (Individual Tape Prints):** `/api/option-trades`
  - Returns individual option transactions for the latest trading day
  - _Params:_ `limit`, `ticker_symbol`, `option_contracts[]`, `type`, `newer_than`, `older_than`, `min_premium`, `max_premium`, `min_size`, `max_size`, `min_dte`, `max_dte`, `min_volume`, `max_volume`, `min_open_interest`, `max_open_interest`, `is_otm`, `opening`, `size_greater_oi`, `volume_greater_oi`, `include_agg_trades`, `tags[]`, `excluded_tags[]`, `issue_types[]`, `sectors[]`, `industries[]`, `exchanges[]`, `trade_codes[]`
  - List parameters use repeated bracket notation, for example `tags[]=ask_side&tags[]=bid_side`. `newer_than` and `older_than` accept Unix timestamps in seconds or milliseconds.
- **Flow Alerts (Unusual Activity):** `/api/option-trades/flow-alerts`
  - _Params:_ `limit`, `is_call`, `is_put`, `is_otm`, `min_premium`, `ticker_symbol`, `size_greater_oi`
- **Options Screener (Hottest Chains):** `/api/screener/option-contracts`
  - _Params:_ `limit`, `min_premium`, `type`, `is_otm`, `issue_types[]`, `min_volume_oi_ratio`
- **Recent Ticker Flow:** `/api/stock/{ticker}/flow-recent`
- **Dark Pool (Ticker):** `/api/darkpool/{ticker}`
- **Dark Pool (Market Wide):** `/api/darkpool/recent`
- **Market Tide:** `/api/market/market-tide`
- **Net Premium Ticks:** `/api/stock/{ticker}/net-prem-ticks`

### Options, Greeks & IV

- **Option Contracts List and Details:** `/api/stock/{ticker}/option-contracts`
- **Greeks for Each Strike & Expiry:** `/api/stock/{ticker}/greeks`
- **"Static" Gamma Exposure (GEX) by Strike:** `/api/stock/{ticker}/greek-exposure/strike`
- **Gamma Exposure (GEX) by Strike:** `/api/stock/{ticker}/spot-exposures/strike`
- **Interpolated IV and Percentiles:** `/api/stock/{ticker}/interpolated-iv`
- **Options Volume/PC Ratio:** `/api/stock/{ticker}/options-volume`
- **Hottest Chains (Options Screener):** `/api/screener/option-contracts`

### Other Data

- **Insider Trading:** `/api/insider/transactions`
- **Politician Trades:** `/api/congress/recent-trades`
- **News:** `/api/news/headlines`

### Financial Statements & Technicals

- **Full Financials:** `/api/stock/{ticker}/financials`
- **Income Statements:** `/api/stock/{ticker}/income-statements`
  - _Params:_ `report_type`
- **Balance Sheets:** `/api/stock/{ticker}/balance-sheets`
  - _Params:_ `report_type`
- **Cash Flows:** `/api/stock/{ticker}/cash-flows`
  - _Params:_ `report_type`
- **Earnings History:** `/api/stock/{ticker}/earnings`
  - _Params:_ `report_type`
- **Technical Indicator Series:** `/api/stock/{ticker}/technical-indicator/{function}`
  - _Params:_ `interval`, `time_period`, `series_type`

## Available Skills

- A skill to learn how to check the current api usage and debug rate limit errors: https://unusualwhales.com/skills/uw-api-usage-monitor-skill.md
- A skill when working with institutional data such as 13F files: https://unusualwhales.com/skills/institutional.md
- A skill when working with the websocket: https://unusualwhales.com/skills/websocket.md
- A skill to find opportunities to short earnings volatility with call calendar spreads based on backtested criteria: https://unusualwhales.com/skills/uw-earnings-vol-scan-skill.md
- A skill to build a local data lake of transaction-level options data (the Full Tape) on your machine: https://unusualwhales.com/skills/uw-options-data-lake-skill.md
- A skill to build a positioning dashboard using the MCP: https://unusualwhales.com/skills/uw-dashboard-skill.md

## Examples

### Example 1: Getting Unusual Options Activity (Flow Alerts)

**User:** "Show me the latest unusual option trades for TSLA."
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/option-trades/flow-alerts"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "ticker_symbol": "TSLA",
    "min_premium": 50_000,
    "size_greater_oi": True,  # Opening trades where size > open_interest
    "limit": 10,
    "is_otm": True
}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'ticker', 'type', 'total_premium', 'total_size', etc.
```

### Example 2: Filtering Individual Option Trades

**User:** "Show me ask side OTM option trades with at least 500 volume and $10,000 premium. Aggregate multiple transactions that happened at the same time as one transaction"

```python
import httpx

url = "https://api.unusualwhales.com/api/option-trades"
headers = {
    "Authorization": "Bearer YOUR_TOKEN",
    "UW-CLIENT-API-ID": "100001",
}
params = {
    "is_otm": True,
    "volume_greater_oi": True,
    "is_multi_leg": False,
    "max_open_interest": 5_000,
    "max_dte": 180,
    "excluded_tags[]": ["bid_side"],
    "min_premium": 10_000,
    "limit": 50,
    "min_volume": 500,
    "max_price": 25,
    "issue_types[]": ["Common Stock", "ADR"],
    "min_ask_perc": 0.5,
    # Aggregate multiple transactions that happened at the same time into one transaction
    # so that if the transaction got split up and the individual transactions would not match
    # the minimum $10,000 premium but the aggregated would the aggregated would show up this way.
    #
    # Aggregated transactions are the flow alerts from https://api.unusualwhales.com/api/option-trades/flow-alerts
    # tagged as RepeatedHits
    "include_agg_trades": True,
}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# Individual prints with fields such as 'option_chain_id', 'executed_at', 'price', 'size', and 'premium'.
```

### Example 3: Screening for Unusually Bullish Option Trades

**User:** "Show me unusually bullish option activity for today."

```python
import httpx

url = "https://api.unusualwhales.com/api/screener/option-contracts"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {
    "limit": 150,
    "is_otm": True,
    "issue_types[]": ["Common Stock", "ADR"],
    "max_dte": 183,
    "max_multileg_volume_ratio": 0.1,
    "min_ask_perc": 0.7,
    "min_volume": 500,
    "min_premium": 250_000,
    "type": "Calls",
    "vol_greater_oi": True,
}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'ticker_symbol', 'option_symbol', 'ask_side_volume', 'avg_price', etc.
```

### Example 4: Checking Market Tide (Sentiment)

**User:** "What is the overall market sentiment right now?"
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/market/market-tide"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
params = {"interval_5m": False}
response = httpx.get(url, headers=headers, params=params)
print(response.json().get("data", []))
# List of dicts with details like 'timestamp', 'net_call_premium', 'net_put_premium', etc.
```

### Example 5: Dark Pool Trades

**User:** "Any big dark pool prints on NVDA?"
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/darkpool/NVDA"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = httpx.get(url, headers=headers)
print(response.json().get("data", []))
# List of dicts with details like 'ticker', 'price', 'size', 'executed_at', etc.
```

### Example 6: Gamma Exposure (GEX) by Strike

**User:** "Show me the gamma exposure for RIVN puts near current price."
**Code:**

```python
import httpx

url = "https://api.unusualwhales.com/api/stock/RIVN/spot-exposures/strike"
headers = {"Authorization": "Bearer YOUR_TOKEN"}
response = httpx.get(url, headers=headers)
print(response.json().get("data", []))
# List of dicts with details like 'strike', 'put_gamma_oi', 'put_gamma_bid', 'put_gamma_ask', etc.
```
