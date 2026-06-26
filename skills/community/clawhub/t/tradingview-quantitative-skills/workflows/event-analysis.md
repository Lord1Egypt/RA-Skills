---
description: Event-Driven Analysis Workflow - Track major events and analyze market impact
---

# Event-Driven Analysis Workflow

Track major events, analyze market impact, identify beneficiary stocks, and provide investment recommendations.

## Execution Steps

### Step 1: Get Financial Calendar

Call calendar based on event type (time span not exceeding 40 days):

```
# Earnings calendar
tradingview_get_calendar(type='earnings', from=now, to=now+14days, market='china')

# Dividend calendar
tradingview_get_calendar(type='revenue', from=now, to=now+14days, market='china')

# Economic data calendar
tradingview_get_calendar(type='economic', from=now, to=now+7days, market='america,china')

# IPO calendar
tradingview_get_calendar(type='ipo', from=now, to=now+14days, market='china')
```

### Step 2: Get Related News

```
# Get specific market news
tradingview_get_news(market='stock', market_country='CN', lang='zh-Hans', limit=20)

# Get specific symbol news
tradingview_get_news(symbol='SSE:600519', lang='zh-Hans', limit=10)

# Get economic news
tradingview_get_news(market='economic', lang='zh-Hans', limit=10)
```

Get details for important news:
```
tradingview_get_news_detail(news_id, lang='zh-Hans')
```

### Step 3: Extract Event Keywords

Extract from calendar events and news:
- **Company name/symbol**: Directly related stocks
- **Industry keywords**: Used to search for same-industry beneficiary stocks
- **Policy keywords**: Used to expand impact scope
- **Event type**: Earnings beat/policy positive/industry event/breaking news

### Step 4: Search Beneficiary Stocks

Search related stocks using extracted keywords:

```
tradingview_search_market(query='keyword', filter='stock', limit=20)
```

For industry events, also find same-sector stocks via leaderboard:
```
tradingview_get_leaderboard(
  asset_type='stocks', tab='gainers',
  market_code='china', columnset='overview', count=50
)
```

### Step 5: Analyze Beneficiary Stock Quotes

For identified beneficiary stocks (5-10), get quotes and technical analysis:

```
tradingview_get_quote_batch(symbols=[...])  # Real-time quotes
tradingview_get_ta(symbol, include_indicators=true)  # Technical confirmation
```

### Step 6: Assess Impact Level

Assess each beneficiary stock:

| Factor | Weight | Assessment Dimension |
|--------|--------|---------------------|
| Event Importance | 30% | Fundamental impact on industry/company |
| Relevance | 25% | Direct correlation between stock and event |
| Timeliness | 20% | Duration of event impact |
| Expectation Gap | 15% | Whether market has fully priced in |
| Certainty | 10% | Certainty of event materialization |

Impact levels:
- **Strong Positive (+3)**: Direct beneficiary, clear earnings improvement
- **Positive (+2)**: Indirect beneficiary, industry prosperity improvement
- **Slight Positive (+1)**: Sentiment positive
- **Neutral (0)**: Limited impact
- **Negative (-1/-2/-3)**: Symmetrical negative impact

### Step 7: Generate Analysis Report

```markdown
# Event-Driven Analysis Report

## Event Overview
- Event: [Event description]
- Time: [Occurrence/expected time]
- Type: [Earnings/Policy/Industry/Breaking]
- Importance: [High/Medium/Low]

## Impact Analysis
- Direct impact: ...
- Indirect impact: ...
- Impact duration: [Short-term/Medium-term/Long-term]

## Beneficiary Stock Analysis

### 1. [Stock Name] (Symbol) - Impact Level: +3
- Relevance: Direct beneficiary, [reason]
- Current price: ¥XX (Change XX%)
- Technical: RSI=XX, TA signal=[Buy/Sell]
- Trading recommendation: ...

### 2. [Stock Name] ...

## Risk Factors
- [Risk 1: Event materialization below expectations]
- [Risk 2: Market has fully priced in]

## Trading Recommendations
- Short-term strategy: ...
- Medium-term strategy: ...
```

## Example

**User**: "Analyze the impact of cloud computing price increases on related companies"

**Execution**:
1. `get_news(market='stock', market_country='CN', lang='zh-Hans')` → Related news
2. `get_news_detail(news_id)` → News details
3. `search_market(query='云计算', filter='stock')` → Related stocks
4. `get_leaderboard(tab='gainers', market_code='china')` → Verify gainers list
5. `get_quote_batch` + `get_ta` → Quotes and technical analysis
6. Assess impact level → Generate analysis report
