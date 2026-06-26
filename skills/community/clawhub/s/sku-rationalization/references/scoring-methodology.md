# SKU Scoring Methodology Guide

## Overview

The multi-factor scoring system converts raw SKU performance data into a single composite score (0-100) that drives Keep/Fix/Kill classification. This guide details the calculation, normalization, weighting, and threshold calibration process.

## Scoring Dimensions

### 1. Revenue Contribution (Default Weight: 30%)

**What it measures**: The SKU's share of total catalog revenue.

**Calculation**: `SKU Revenue ÷ Total Catalog Revenue × 100`

**Why it matters**: Revenue contribution identifies your catalog's money-makers. However, high revenue alone doesn't mean a SKU is healthy — it could be selling at razor-thin or negative margins.

**Normalization**: Apply min-max normalization across all SKUs. The highest revenue-contributing SKU scores 100, the lowest scores 0.

**Pitfall**: Revenue is heavily skewed by price. A $500 item selling 10 units may outscore a $5 item selling 500 units despite the latter being a stronger performer by volume. Consider using unit contribution as an alternative for low-ASP catalogs.

### 2. Gross Margin % (Default Weight: 25%)

**What it measures**: Profitability per unit after direct costs.

**Calculation**: `(Selling Price − COGS) ÷ Selling Price × 100`

**Why it matters**: Margin health determines whether sales actually generate profit. SKUs with negative margins after platform fees, shipping, and returns are actively destroying value.

**Adjustments**: Where possible, use "true margin" that includes: platform commission, payment processing fees, shipping cost (net of customer payment), return processing cost, and advertising cost per unit.

**Normalization**: Min-max across catalog. Negative margins score 0.

### 3. Inventory Turnover Ratio (Default Weight: 20%)

**What it measures**: How efficiently inventory converts to sales.

**Calculation**: `Annual Units Sold ÷ Average Inventory on Hand`

**Benchmarks by category**:
- Fast fashion / consumables: 8-12x is good
- General apparel: 4-6x is good
- Electronics / gadgets: 6-10x is good
- Home / furniture: 2-4x is good
- Specialty / niche: 2-3x is good

**Why it matters**: Low turnover means capital is trapped in unsold inventory. High turnover means the SKU is efficiently converting investment into revenue.

### 4. Demand Velocity (Default Weight: 15%)

**What it measures**: Whether demand is growing, stable, or declining.

**Calculation**: `Units Sold (Last 90 days) ÷ Units Sold (Prior 90 days)`

**Interpretation**:
- Velocity > 1.2: Growing demand (positive signal)
- Velocity 0.8-1.2: Stable demand (neutral)
- Velocity < 0.8: Declining demand (negative signal)
- Velocity = 0: No recent sales (strong negative signal)

**Why it matters**: A SKU that sold well historically but is trending to zero should be flagged before inventory becomes truly dead stock.

### 5. Return Rate (Default Weight: 10%)

**What it measures**: Product quality and listing accuracy signals.

**Calculation**: `Units Returned ÷ Units Sold × 100`

**Scoring**: Inverse scoring — lower return rates score higher. Return rates above 15% score 0.

**Why it matters**: High return rates signal product issues, sizing problems, or misleading listings. Returns also incur direct costs (shipping, restocking, damage) that erode margin.

## Composite Score Calculation

```
Composite = (Revenue_norm × W_rev) + (Margin_norm × W_mar) + (Turnover_norm × W_turn) + (Velocity_norm × W_vel) + (ReturnInverse_norm × W_ret)
```

Where all weights sum to 1.0 (100%).

## Threshold Calibration

### Default Thresholds
- Keep: 70-100
- Fix: 40-69
- Kill: 0-39

### When to Adjust Thresholds

**Aggressive pruning** (e.g., warehouse at capacity): Lower Kill threshold to 45, Fix to 75. This increases the Kill bucket.

**Conservative approach** (e.g., risk-averse stakeholder): Lower Kill threshold to 30, keep Fix at 40. This reduces false Kill recommendations.

**Category-specific**: Apply different thresholds per category when category dynamics vary significantly (e.g., accessories vs. furniture).

## Weight Customization Guide

| Business Priority | Revenue | Margin | Turnover | Velocity | Returns |
|---|---|---|---|---|---|
| Growth-focused | 35% | 15% | 20% | 20% | 10% |
| Profitability-focused | 20% | 35% | 20% | 15% | 10% |
| Cash-flow focused | 15% | 20% | 35% | 20% | 10% |
| Trend-responsive | 20% | 20% | 15% | 35% | 10% |
| Quality-focused | 20% | 25% | 15% | 15% | 25% |

Always document the weight configuration used and the rationale for any deviation from defaults.
