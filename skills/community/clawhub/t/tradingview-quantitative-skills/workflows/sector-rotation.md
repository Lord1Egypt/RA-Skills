---
description: Sector rotation analysis workflow - Identify strong sectors and rotation trends
---

# Sector Rotation Analysis Workflow

Through `tradingview_get_leaderboard`'s performance columnset and various tabs, identify current strong sectors, analyze rotation trends, and discover investment opportunities.

## Execution Steps

### Step 1: Get Metadata

```
tradingview_get_metadata(type='markets')   # Confirm market_code
tradingview_get_metadata(type='tabs', asset_type='stocks')  # View all category tabs
```

### Step 2: Get Sector Performance Rankings (performance columnset)

```
# Gainers - performance data (1W/1M/3M/6M/1Y returns)
tradingview_get_leaderboard(
  asset_type='stocks', tab='best-performing',
  market_code='china', columnset='performance', count=50
)

# Losers
tradingview_get_leaderboard(
  asset_type='stocks', tab='losers',
  market_code='china', columnset='performance', count=50
)

# Active stocks
tradingview_get_leaderboard(
  asset_type='stocks', tab='active',
  market_code='china', columnset='overview', count=50
)

# Unusual volume
tradingview_get_leaderboard(
  asset_type='stocks', tab='unusual-volume',
  market_code='china', columnset='overview', count=50
)
```

### Step 3: Sector Classification Analysis

Classify gainer stocks by industry/sector, calculate:
- Percentage of each sector in gainers
- Average gains of each sector (1W/1M/3M dimensions)
- Sector leader identification

### Step 4: Sector Strength Ranking

Compare multi-period returns of various sectors through performance data:

| Sector | 1W | 1M | 3M | 6M | Trend Judgment |
|--------|----|----|----|----|---------------|
| ... | ... | ... | ... | ... | Acceleration/Deceleration/Reversal |

Judgment logic:
- **Accelerating up**: Short-term > medium-term > long-term returns
- **Decelerating up**: Long-term > medium-term > short-term returns
- **Reversal up**: Short-term positive, long-term negative
- **Reversal down**: Short-term negative, long-term positive

### Step 5: Confirm with News

```
tradingview_get_news(market='stock', market_country='CN', lang='zh-Hans', limit=10)
```

Analyze news for sector associations, confirm if sector strength has fundamental/policy support.

### Step 6: Sector Leader Technical Verification

For 1-2 leader stocks of each strong sector:

```
tradingview_get_ta(symbol, include_indicators=true)
```

Confirm if sector leader technicals support continued sector trend.

### Step 7: Generate Sector Rotation Report

```markdown
# Sector Rotation Analysis Report

## Current Strong Sectors (Ranked by Strength)
| Rank | Sector | 1W Gain | 1M Gain | Trend Stage | Leader Stock |
|------|--------|---------|---------|------------|-------------|

## Weak Sectors
| Rank | Sector | 1W Loss | Trend Stage | Oversold? |
|------|--------|---------|------------|-----------|

## Rotation Trend Judgment
- Current market style: [Value/Growth/Cyclical/Defensive]
- Capital flow: [From XX sector to XX sector]
- Rotation stage: [Early/Middle/Late]

## Investment Recommendations
- Recommended sectors: ...
- Avoid sectors: ...
- Leader stock recommendations: ...
```

## ETF/Index Sector Analysis

Can also use index and ETF data for sector analysis:

```
# Industry index comparison
tradingview_get_leaderboard(asset_type='indices', tab='all', columnset='performance')

# ETF sector comparison
tradingview_get_leaderboard(asset_type='etfs', tab='sector-etfs', columnset='performance')
tradingview_get_leaderboard(asset_type='etfs', tab='highest-returns', columnset='performance')
```
