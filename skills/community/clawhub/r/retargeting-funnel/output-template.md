# Retargeting Funnel — Output Template

Use this template to document a complete retargeting funnel plan. Fill in each section based on the workflow steps in the main skill file.

---

## 1. Business Context

**Brand/Store Name:** [Name]
**Industry/Vertical:** [e.g., DTC Skincare, Fashion Retail, Home Goods]
**Monthly Site Traffic:** [Unique visitors per month]
**Average Order Value (AOV):** $[Amount]
**Current Monthly Ad Spend:** $[Total] | Retargeting portion: $[Amount] ([X]%)
**Ecommerce Platform:** [Shopify / WooCommerce / Magento / Custom]
**Current Retargeting ROAS:** [X.Xx] (if existing campaigns are running)

---

## 2. Pixel and Event Health Report

### Meta Pixel

| Event | Status | 7-Day Fire Count | Parameters Verified | Notes |
|---|---|---|---|---|
| PageView | Active / Inactive | [count] | Yes / No | |
| ViewContent | Active / Inactive | [count] | product_id, value, currency | |
| AddToCart | Active / Inactive | [count] | product_id, value, currency | |
| InitiateCheckout | Active / Inactive | [count] | value, currency, num_items | |
| Purchase | Active / Inactive | [count] | value, currency, order_id | |

**CAPI Status:** Active / Not configured
**CAPI Event Match Quality:** [Score if available]

### Google Ads Tag

| Event | Status | 7-Day Fire Count | Parameters Verified | Notes |
|---|---|---|---|---|
| page_view | Active / Inactive | [count] | Yes / No | |
| view_item | Active / Inactive | [count] | item_id, value, currency | |
| add_to_cart | Active / Inactive | [count] | item_id, value, currency | |
| begin_checkout | Active / Inactive | [count] | value, currency, items | |
| purchase | Active / Inactive | [count] | transaction_id, value | |

**Enhanced Conversions:** Active / Not configured

### TikTok Pixel

| Event | Status | 7-Day Fire Count | Parameters Verified | Notes |
|---|---|---|---|---|
| PageView | Active / Inactive | [count] | Yes / No | |
| ViewContent | Active / Inactive | [count] | content_id, value, currency | |
| AddToCart | Active / Inactive | [count] | content_id, value, currency | |
| InitiateCheckout | Active / Inactive | [count] | value, currency | |
| CompletePayment | Active / Inactive | [count] | value, currency, order_id | |

**Issues to Resolve:**
- [ ] [Describe any pixel issues, missing events, parameter gaps]
- [ ] [Developer tasks required]

---

## 3. Audience Segmentation Plan

| Segment ID | Segment Name | Definition | Lookback Window | Estimated Size | Exclusions |
|---|---|---|---|---|---|
| S1 | Homepage Bouncers | [Definition] | [X] days | [Size] | Excludes S2-S6 |
| S2 | Category Browsers | [Definition] | [X] days | [Size] | Excludes S3-S6 |
| S3 | Product Viewers | [Definition] | [X] days | [Size] | Excludes S4-S6 |
| S4 | Cart Abandoners | [Definition] | [X] days | [Size] | Excludes S5-S6 |
| S5 | Checkout Abandoners | [Definition] | [X] days | [Size] | Excludes S6 |
| S6 | Recent Purchasers | [Definition] | [X] days | [Size] | — |

**Sub-segments (if applicable):**
- [e.g., S3a: Single Product Viewers / S3b: Multi-Product Viewers]
- [e.g., S4 split by cart value threshold]

---

## 4. Creative Strategy by Segment

### S1 — Homepage Bouncers
- **Format:** [Video / Carousel / Static]
- **Message Angle:** [Description]
- **CTA:** [CTA text]
- **Creative Assets Needed:** [List]

### S2 — Category Browsers
- **Format:** [Video / Carousel / Static]
- **Message Angle:** [Description]
- **CTA:** [CTA text]
- **Creative Assets Needed:** [List]

### S3 — Product Viewers
- **Format:** [DPA / Carousel / Static]
- **Message Angle:** [Description]
- **CTA:** [CTA text]
- **Creative Assets Needed:** [List]

### S4 — Cart Abandoners
- **Format:** [DPA / Single Image / Carousel]
- **Message Angle:** [Description]
- **CTA:** [CTA text]
- **Incentive (if any):** [e.g., free shipping, discount code]
- **Creative Assets Needed:** [List]

### S5 — Checkout Abandoners
- **Format:** [DPA / Single Image]
- **Message Angle:** [Description]
- **CTA:** [CTA text]
- **Incentive (if any):** [e.g., discount code, price guarantee]
- **Creative Assets Needed:** [List]

---

## 5. Platform Campaign Structure

### Meta Ads

| Campaign | Objective | Segments | Bid Strategy | Budget | Placements |
|---|---|---|---|---|---|
| [Name] | [Objective] | [S1-S2] | [Strategy] | $[Daily] | [Placements] |
| [Name] | [Objective] | [S3] | [Strategy] | $[Daily] | [Placements] |
| [Name] | [Objective] | [S4-S5] | [Strategy] | $[Daily] | [Placements] |

### Google Ads

| Campaign | Type | Segments | Bid Strategy | Budget | Networks |
|---|---|---|---|---|---|
| [Name] | [PMax/Display/YouTube] | [Segments] | [Strategy] | $[Daily] | [Networks] |

### TikTok Ads

| Campaign | Objective | Segments | Bid Strategy | Budget | Format |
|---|---|---|---|---|---|
| [Name] | [Objective] | [Segments] | [Strategy] | $[Daily] | [Format] |

---

## 6. Frequency Caps and Budget Allocation

### Frequency Caps

| Segment | Daily Cap | Weekly Cap |
|---|---|---|
| S1 | [X] | [X] |
| S2 | [X] | [X] |
| S3 | [X] | [X] |
| S4 | [X] | [X] |
| S5 | [X] | [X] |

### Budget Allocation

| Segment | % of Retargeting Budget | Monthly Spend | Expected ROAS |
|---|---|---|---|
| S1 | [X]% | $[Amount] | [X.Xx] |
| S2 | [X]% | $[Amount] | [X.Xx] |
| S3 | [X]% | $[Amount] | [X.Xx] |
| S4 | [X]% | $[Amount] | [X.Xx] |
| S5 | [X]% | $[Amount] | [X.Xx] |
| **Total** | **100%** | **$[Amount]** | **[X.Xx]** |

---

## 7. Measurement Framework

### KPIs by Segment

| Segment | Primary KPI | Target | Secondary KPI | Target |
|---|---|---|---|---|
| S1 | [Metric] | [Value] | [Metric] | [Value] |
| S2 | [Metric] | [Value] | [Metric] | [Value] |
| S3 | [Metric] | [Value] | [Metric] | [Value] |
| S4 | [Metric] | [Value] | [Metric] | [Value] |
| S5 | [Metric] | [Value] | [Metric] | [Value] |

### Incrementality Test Plan
- **Holdout percentage:** [X]%
- **Test duration:** [X] weeks
- **Segments tested:** [List]
- **Success criteria:** Incremental lift > [X]%

---

## 8. Optimization Schedule

| Cadence | Action |
|---|---|
| Daily | Monitor delivery pacing, check for ad disapprovals, review spend vs. budget |
| Weekly | Review segment performance vs. KPIs, adjust bids, check frequency vs. CTR |
| Bi-weekly | Creative rotation review, A/B test results analysis |
| Monthly | Budget reallocation across segments, incrementality test review |
| Quarterly | Full funnel audit, lookback window adjustments, new segment exploration |

---

## 9. Open Items and Next Steps

- [ ] [Action item 1 — owner — due date]
- [ ] [Action item 2 — owner — due date]
- [ ] [Action item 3 — owner — due date]
