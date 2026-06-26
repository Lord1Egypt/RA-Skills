# Rent Estimation Reference Guide

> ⚠️ **IMPORTANT**: This file contains methodology for price estimation. Do NOT use static price tables. Always search for the latest real market data first.

---

## Core Principle: Live Search First

**Never provide estimates based solely on static reference data.**

When a user asks about rent prices:

1. **Always execute a live search first** using `wechat-article-search` or other tools
2. Use static reference data only as a sanity check / cross-reference
3. If live data differs significantly from reference data, trust live data and flag the deviation

---

## Live Search Execution

### Step 1: Search WeChat Articles

Use `wechat-article-search` to find recent rental listings:

```bash
# Format: "城市 区域 小区 租房 租金"
node scripts/search_wechat.js "上海 颛桥 租房 租金" -n 15
node scripts/search_wechat.js "城市 区域 直租 2024" -n 15
node scripts/search_wechat.js "城市 区域 转租 2024" -n 15
```

### Step 2: Cross-Validate with Xiaohongshu

Recommend users search Xiaohongshu for the most recent listings:

| Search Purpose | Keywords |
|---------------|----------|
| Direct landlord listings | `[城市] [区域] 直租` |
| Recent listings | `[城市] [区域] 租房 2025` |
| Specific community | `[小区名] 租房` |
| Sublet listings | `[城市] [区域] 转租` |

### Step 3: Compare and Assess

When live data is found, compare against the estimation factors below:

| Deviation | Assessment |
|-----------|------------|
| Live price ≤ Reference Low - 15% | ⚠️ Verify - may be sublet, older, or shared |
| Live price within Reference Range | ✅ Normal |
| Live price > Reference High + 15% | ⚠️ Premium - check what's included |
| Live price > Reference High + 30% | ❌ Suspicious - verify authenticity |

---

## Price Estimation Factors

Use these factors to estimate when live data is unavailable or insufficient:

### Factor Weight

| Factor | Impact | Description |
|--------|---------|-------------|
| Area/District | ★★★★★ | Core vs suburban 2-3x difference |
| Metro Distance | ★★★★☆ | Direct access > 5min > 10min > further |
| Unit Type | ★★★★☆ | Studio < 1BR < 2BR < 3BR tiered |
| Community Quality | ★★★☆☆ | Post-2015 new > old communities |
| Renovation | ★★★☆☆ | Furnished > basic > bare shell |
| Floor/Orientation | ★★☆☆☆ | Mid-high floor, south-facing premium |

### Quick Estimation Formula

```
Reasonable Rent ≈ Base × Area Factor × Metro Factor × Quality Factor × Renovation Factor
```

### Area Factor (Shanghai Example)

| Area Type | Factor |
|-----------|--------|
| Core (15min to CBD) | 1.5-2.0 |
| Suburban (3 metro stops) | 1.0-1.3 |
| Remote (5+ metro stops) | 0.6-0.9 |

### Metro Distance Factor

| Distance | Factor |
|----------|--------|
| Direct metro access | 1.2-1.3 |
| 5 min walk | 1.1-1.2 |
| 10 min walk | 1.0 |
| 15 min walk | 0.9 |
| 20+ min walk | 0.7-0.8 |

### Community Quality Factor

| Type | Factor |
|------|--------|
| Post-2015, brand developer | 1.2-1.4 |
| 2010-2015 | 1.0-1.1 |
| 2000-2010 | 0.9-1.0 |
| Pre-2000 | 0.7-0.9 |

### Renovation Factor

| Condition | Factor |
|-----------|--------|
| Fully furnished | 1.15-1.25 |
| Standard | 1.0 |
| Basic | 0.85-0.95 |
| Bare shell | 0.6-0.75 |

---

## Normal Deposit Standards

| City | Standard |
|------|----------|
| Shanghai | 1 month deposit + 3 months payment |
| Beijing | Primarily 1+3 |
| Shenzhen | 1+2 to 1+3 |
| **Warning** | 3+1 or higher is unreasonable |

---

## Price Warning Signs

| Sign | Risk Level | Action |
|------|------------|--------|
| >30% below market | ❌ High | Likely scam, verify |
| "Pay annual, no agent fee" | ❌ High | Possible Ponzi scheme |
| No contract offered | ❌ High | Extremely risky |
| >30% above market | ⚠️ Medium | Verify what's included |

---

## Live Search Priority

When user asks for rent estimation or area recommendations:

1. **Execute WeChat search first** - find recent aggregate listings
2. **Recommend Xiaohongshu search** - for individual landlord posts
3. **Provide estimation based on factors** - only if no live data found
4. **Always note data age** - flag if data is >3 months old

### Search Terms by City

| City | Sample Search Terms |
|------|-------------------|
| 上海 | `上海 颛桥 租房 租金` / `上海 松江 租房` |
| 北京 | `北京 昌平 租房` / `北京 通州 租房` |
| 深圳 | `深圳 宝安 租房` / `深圳 龙华 租房` |
| 广州 | `广州 天河 租房` / `广州 番禺 租房` |

---

## Important Notes

1. **Market prices fluctuate** - always search for latest data
2. **Location is everything** - same city, different street = different price
3. **Use ranges, not exact numbers** - market is fluid
4. **Verify before deciding** - live search is the baseline, not the ceiling
