---
description: Financial News Briefing Workflow - Get and summarize financial news
---

# Financial News Briefing Workflow

Get financial news for specified countries/regions, analyze impact, and generate structured briefings.

## Execution Steps

### Step 1: Determine Target Market

Common market_country and lang combinations:

| Market | market_country | lang |
|--------|---------------|------|
| China | CN | zh-Hans |
| United States | US | en |
| Japan | JP | ja |
| Hong Kong | HK | zh-Hans or en |
| South Korea | KR | ko |

### Step 2: Get News List

```
tradingview_get_news(
  market_country='CN', lang='zh-Hans', limit=10,
  market='stock'  # Optional filter: stock/crypto/forex/futures/bond/etf/index/economic
)
```

Can also get by symbol:
```
tradingview_get_news(symbol='NASDAQ:AAPL', lang='en', limit=10)
```

### Step 3: Get News Details

Get full content for each news item:

```
tradingview_get_news_detail(news_id='tag:reuters.com,2026:newsml_xxx', lang='zh-Hans')
```

Returns: title, description, full content, related symbols, tags, storyPath.

News link format: `https://www.tradingview.com{storyPath}`

### Step 4: Analysis and Summary

Extract from each news item:
- Event subject (company/industry/policy)
- Impact scope and duration
- Beneficiary/affected symbols
- Investment recommendations

### Step 5: Generate Briefing

```markdown
# [Country/Region] Financial News Briefing - YYYY-MM-DD

## Today's Headlines

### 1. [News Title]
- Event: [Brief description]
- Impact: [Market impact analysis]
- Related symbols: [Stock codes]
- Source: https://www.tradingview.com{storyPath}

## Sector Updates
| Sector | Main News | Affected Symbols | Trend |
|--------|-----------|------------------|-------|

## Investment Opportunities and Risks
- Opportunities: ...
- Risks: ...
```

## Examples

**User**: "Generate today's China financial news briefing"

**Execution**:
1. `get_news(market_country='CN', lang='zh-Hans', limit=10)` → News list
2. For each `get_news_detail(news_id, lang='zh-Hans')` → Full content
3. Analyze impact, categorize by sector
4. Generate structured briefing

**User**: "Compare financial news from China, US, and Japan"

**Execution**:
1. `get_news` separately for CN/US/JP news
2. Get details separately
3. Cross-market comparative analysis
4. Generate comparison briefing
