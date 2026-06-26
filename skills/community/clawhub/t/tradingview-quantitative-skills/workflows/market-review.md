---
description: Market Review Workflow - Daily market analysis and investment opportunity discovery
---

# Market Review Workflow

Daily market review, tracking hot sectors and capital flows, discovering investment opportunities.

## Execution Steps

### Step 1: Get Metadata

```
tradingview_get_metadata(type='markets')  # Confirm market_code
```

### Step 2: Get Gainers/Losers Data

Call in parallel to get multi-dimensional data:

```
# Gainers
tradingview_get_leaderboard(
  asset_type='stocks', tab='gainers',
  market_code='china', columnset='overview', count=50
)

# Losers
tradingview_get_leaderboard(
  asset_type='stocks', tab='losers',
  market_code='china', columnset='overview', count=50
)

# Most active (highest volume)
tradingview_get_leaderboard(
  asset_type='stocks', tab='active',
  market_code='china', columnset='overview', count=30
)

# Unusual volume
tradingview_get_leaderboard(
  asset_type='stocks', tab='unusual-volume',
  market_code='china', columnset='overview', count=30
)
```

### Step 3: Get Market News

```
tradingview_get_news(market='stock', market_country='CN', lang='zh-Hans', limit=10)
```

Get details for important news:
```
tradingview_get_news_detail(news_id, lang='zh-Hans')
```

### Step 4: Get Index Quotes (Optional)

```
tradingview_get_quote_batch(
  symbols=["SSE:000001", "SZSE:399001", "SZSE:399006"]  # Shanghai/Shenzhen/ChiNext
)
```

### Step 5: Identify Hot Sectors

Analyze industry distribution in gainers list:
- Categorize top 50 gainers by industry
- Count number and average gain for each industry
- Identify top 3-5 sectors with highest representation

### Step 6: Analyze Capital Flow

Analyze through volume data:
- Industry distribution of active and unusual volume stocks
- Volume comparison between gainers vs losers
- Stocks with volume surge and price increase (capital inflow signal)

### Step 7: Correlate News with Market Action

Correlate companies/industries in news with gainers/losers:
- News catalysts for limit-up stocks
- Policy/event drivers for sector movements
- Sustainability assessment

### Step 8: Generate Review Report

```markdown
# [Market] Market Review - YYYY-MM-DD

## Market Overview
- Index performance: [Shanghai/Shenzhen/ChiNext changes]
- Advance/decline: XX up / XX down
- Trading volume: XX billion (vs previous +/-XX%)

## Hot Sectors (Ranked by strength)
| Rank | Sector | Gain | Representative Stocks | Catalyst |
|------|--------|------|----------------------|----------|

## Top 10 Gainers
| Rank | Stock | Gain | Volume | Unusual Signal |
|------|-------|------|--------|----------------|

## Capital Flow
- Main inflow sectors: ...
- Main outflow sectors: ...
- Unusual volume stocks: ...

## News Highlights
1. [News title] - [Impact analysis]
2. ...

## Investment Opportunities
- [Opportunity 1]: Reason and recommended stocks
- [Opportunity 2]: ...

## Risk Warnings
- [Risk 1]
- [Risk 2]
```

## Example

**User**: "How was the A-share market today?"

**Execution**:
1. `get_metadata(type='markets')` → china
2. `get_leaderboard` × 4 (gainers/losers/active/unusual-volume)
3. `get_news(market_country='CN', lang='zh-Hans')` + details
4. `get_quote_batch` → Index quotes
5. Sector categorization → Hot sector identification → News correlation
6. Generate review report
