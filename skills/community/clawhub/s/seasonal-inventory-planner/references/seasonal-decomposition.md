# Seasonal Decomposition Guide

## Overview

Seasonal decomposition separates a product's sales history into three components: trend, seasonality, and residual. This separation is essential because each component drives different inventory decisions — trend drives year-over-year buy quantities, seasonality drives when to stock, and residuals drive how much safety stock to carry.

## Step 1: Choose the Decomposition Model

### Multiplicative (Recommended for Most E-commerce)
Use when seasonal swings are proportional to the trend level. If a product sells 100 units in January and 200 in June at baseline, and after 50% growth it sells 150 in January and 300 in June, the seasonal effect is multiplicative.

**Formula**: Demand = Trend × Seasonal Index × Residual

### Additive
Use when seasonal swings are constant regardless of trend level. If a product always sells 100 more units in June than January regardless of the baseline, the effect is additive.

**Formula**: Demand = Trend + Seasonal Component + Residual

**Rule of thumb**: If your seasonal peak-to-trough ratio stays roughly constant as the business grows, use multiplicative. If the absolute difference stays constant, use additive. When in doubt, use multiplicative.

## Step 2: Calculate the Base Trend

### Method: Centered Moving Average
1. Calculate a 12-month (or 52-week) centered moving average of demand to smooth out seasonality
2. Fit a line (linear) or curve (exponential) through the smoothed series
3. The slope of this line is your base trend growth rate

### Adjustments
- **Stockout periods**: Replace zero-demand periods during known stockouts with estimated demand (use the same period from a prior year, adjusted for trend)
- **Promotional spikes**: Flag promotional periods but include them in the trend calculation — promotions are part of your demand pattern
- **New products**: Products with less than 12 months of history cannot have trend reliably separated from seasonality. Use category-level seasonal indices instead.

### Output
- Annual growth rate (e.g., +15% YoY)
- Monthly or weekly trend values for the forecast horizon

## Step 3: Calculate Seasonal Indices

### Method: Ratio-to-Moving-Average
1. For each period, divide actual demand by the centered moving average for that period
2. This gives a raw seasonal ratio for each period in each year
3. Average the ratios across all available years for each period (e.g., average all January ratios)
4. Normalize so the indices average to 1.0 across the full cycle

### Interpretation
- Index = 1.0: Average demand period
- Index = 1.5: 50% above average (peak)
- Index = 0.5: 50% below average (trough)
- Index = 2.0+: Strong peak — requires aggressive pre-stocking

### Confidence in Indices
- **2+ years of data**: High confidence — indices are stable and reliable
- **1 year of data**: Medium confidence — indices may reflect one-time events rather than true seasonality
- **<1 year of data**: Low confidence — use category-level or industry benchmarks instead

### Seasonal Profile Classification

| Profile | Description | Index Range (Peak) | Example |
|---|---|---|---|
| Sharp Peak | >70% of demand in <3 months | 3.0–5.0+ | Holiday gifts, Halloween costumes |
| Broad Season | Clear season spanning 4–6 months | 1.5–2.5 | Outdoor furniture, sunscreen |
| Dual Peak | Two distinct peaks per year | 1.5–2.0 each | Chocolate (Valentine's + Christmas) |
| Mild Seasonal | Slight seasonal variation | 1.1–1.4 | Vitamins, cleaning supplies |
| Counter-Seasonal | Peak in typical off-season | Varies | Tax software (Q1), heaters (winter) |

## Step 4: Calculate Residuals and Demand Variability

### Method
1. Subtract (additive) or divide out (multiplicative) the trend and seasonal components from actual demand
2. What remains is the residual — unexplained variation
3. Calculate the standard deviation of residuals for each period or season

### Use in Safety Stock Sizing
- **High residual periods**: Need more safety stock (demand is less predictable)
- **Low residual periods**: Need less safety stock (demand is more predictable)
- **Peak + high residual**: Most dangerous combination — maximize safety stock
- **Trough + low residual**: Minimize safety stock to reduce carrying cost

### Safety Stock Formula
**Safety stock = Z × σ_demand × √(Lead time in periods)**

Where:
- Z = service level factor (1.28 for 90%, 1.65 for 95%, 2.33 for 99%)
- σ_demand = standard deviation of demand in that period
- Lead time = replenishment lead time expressed in demand periods

### Period-Specific Safety Stock Table

| Service Level | Z-Score | Use When |
|---|---|---|
| 99% | 2.33 | Peak season, high-margin products, brand-critical items |
| 95% | 1.65 | Most products during peak and transition |
| 90% | 1.28 | Trough season, low-margin products |
| 85% | 1.04 | End-of-life products, deep trough periods |

## Step 5: Generate the Forward Forecast

### Period-by-Period Calculation
**Forecast_t = Trend_t × Seasonal_Index_t**

### Confidence Intervals
- **Lower bound**: Forecast_t - (Z × σ_residual_t)
- **Upper bound**: Forecast_t + (Z × σ_residual_t)
- Use 80% confidence interval (Z = 1.28) for planning range
- Intervals widen for periods further in the future

### Known Adjustments
Apply these after the statistical forecast:
- **Planned promotions**: Add expected promotional uplift based on historical promotion response
- **Product launches/exits**: Adjust for cannibalization or complementary demand
- **Channel changes**: Scale for new marketplace listings or channel exits
- **Price changes**: Apply historical price elasticity estimates
- **Market shifts**: Industry-level trend changes not captured in your data

## Common Decomposition Pitfalls

1. **Insufficient data**: Seasonal indices from a single year may reflect anomalies rather than patterns. Always flag indices based on <2 years of data.

2. **Stockout contamination**: Zero-demand periods from stockouts look like troughs. Always cross-reference zero-demand with inventory data before calculating indices.

3. **Over-fitting to promotions**: A product that only spikes during Prime Day isn't seasonal — it's promotion-dependent. Distinguish true seasonality (driven by external factors like weather or holidays) from promotion-driven demand.

4. **Ignoring trend when projecting**: Applying last year’s seasonal indices to this year's demand without adjusting for trend either over-orders (if declining) or under-orders (if growing).

5. **Annual cycle assumption**: Some products have sub-annual cycles (weekly patterns for grocery, quarterly for B2B). Match the decomposition cycle to the actual demand pattern.
