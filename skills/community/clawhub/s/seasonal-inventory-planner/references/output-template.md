# Seasonal Inventory Plan — Output Template

## Executive Summary

**Planning horizon**: [Start month] — [End month]
**Products covered**: [N] SKUs across [N] categories
**Data source**: [Platform/export name]
**Historical data window**: [N] months ([Start] — [End])

### Season Overview

| Metric | Value |
|---|---|
| Peak season window | [Month] — [Month] |
| Peak seasonal index range | [X.X] — [X.X] |
| Trough season window | [Month] — [Month] |
| Base trend (YoY) | [+/-X%] |
| Total projected seasonal demand (units) | [N] |
| Total pre-season investment required | $[amount] |
| Projected sell-through rate | [%] |
| Projected in-stock rate during peak | [%] |

---

## Seasonal Demand Forecast

| Period | Seasonal Index | Projected Demand (units) | Confidence Range | YoY Change |
|---|---|---|---|---|
| [Month/Week] | [X.XX] | [N] | [Low] — [High] | [+/-X%] |

*Include all periods in the planning horizon. Highlight peak periods and transition periods.*

---

## Inventory Target Schedule

| Period | Projected Demand | Cycle Stock | Safety Stock | Pipeline Stock | Target Inventory Position | Notes |
|---|---|---|---|---|---|---|
| [Month/Week] | [N] | [N] | [N] | [N] | [N] | [Peak/Trough/Transition] |

### Safety Stock Rationale

| Period Type | Safety Stock Level | Weeks of Cover | Rationale |
|---|---|---|---|
| Peak months | [N] units | [N] weeks | High demand volatility, maximum stockout cost |
| Transition months | [N] units | [N] weeks | Moderate uncertainty, demand direction unclear |
| Trough months | [N] units | [N] weeks | Low volatility, carrying cost outweighs stockout risk |

---

## Reorder Calendar

| Order # | Order Date | Supplier | Quantity | Est. Arrival | Demand Period Covered | Cost | Cancellable? |
|---|---|---|---|---|---|---|---|
| 1 | [Date] | [Name] | [N] units | [Date] | [Period] | $[amount] | [Y/N] |

### Cash Flow Timeline

| Month | Order Payments Due | Cumulative Investment | Expected Revenue | Net Cash Position |
|---|---|---|---|---|
| [Month] | $[amount] | $[amount] | $[amount] | $[amount] |

---

## Post-Season Markdown Calendar

| Stage | Trigger Date | Discount Depth | Target Sell-Through | Inventory Threshold | Action |
|---|---|---|---|---|---|
| Full price | Season start — [Date] | 0% | [%] of total | N/A | Normal selling |
| Markdown 1 | [Date] | [X%] off | [%] cumulative | If >[N] units remain | Reduce price, increase visibility |
| Markdown 2 | [Date] | [X%] off | [%] cumulative | If >[N] units remain | Deep discount, clearance section |
| Liquidation | [Date] | [X%] off | 100% | Any remaining | Move to liquidation channel |

---

## Product-Level Plans

For each product or top N products:

### [Product Name] — Seasonal Profile: [Sharp Peak / Broad Season / Dual Peak / Steady]

- **Peak period**: [Month–Month], seasonal index [X.X]
- **Pre-season buy**: [N] units across [N] orders totaling $[amount]
- **Peak safety stock**: [N] units ([N] weeks of cover)
- **Markdown trigger**: [Date] or [inventory level]
- **Projected sell-through**: [%]
- **Key risk**: [Primary risk — e.g., "Long lead time requires blind buy 4 months before peak"]

---

## Constraint Validation

| Constraint | Limit | Plan Maximum | Status |
|---|---|---|---|
| Warehouse capacity | [N] units / [N] pallets | [N] units / [N] pallets | [OK / Adjusted] |
| Cash flow (monthly max) | $[amount] | $[amount] | [OK / Adjusted] |
| Supplier MOQ | [N] units per order | [N] units ordered | [OK / Adjusted] |
| Shelf life | [N] months | [N] months max hold | [OK / Risk] |

---

## Risk Register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Demand exceeds forecast by >20% | [H/M/L] | Stockouts during peak | Reserve budget for in-season replenishment |
| Demand falls short by >20% | [H/M/L] | Excess inventory, margin erosion | Earlier markdown trigger, negotiated return terms |
| Supplier delay (>2 weeks) | [H/M/L] | Late arrival for peak | Split orders across suppliers, air freight contingency |
| Storage capacity exceeded | [H/M/L] | Receiving delays, overflow cost | Phased deliveries, offsite storage arrangement |

---

## Methodology Notes

- **Decomposition method**: [Multiplicative / Additive] seasonal decomposition
- **Seasonal indices**: Calculated from [N] years of data, averaged and normalized
- **Trend projection**: [Linear / Exponential / Weighted recent]
- **Safety stock method**: [Z-score based on service level target of X%]
- **Lead times used**: [Supplier-specific / Category average], including [N] days buffer

---

## Next Steps

1. [ ] Approve pre-season buy quantities and place initial orders by [date]
2. [ ] Set up weekly sell-through tracking dashboard for peak season monitoring
3. [ ] Confirm warehouse capacity for peak inventory levels
4. [ ] Brief markdown team on post-season calendar and trigger points
5. [ ] Schedule mid-season review on [date] to adjust replenishment orders
6. [ ] Schedule post-season retrospective on [date] to capture learnings
