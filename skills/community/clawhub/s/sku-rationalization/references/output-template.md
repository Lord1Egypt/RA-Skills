# SKU Rationalization Report — Output Template

## Executive Summary

**Analysis period**: [Start date] — [End date]
**Total SKUs analyzed**: [N]
**Data source**: [Platform/export name]

### Bucket Distribution

| Bucket | SKU Count | % of Catalog | % of Revenue | % of Margin |
|---|---|---|---|---|
| Keep | [N] | [%] | [%] | [%] |
| Fix | [N] | [%] | [%] | [%] |
| Kill | [N] | [%] | [%] | [%] |

### Projected Financial Impact

| Metric | Value |
|---|---|
| Inventory capital released (Kill) | $[amount] |
| Annual carrying cost savings | $[amount] |
| Storage fee reduction (if applicable) | $[amount] |
| Projected revenue uplift from Fix actions | $[amount] |
| Net annual impact | $[amount] |

---

## Full Scored SKU Table

| Rank | SKU | Product Name | Category | Revenue % | Margin % | Turnover | Velocity | Return % | Composite Score | Bucket |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | [ID] | [Name] | [Cat] | [%] | [%] | [x] | [ratio] | [%] | [0-100] | Keep/Fix/Kill |

*Sort by composite score descending. Highlight Kill in red, Fix in yellow, Keep in green.*

---

## Top Kill Candidates

For each of the top 10 Kill-bucket SKUs:

### [SKU ID] — [Product Name]
- **Composite score**: [score]/100
- **Key failure dimensions**: [e.g., "0.1x turnover, -2% margin, declining velocity"]
- **Current inventory**: [units] units ($[value] at cost)
- **Monthly carrying cost**: $[amount]
- **Recommended exit path**: [Clearance sale / Bundle / Return to supplier / Donate / Destroy]
- **Execution timeline**: [e.g., "List at 60% off for 30 days, then destroy remaining"]

---

## Top Fix Candidates

For each of the top 10 Fix-bucket SKUs:

### [SKU ID] — [Product Name]
- **Composite score**: [score]/100
- **Primary issue**: [e.g., "Low visibility — page 4 in search results"]
- **Prescribed action**: [Specific, actionable steps]
- **Investment required**: $[amount] or [hours] of work
- **Projected uplift**: $[amount]/quarter revenue increase
- **Review checkpoint**: [Date — 30/60/90 days to re-evaluate]

---

## Seasonal and Strategic Overrides

| SKU | Product | Bucket (Scored) | Override To | Reason |
|---|---|---|---|---|
| [ID] | [Name] | Kill | Hold | Seasonal — peak demand in Q4 |
| [ID] | [Name] | Kill | Hold | Strategic — completes size run |

---

## Category Breakdown

For each category:

### [Category Name]
- **SKU count**: [N] (Keep: [n], Fix: [n], Kill: [n])
- **Revenue contribution**: [%] of total
- **Average composite score**: [score]
- **Key insight**: [One-sentence takeaway]

---

## Methodology Notes

- **Scoring weights used**: Revenue [%], Margin [%], Turnover [%], Velocity [%], Return Rate [%]
- **Normalization method**: Min-max within catalog
- **Threshold calibration**: [Industry-standard / Custom — describe basis]
- **Data exclusions**: [New launches < 90 days, test SKUs, etc.]

---

## Next Steps

1. [ ] Review Kill list with procurement team for supplier impact
2. [ ] Launch clearance campaigns for approved Kill SKUs
3. [ ] Implement Fix action plans with 30-day review checkpoints
4. [ ] Schedule re-analysis in [90 days] to measure progress
5. [ ] Update inventory planning models with rationalized catalog
