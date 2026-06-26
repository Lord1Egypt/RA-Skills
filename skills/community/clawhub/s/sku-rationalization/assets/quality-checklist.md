# SKU Rationalization Quality Checklist

## Data Completeness (7 items)
- [ ] Sales data covers at least 6 months (ideally 12+ months)
- [ ] All active SKUs are included in the export
- [ ] Dormant/discontinued SKUs are flagged separately
- [ ] COGS data is present for every SKU
- [ ] Return/refund data is included
- [ ] Current inventory on-hand quantities are current (within 7 days)
- [ ] Data source and export date are documented

## Data Quality (6 items)
- [ ] No negative quantities or prices
- [ ] No duplicate SKU entries
- [ ] Zero-revenue SKUs are investigated (new launch vs. dead stock)
- [ ] Currency is consistent across all data points
- [ ] Cost data reflects landed cost (not just supplier price)
- [ ] Outliers are identified and explained (e.g., one-time bulk orders)

## Scoring Configuration (6 items)
- [ ] All five scoring dimensions are calculated
- [ ] Weights sum to 100% and are documented
- [ ] Weight rationale matches stated business priority
- [ ] Normalization method is applied consistently
- [ ] Category-specific thresholds are used where appropriate
- [ ] Composite score formula is shown and verifiable

## Keep Bucket Validation (5 items)
- [ ] Keep SKUs genuinely perform well across multiple dimensions
- [ ] No SKUs with negative margins are in the Keep bucket
- [ ] Keep bucket accounts for reasonable % of catalog (typically 20-35%)
- [ ] Keep SKUs' revenue share matches expectations (typically 70-85%)
- [ ] Any Keep overrides are justified

## Fix Bucket Validation (5 items)
- [ ] Each Fix SKU has a specific issue identified
- [ ] Each Fix SKU has a concrete, actionable prescription
- [ ] Investment required for fixes is estimated
- [ ] Projected uplift is quantified
- [ ] Review checkpoint dates are set (30/60/90 days)

## Kill Bucket Validation (7 items)
- [ ] Kill bucket does not include SKUs launched within last 90 days
- [ ] Seasonal products are not killed based on off-season data
- [ ] Strategic assortment SKUs (size runs, color completions) are flagged
- [ ] Supplier minimum order impacts are checked
- [ ] Each Kill SKU has an assigned liquidation strategy
- [ ] Financial impact (capital released, carrying cost saved) is calculated
- [ ] Execution timeline is defined for each Kill action

## Financial Analysis (5 items)
- [ ] Total inventory capital released is calculated
- [ ] Annual carrying cost savings are quantified
- [ ] Storage/FBA fee reduction is estimated where applicable
- [ ] Fix bucket projected revenue uplift is included
- [ ] Net annual impact summary is provided

## Report Quality (6 items)
- [ ] Executive summary is present and concise
- [ ] Full scored SKU table is included and sortable
- [ ] Bucket distribution is visualized
- [ ] Top 10 Kill and Fix candidates have detailed write-ups
- [ ] Methodology notes explain scoring and thresholds
- [ ] Next steps with owners and timelines are listed

## Stakeholder Readiness (4 items)
- [ ] Language matches audience (technical vs. executive)
- [ ] Recommendations are framed as suggestions, not mandates
- [ ] Risks and caveats are disclosed
- [ ] Override mechanism is documented for stakeholder disagreements
