# TrendRadar — Detect Trending Products Before They Peak

> Know what's going viral before everyone else — track 小红书, 微博, Reddit, Google Trends. Buy before prices spike.

[![clawhub](https://img.shields.io/badge/clawhub-trendradar-blue)](https://clawhub.ai/skills/trendradar)
[![version](https://img.shields.io/badge/version-1.1.3-green)](https://clawhub.ai/skills/trendradar)
[![license](https://img.shields.io/badge/license-MIT--0-lightgrey)](LICENSE)

## What it does

TrendRadar is an [OpenClaw](https://openclaw.ai) skill that monitors social platforms for rising products and assigns a **trend direction signal**:

| Signal | Meaning | Commercial action |
|---|---|---|
| ↑↑ Surging | >200% growth in 7 days | Buy before price rises with demand |
| ↑ Rising | 50–200% growth in 7 days | Good timing — more deals as competition increases |
| → Stable | High volume, growth slowing | Safe choice, no urgency |
| ↓ Cooling | Declining 3+ days | Wait for price drop, or try alternatives |

It is the **upstream signal** for the entire smart shopping ecosystem — trending items flow into [BuyWise](https://github.com/jiajiaoy/BuyWise) for decision analysis and [CouponClaw](https://github.com/jiajiaoy/CouponClaw) for deal stacking.

## Data sources

| Platform | Region | Signal |
|---|---|---|
| 小红书 (Xiaohongshu) | China | Post volume & engagement velocity |
| 微博热搜 | China | Search trend ranking |
| 什么值得买 | China | Save/comment growth rate |
| 抖音 (Douyin) | China | Viral product videos |
| Reddit | US / Global | Upvotes and post frequency |
| Google Trends | Global | Search volume trajectory |
| Product Hunt | US / Global | New product launches & upvotes |

## Installation

```bash
openclaw install trendradar
```

## Usage

```bash
# Scan a keyword or category for trending items
openclaw run trendradar scan "wireless earbuds" --region all

# Full daily trending briefing across all categories
openclaw run trendradar daily-hot --region all --lang en

# China only, Chinese output
openclaw run trendradar scan --region cn --lang zh

# Schedule daily trending push at 8am
openclaw cron add --schedule "0 0 8 * * *" \
  --cmd "node scripts/daily-hot.js --region all --lang zh" \
  --channel telegram
```

## Ecosystem

Part of the **OpenClaw Smart Consumer** skill suite:

```
TrendRadar (signal source)
    ↓  ↑↑ surging item detected
BuyWise (is it worth buying? price + reviews)
    ↓  confirmed: buy now
CouponClaw (find coupon codes + stack cashback)
```

| Skill | Description |
|---|---|
| **TrendRadar** | Trend detection ← you are here |
| [BuyWise](https://github.com/jiajiaoy/BuyWise) | Buying decision for trending items |
| [CouponClaw](https://github.com/jiajiaoy/CouponClaw) | Coupons + cashback for confirmed buys |
| [NewsToday](https://github.com/jiajiaoy/NewsToday) | News feed including consumer trend signals |

## Keywords

trending products · viral products · what's hot · going viral · TikTok trends · xiaohongshu trending · Reddit hot · Google Trends · Product Hunt · social commerce · product discovery · 爆款 · 热销 · 种草 · 小红书爆款 · 消费趋势 · 热门商品

---

Built for [OpenClaw](https://openclaw.ai) · Published on [clawhub.ai/skills/trendradar](https://clawhub.ai/skills/trendradar)
