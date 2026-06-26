---
name: Seasonal Inventory Planner
description: Build month-by-month inventory plans that align purchasing, stocking, and markdown timing with seasonal demand curves to prevent both stockouts during peaks and overstock during troughs.
---

# Seasonal Inventory Planner

Build month-by-month inventory plans that align purchasing, stocking, and markdown timing with seasonal demand curves to prevent both stockouts during peaks and overstock during troughs. This skill transforms historical sales patterns into forward-looking inventory calendars with specific reorder dates, quantity targets, and pre-season/post-season action triggers. It accounts for supplier lead times, storage capacity constraints, and cash flow timing to produce plans that are operationally executable — not just theoretically optimal.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Historical data | 2+ years of weekly/monthly sales covering full seasonal cycles | 1 year of data with comparable industry benchmarks | Under 1 year or missing peak season data |
| Demand modeling | Decomposed trend + seasonal + residual with confidence intervals | Year-over-year growth-adjusted seasonal indices | Flat averages or single-year extrapolation |
| Lead time integration | Supplier-specific lead times with variability buffers built into reorder dates | Average lead times applied uniformly | Lead times ignored or assumed instant |
| Inventory targets | Week-level stock targets with safety stock calibrated to demand volatility | Monthly stock targets with fixed safety stock | Single annual target or no safety stock |
| Pre-season planning | Specific buy quantities, dates, and allocation by channel/location | Aggregate buy plan without channel detail | No pre-season plan — reactive purchasing only |
| Post-season strategy | Defined markdown schedule with trigger points and liquidation timeline | General "mark down after season" guidance | No post-season plan — ad hoc discounting |

## Solves

- You are placing pre-season purchase orders and need to know exactly how many units to buy, when to place orders, and how to phase deliveries to avoid warehouse overflow
- Your seasonal products consistently stockout during peak weeks and you need a plan that front-loads inventory while respecting cash flow and storage limits
- You carry too much post-season dead stock and need a structured markdown calendar that starts at the right time with the right depth to clear inventory before the next cycle
- Your purchasing team orders based on gut feel rather than data and you need a quantitative framework that accounts for trend, seasonality, and growth
- You sell across multiple channels or locations with different seasonal curves and need differentiated inventory plans rather than one-size-fits-all ordering
- You want to optimize the balance between stockout risk and carrying cost by setting safety stock levels that reflect actual demand volatility during peak versus off-peak periods
- Your supplier lead times are long (60-120 days) and you need to place orders months before the season starts, requiring accurate forward demand estimates

## Workflow

### Step 1 — Gather and clean historical demand data
Collect at minimum 12 months (ideally 24+) of sales data at the weekly or monthly level for each product or category. Required fields: product/SKU, time period, units sold, and revenue. Optional but valuable: units lost to stockouts (estimated from zero-inventory days), returns by period, and channel/location breakdowns. Clean the data by identifying and adjusting for known anomalies: stockout periods (replace zeros with estimated demand), one-time promotional spikes (flag but don't remove), and data gaps.

### Step 2 — Decompose demand into trend and seasonal components
Separate each product's demand signal into three components: (1) Base trend — the underlying growth or decline trajectory independent of seasonality, calculated as year-over-year change in total demand. (2) Seasonal index — the relative demand multiplier for each period, calculated by dividing each period's actual demand by the trend-adjusted average. A seasonal index of 1.5 means that period sees 50% more demand than average. (3) Residual — unexplained variation used to size safety stock. Products with high residuals need larger safety buffers.

### Step 3 — Project forward demand by period
Multiply the base trend forecast by the seasonal index for each future period to generate a period-by-period demand forecast. Apply any known adjustments: planned promotions, new product launches that will cannibalize or complement, channel expansion or contraction, and market trend shifts. Calculate confidence intervals — the range widens for periods further in the future and for products with higher residual variation.

### Step 4 — Set inventory targets by period
For each period, calculate: (1) Cycle stock — the quantity needed to meet expected demand between replenishments. (2) Safety stock — the buffer against demand uncertainty, sized based on the period's demand variability and your acceptable stockout probability. Safety stock should be higher during peak periods when lost sales are most costly and lower during troughs when carrying cost matters more. (3) Pipeline stock — units in transit based on lead time. Sum these to get the target inventory position for each period.

### Step 5 — Build the reorder calendar
Working backward from each period's target inventory position, calculate when orders must be placed to arrive on time given supplier lead times. For each reorder: specify the order date, quantity, expected arrival date, and the demand period it covers. Phase large pre-season buys across multiple orders where possible to reduce risk and spread cash flow. Flag orders that require commitment before demand signals are available (the "blind buy" problem) and recommend smaller initial orders with replenishment options.

### Step 6 — Design the post-season markdown strategy
For products with defined seasons, plan the transition from full-price to marked-down inventory: (1) Set the markdown trigger — the date or inventory level that initiates discounting. (2) Define the markdown cadence — progressive discounts (e.g., 20% → 40% → 60%) on a defined schedule. (3) Calculate the sell-through target for each markdown stage. (4) Set the final exit deadline — the date by which all seasonal inventory must be cleared, even at deep discount or liquidation.

### Step 7 — Validate against constraints and finalize
Cross-check the plan against operational constraints: warehouse capacity limits (can you physically store the peak inventory position?), cash flow limits (can you fund the pre-season buy?), supplier minimums and maximums (do your orders meet MOQs?), and shelf life constraints (will inventory expire before sell-through?). Adjust the plan to respect constraints, documenting any tradeoffs. Produce the final inventory calendar with week-by-week or month-by-month targets, reorder schedule, and action triggers.

## Example 1: Outdoor Furniture E-commerce (45 SKUs)

**Input data**: 24 months of Shopify sales data across 45 SKUs in patio furniture — chairs, tables, umbrellas, and cushions.

**Seasonal decomposition results**:
- Peak season: April–August (seasonal indices 1.4–2.1)
- Trough season: November–February (seasonal indices 0.2–0.4)
- Base trend: +12% year-over-year growth
- Highest volatility: March and September (transition months)

**Key plan outputs**:
| Action | Timing | Detail |
|---|---|---|
| Pre-season buy #1 | January 15 | 40% of projected peak inventory, covers April–May demand |
| Pre-season buy #2 | March 1 | 35% of peak inventory, adjusted for early-season sell-through signals |
| In-season replenishment | May 15 | 25% reserve order, triggered only if sell-through exceeds 110% of forecast |
| Markdown initiation | August 15 | 20% off remaining seasonal inventory |
| Deep markdown | September 15 | 40% off, target 90% sell-through by October 1 |
| Liquidation | October 1 | Remaining units to clearance channel at 60% off |

**Safety stock calibration**: Peak months (June–July) carry 3 weeks of safety stock due to high demand volatility and high cost of stockouts. Trough months carry 1 week. Transition months carry 2 weeks with weekly review triggers.

**Financial impact**: Plan projects 94% sell-through rate versus prior year's 78%, reducing end-of-season write-downs by $34,000 while maintaining a 97% in-stock rate during peak weeks.

## Example 2: Holiday Gift Retailer (150 SKUs)

**Input data**: 18 months of Amazon and DTC sales data, 150 SKUs across toys, home décor, and gift sets. Extreme seasonality — 65% of annual revenue occurs in November–December.

**Seasonal decomposition results**:
- Peak season: November–December (seasonal indices 3.2–4.8)
- Secondary peak: February (Valentine's), May (Mother's Day) — indices 1.3–1.6
- Base trough: January, March, June–September (indices 0.2–0.5)
- Base trend: +8% year-over-year

**Key plan outputs**:
| Action | Timing | Detail |
|---|---|---|
| Holiday pre-buy commitment | July 1 | 60% of projected Q4 demand, non-cancellable with supplier |
| Holiday pre-buy #2 | September 15 | 25% of Q4 demand, based on early wholesale/pre-order signals |
| Reserve allocation | October 15 | 15% held for in-season replenishment based on sell-through velocity |
| Black Friday stock check | November 15 | Verify 6-week supply on hand for all A-tier SKUs |
| Post-holiday markdown | December 27 | 25% off gift sets, 30% off seasonal décor |
| January clearance | January 10 | 50% off all remaining holiday inventory |
| Liquidation deadline | January 31 | Move remaining units to liquidation channel |

**Blind buy risk mitigation**: For the July commitment (5 months before peak), the plan recommends concentrating 80% of the non-cancellable buy on proven top-50 SKUs with 2+ years of history, and limiting new/unproven SKUs to 20% of the commitment. New SKUs get smaller initial orders with an option for September top-up if early signals are positive.

**Cash flow phasing**: Total pre-season investment of $180,000 phased as $108K (July), $45K (September), $27K (October reserve). Peak inventory carrying cost of $12,000/month in October–November, dropping to near zero by February.

## Common Mistakes

1. **Using annual averages instead of seasonal indices**: Ordering the same quantity every month guarantees both stockouts during peak and overstock during trough. Always decompose demand into seasonal components and plan inventory at the period level, not annually.

2. **Ignoring lead time in reorder calculations**: A 90-day supplier lead time means your April inventory decision was actually made in January. Every reorder date must account for the full procurement cycle — order processing, production, shipping, receiving, and quality check time.

3. **Setting uniform safety stock**: A fixed "2 weeks of safety stock" rule over-stocks during low-demand periods and under-stocks during high-demand periods. Calibrate safety stock to each period's demand variability and the business cost of a stockout in that period.

4. **No post-season markdown plan**: Without a predefined markdown calendar, teams discount reactively and inconsistently — often too late, too shallow, then panic-deep. Set markdown triggers, timing, and depth before the season starts.

5. **Treating all products as equally seasonal**: Within a "seasonal" category, some products have sharp peaks while others sell more steadily. Group products by seasonal profile and plan each group's inventory curve separately.

6. **Forgetting about the "blind buy" problem**: Long lead times force purchase decisions before demand signals are available. Acknowledge this uncertainty explicitly — use smaller initial orders for unproven products, negotiate cancellation or return options, and hold reserve budget for in-season adjustment.

7. **Not accounting for storage capacity**: A plan that calls for 10,000 units in the warehouse when capacity is 6,000 isn't a plan. Validate peak inventory positions against physical storage constraints and adjust delivery phasing accordingly.

8. **Planning in isolation from cash flow**: The optimal inventory plan from a demand perspective may be unaffordable from a cash flow perspective. Always overlay the inventory plan with a cash flow timeline to ensure the business can fund the pre-season build.

## Resources

- [Output template](references/output-template.md) — Structured format for presenting seasonal inventory plans
- [Seasonal decomposition guide](references/seasonal-decomposition.md) — Step-by-step methods for calculating trend, seasonal indices, and safety stock
- [Post-season playbook](references/post-season-playbook.md) — Markdown strategies, liquidation timing, and sell-through optimization
- [Quality checklist](assets/quality-checklist.md) — Pre-delivery validation checklist
