---
name: tiktok-trend-slayer
description: "TikTok Shop influencer analytics, product selection, and content strategy toolkit. Fetches creator data via EchoTik API, optionally fetches product trending data via TikTok Shop Partner API, then generates multi-region analysis reports, influencer collaboration plans, prioritized product selection lists, and video hook strategies."
metadata:
  openclaw:
    requires:
      env:
        - ECHOTIK_AUTH_HEADER
        - TIKTOK_SHOP_API_KEY
      bins:
        - curl
        - jq
      primaryEnv: ECHOTIK_AUTH_HEADER
    config:
      requiredEnv:
        - ECHOTIK_AUTH_HEADER
      requiredEnv:
        - TIKTOK_SHOP_API_KEY
      stateDirs:
        - .openclaw/skills/tiktok-trend-slayer/output
    homepage: "https://github.com/skovely/tiktok-trendslayer"
    source: "https://github.com/skovely/tiktok-trendslayer"
---

# TikTok Trend Slayer

TikTok Shop analytics toolkit: fetch influencer data via EchoTik API, optionally fetch product trending data via TikTok Shop Partner API, analyze cross-region trends, build collaboration plans, create product selection lists, and plan video hook strategies.

TikTok 选品猎手是一款面向 TikTok 电商卖家的智能选品工具。通过自动监控 TikTok Shop 商品榜、EchoTik 数据接口，实时识别高增长爆款商品，并利用 AI 分析爆款视频的钩子（Hook）与结构，自动匹配合适的中腰部达人（KOC），帮助卖家快速发现蓝海品类与合作机会。在 TikTok 电商领域，领先 48 小时发现爆款意味着 10 倍的利润空间。传统的选品工具只告诉你“什么火了”，而 TikTok Trend Slayer 告诉你“什么即将火”以及“为什么火”。将原本需要 3 小时的手动刷榜和分析，缩短为 1 分钟的“选品简报”。

## 核心功能概述 （Core Features Overview）

1. **黑马发现算法｜Dark Horse Discovery Algorithm**
- 调用 TikTok Affiliate API 和 EchoTik 接口获取商品/达人数据，实时监测 GMV 增长斜率。当某个商品在 24 小时内销量增速翻倍，且挂车达人数仍处于低位时，系统将自动触发“蓝海预警”。

- Leverages TikTok Affiliate and EchoTik APIs to fetch real-time product and creator data, monitoring GMV growth gradients. When a product's sales growth doubles within 24 hours while the number of linked creators remains low, the system automatically triggers a "Blue Ocean Alert."

2. **视频病毒基因拆解 ｜Viral Video Gene Dissection**
- 识别 GMV 增速前 5% 商品及 24h 销量翻倍的黑马 SKU，AI 自动解析高转化视频的“黄金 3 秒”Hook、脚本结构与 BGM 情绪，为您提供 1:1 可复刻的爆款脚本公式。

- Identifies the top 5% of products by GMV growth and "dark horse" SKUs with doubled sales. AI automatically analyzes the "Golden 3-Second" hooks, script structures, and BGM vibes of high-conversion videos, providing you with 1:1 replicable viral script formulas.

3. **达人撮合雷达 | Creator Matchmaking Radar**
- 基于商品画像自动筛选最具带货潜力的高转化 KOC，拒绝只看粉丝数，只看实战转化率，自动制定达人合作方案。

- Automatically filters KOCs with the highest sales potential based on product profiling. Moving beyond vanity metrics like follower counts, it focuses solely on actual conversion rates to generate automated creator collaboration plans.

4. **自动选品报告 | Automated Product Selection Report**
- 支持自动生成目标品类/商品、当前销量、预估利润、竞争程度及推荐话术等的完整报告。

- Supports the automatic generation of comprehensive reports covering target categories/products, current sales volume, estimated profit margins, competition levels, and recommended sales pitches.


## Quick Start

```bash
# Install dependencies
brew install curl jq

# Set EchoTik credential (required)
export ECHOTIK_AUTH_HEADER="Basic <base64_credentials>"

# Optional TikTok Shop credential (if you want product data)
export TIKTOK_SHOP_API_KEY="your_app_key"

# Fetch influencer data
~/.openclaw/skills/tiktok-trend-slayer/scripts/tiktok_slayer.sh --category 3c --region US

# Fetch product trending data
~/.openclaw/skills/tiktok-trend-slayer/scripts/tiktok_slayer.sh --category 3c --region US --mode products

# Fetch both influencers and products
~/.openclaw/skills/tiktok-trend-slayer/scripts/tiktok_slayer.sh --category 3c --region US,SG,TH --format md --mode both

# All categories across all regions
~/.openclaw/skills/tiktok-trend-slayer/scripts/tiktok_slayer.sh --all --region US,SG,TH --format json --mode influencers
```

## Script Arguments

| Flag | Value | Default | Description |
|------|-------|---------|-------------|
| `--category` | beauty/3c/home/fashion/food/sports/baby/pet | — | Single category |
| `--all` | — | — | All 8 categories |
| `--region` | US,SG,TH,UK,... (comma-separated) | US | One or more markets |
| `--format` | json / md | json | Output format |
| `--page-size` | 1-10 | 10 | Results per request |
| `--output-dir` | path | skill/output/ | Custom output directory |
| `--mode` | influencers/products/both | influencers | Data type to fetch |

## What It Does

1. **Influencer data (default)** — Fetches creator/influencer data via EchoTik API (`--mode influencers`).
2. **Product data (optional)** — Fetches trending product data via TikTok Shop Partner API (`--mode products`).
3. **Both data types** — Fetch both influencers and products (`--mode both`).

Without `TIKTOK_SHOP_API_KEY`, product fetching gracefully skips and reports how to enable.

## Advanced Workflows

After fetching data, use these workflows to generate professional deliverables. Read [references/workflows.md](references/workflows.md) for detailed step-by-step instructions.

### 1. Multi-Region Category Analysis

Compare influencer landscapes across markets to find the best opportunities.

**Trigger:** "compare US vs SG", "analyze Southeast Asia", "which market for 3C"

**Process:** Fetch data for multiple regions, cross-compare engagement/EC scores/sales, generate comparison report.

**Output:** Regional comparison report with per-market insights and recommendations.

### 2. Influencer Collaboration Plan

Build a tiered influencer partnership proposal with pricing and timeline.

**Trigger:** "create collab plan", "how to work with influencers", "partnership proposal"

**Process:** Score influencers (engagement 30%, EC score 25%, followers 20%, sales 15%, fit 10%), assign tiers, generate plan with compensation framework and 5-phase execution timeline.

**Output:** Structured proposal with Tier 1/2/3 influencers, collaboration models, rates, timeline, KPIs.

### 3. Product Selection List

Generate a prioritized product list with pricing strategy and revenue forecast.

**Trigger:** "what to sell", "product recommendations", "selection list"

**Process:** Analyze market data (price ranges, conversion patterns), build product list by sub-category, add pricing strategy and revenue forecast.

**Output:** Categorized product list with specs, pricing bands, profit margins, revenue projections.

### 4. Video Hook Strategy

Create video scripts and content calendar matched to products and influencers.

**Trigger:** "create video scripts", "what hooks to use", "content calendar"

**Process:** Match hook types to products (Drop Test, Comparison, Unboxing, Scene, Price Impact), write scene-by-scene scripts, build weekly content calendar with influencer assignments.

**Output:** 3-5 video scripts with storyboard + content calendar.

## Output Formats

| Format | Best For | Generation |
|--------|----------|------------|
| **MD** | Default — readable, editable | Write directly |
| **JSON** | Machine processing, APIs | Script `--format json` |
| **PDF** | Professional reports, sharing | Python reportlab (use English content) |
| **Excel** | Data tracking, calculations | Python openpyxl (use Calibri font) |

See [references/output_example.md](references/output_example.md) for format templates.

## Category Reference

| Category | Code |
|----------|------|
| Beauty | beauty |
| 3C Electronics | 3c |
| Home & Living | home |
| Fashion | fashion |
| Food & Beverage | food |
| Sports & Outdoors | sports |
| Baby & Maternity | baby |
| Pet Supplies | pet |

## API Details

See [references/api_docs.md](references/api_docs.md) for EchoTik and TikTok Shop API endpoints, response schemas, and credential setup.

## Tags

tiktok tiktok-shop product-selection influencer-analytics echotik video-hook content-strategy cross-border ecommerce collaboration-plan
