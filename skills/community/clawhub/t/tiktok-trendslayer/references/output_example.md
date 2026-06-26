# Output Format Examples

## Script Output (auto-generated)

### Influencer Data — JSON Format

```json
{
  "report_meta": {
    "category": "beauty",
    "region": "US",
    "generated_at": "2026-03-24T08:00:00Z",
    "result_count": 10,
    "api": "echotik_influencer_list"
  },
  "influencers": [
    {
      "nick_name": "example_user",
      "total_followers_cnt": 28000,
      "interaction_rate": 0.082,
      "ec_score": 5.47,
      "sales": 320,
      "avg_30d_price": 22.50,
      "category": "[]",
      "avg_view_cnt": 125000
    }
  ]
}
```

### Influencer Data — Markdown Format

```markdown
# EchoTik Influencer Report

**Category:** beauty | **Region:** US | **Generated:** 2026-03-24T08:00:00Z

## High-Engagement Influencers (engagement > 5%)

| Nickname | Followers | Engagement | EC Score | Sales | Avg Price |
|----------|----------|------------|----------|-------|-----------|
| example_user | 28000 | 8.2% | 5.47 | 320 | 22.5 |

## Full Data (10 results)
(json block)
```

### Product Data — JSON Format

```json
{
  "report_meta": {
    "category": "3c",
    "region": "US",
    "generated_at": "2026-03-24T08:00:00Z",
    "result_count": 20,
    "api": "tiktokshop_product_search"
  },
  "products": [
    {
      "product_id": "123456",
      "title": "Fast Charging Power Bank 20000mAh",
      "category_id": 10002,
      "sales_volume": 25800,
      "gmv": 258000,
      "price": 30.0,
      "gmv_growth": "+67%",
      "image_url": "https://..."
    }
  ]
}
```

### Product Data — Markdown Format

```markdown
# TikTok Shop Product Report

**Category:** 3c | **Region:** US | **Generated:** 2026-03-24T08:00:00Z

## Trending Products

| Product | Price | Sales Volume | GMV Growth | Image |
|---------|-------|--------------|------------|-------|
| Fast Charging Power Bank 20000mAh | 30 | 25800 | +67% | https://... |

## Full Data (20 results)
(json block)
```

### No TikTok Shop API Key

When `TIKTOK_SHOP_API_KEY` is not set:

```markdown
# TikTok Shop Product Report

**Category:** 3c | **Region:** US | **Generated:** 2026-03-24T08:00:00Z

## Note

Product data unavailable because TIKTOK_SHOP_API_KEY environment variable is not set.
To enable product fetching:
1. Log in to https://seller.tiktokglobalshop.com/
2. Create an app in Developer Center
3. Export: export TIKTOK_SHOP_API_KEY="your_app_key"
```

## File Naming Convention

```
<category>_<region>_<YYYYMMDD>_<type>.<format>

Examples:
  beauty_US_20260324_influencers.json
  beauty_US_20260324_products.md
  3c_SG_20260324_influencers.json
```

---

## Advanced Workflow Outputs (AI-generated)

### Regional Analysis Report (MD)

```markdown
# Regional Analysis: 3C Electronics — US, SG, TH

## Executive Summary
- US market has the largest influencer pool but lower avg engagement
- SG shows highest EC scores, indicating strong commercial readiness
- TH has emerging creators with high growth potential

## US — 3C Electronics
(table of top influencers + insights)

## SG — 3C Electronics
(table + insights)

## TH — 3C Electronics
(table + insights)

## Cross-Regional Comparison
(table: engagement, EC score, sales by region)

## Recommendations
(bullet list)
```

### Collaboration Plan (MD)

```markdown
# TikTok Influencer Collaboration Plan

## Project Overview
- Category: 3C Electronics
- Markets: US, SG
- Timeline: April 2026

## Tier 1 — Priority
| Influencer | Region | Followers | Engagement | EC Score | Products | Collab Type | Expected Sales | Rate |
|---|---|---|---|---|---|---|---|---|
| ... | ... | ... | ... | ... | ... | ... | ... | ... |

## Tier 2 — Key
(same table)

## Execution Timeline
| Phase | Week | Tasks | Status |
|---|---|---|---|
| Outreach | 1 | Contact influencers | Pending |
...
```

### Product Selection List (Excel structure)

| Sheet | Content |
|-------|---------|
| Product List | Product, Specs, Price, Market, Conversion, Priority |
| Pricing Strategy | Price Band, Product Types, Conversion, Margin |
| Revenue Forecast | Product, Unit Price, Cost, Profit, Monthly Target |

### Video Hook Scripts (MD)

```markdown
# Script 1: Drop Test — Phone Case

## Meta
- Product: Military-grade shockproof case
- Hook Type: Drop Test
- Duration: 45s
- Conversion Target: 12-18%

## Storyboard
| Time | Scene | Voiceover | SFX |
|---|---|---|---|
| 0-3s | Show phone + case | "Can this case save your phone?" | Tense music |
| 3-8s | Show case details | "TPU + PC military grade" | Tap sound |
...
```

## File Naming

```
<type>_<category>[_<region>]_<YYYYMMDD>.<ext>

selection_list_3c_20260324.md
collab_plan_3c_US_20260324.pdf
regional_analysis_3c_20260324.xlsx
video_hooks_beauty_20260324.md
```
