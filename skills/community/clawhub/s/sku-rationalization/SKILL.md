---
name: SKU Rationalization
description: Identify underperforming SKUs, recommend discontinuations, and optimize product catalog for maximum profitability.
---

# SKU Rationalization

Analyze your entire product catalog to surface which SKUs are draining warehouse space, tying up capital, and diluting focus — then generate concrete keep, fix, or kill recommendations backed by multi-factor scoring. This skill bridges the gap between raw sales exports and strategic catalog decisions by combining revenue contribution, margin health, inventory turnover, and demand velocity into a single actionable framework.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Data window | 12+ months of sales data covering full seasonality | 6-11 months with known gaps documented | Under 6 months or missing peak season |
| SKU count | Full catalog export (all active + dormant SKUs) | Active SKUs only with dormant noted | Cherry-picked subset without justification |
| Scoring dimensions | 4+ factors (revenue, margin, turnover, velocity) | 3 factors with reasoning for omissions | 1-2 factors only (e.g., revenue alone) |
| Recommendation clarity | Keep/Fix/Kill with specific next-step actions | Category labels with general guidance | Vague "review further" without direction |
| Threshold calibration | Thresholds tuned to client's industry benchmarks | Standard thresholds with disclosure | Arbitrary cutoffs with no rationale |
| Financial impact | Dollar-value estimates for each recommendation | Directional impact (high/medium/low) | No financial quantification |

## Solves

- You exported your Shopify, Amazon Seller Central, or Shopee product report and want to know which bottom-performing SKUs to cut before next quarter's purchasing round
- Your warehouse manager is flagging space constraints and you need a data-backed list of slow-moving products that can be liquidated or discontinued immediately
- You are preparing for a seasonal reset and need to rationalize your catalog to focus marketing spend on winners
- Your cash flow is tight and you need to identify which inventory investments are generating the worst return on capital
- You merged product lines after an acquisition and need a unified scoring framework to decide which overlapping SKUs survive
- Your marketplace listing fees are eating margin and you want to prune the long tail of zero- or near-zero-velocity SKUs
- You need to present a catalog optimization plan to leadership with clear financial projections

## Workflow

### Step 1 — Collect and validate source data
Gather the full product catalog export including: SKU identifier, product name, category, unit cost (COGS), selling price, units sold per period, current inventory on hand, days of inventory, and any return/refund rates. Validate completeness by checking total SKU count against known catalog size. Flag any SKUs missing cost data or with obvious data errors (negative quantities, prices of $0).

### Step 2 — Calculate scoring dimensions
For each SKU compute the following metrics:
- **Revenue contribution %**: SKU revenue ÷ total catalog revenue
- **Gross margin %**: (Selling price − COGS) ÷ Selling price
- **Inventory turnover ratio**: Units sold (annual) ÷ Average inventory on hand
- **Demand velocity**: Units sold in last 90 days ÷ Units sold in prior 90 days (trend indicator)
- **Return rate %**: Units returned ÷ Units sold
- **Days of supply**: Current inventory ÷ Average daily sales rate

### Step 3 — Normalize and weight scores
Convert each metric to a 0-100 normalized scale using min-max normalization within the catalog. Apply weights based on business priority (default: Revenue 30%, Margin 25%, Turnover 20%, Velocity 15%, Return Rate 10%). Calculate composite score for each SKU.

### Step 4 — Classify into Keep / Fix / Kill buckets
- **Keep** (score 70-100): Strong performers. Maintain or increase inventory investment.
- **Fix** (score 40-69): Underperforming but salvageable. Identify specific issues (pricing? visibility? seasonality?) and prescribe corrective actions.
- **Kill** (score 0-39): Poor performers across multiple dimensions. Recommend discontinuation, liquidation, or bundling strategies.

### Step 5 — Quantify financial impact
For each Kill recommendation, estimate: inventory carrying cost saved, warehouse space freed, and capital released. For each Fix recommendation, estimate potential revenue uplift if corrective action succeeds. Aggregate into a total catalog optimization impact summary.

### Step 6 — Generate actionable output report
Produce the final rationalization report using the output template. Include: executive summary, full scored SKU table (sortable), bucket distribution chart, top 10 Kill candidates with liquidation recommendations, top 10 Fix candidates with specific action plans, and projected financial impact.

### Step 7 — Validate and sanity-check
Cross-check Kill recommendations against: seasonal products (don't kill a winter coat in summer), new launches (< 90 days insufficient data), strategic assortment SKUs (loss leaders, category anchors), and supplier minimum order requirements. Flag any overrides with justification.

## Example 1: Shopify Apparel Brand (150 SKUs)

**Input data**: 12 months Shopify export, 150 active SKUs across 4 categories (tops, bottoms, accessories, outerwear).

**Scoring results**:
- Keep: 42 SKUs (28%) generating 78% of revenue
- Fix: 61 SKUs (41%) generating 19% of revenue
- Kill: 47 SKUs (31%) generating 3% of revenue

**Key findings for Kill bucket**:
| SKU | Product | Revenue % | Margin | Turnover | Composite | Action |
|---|---|---|---|---|---|---|
| APP-2847 | Linen shorts (XXS) | 0.01% | 12% | 0.3x | 8 | Discontinue — size not viable |
| APP-1923 | Wool scarf (pink) | 0.02% | -3% | 0.1x | 5 | Liquidate at 70% off — negative margin |
| APP-3341 | Canvas tote (limited) | 0.04% | 8% | 0.2x | 12 | Bundle with top sellers |

**Fix bucket sample action plan**:
| SKU | Issue identified | Prescribed action | Projected uplift |
|---|---|---|---|
| APP-1150 | Low visibility | Move to featured collection + retarget ads | +$2,400/quarter |
| APP-2201 | Price too high vs competitors | Reduce price 15%, monitor 30 days | +$1,800/quarter |

**Financial impact**: Killing 47 SKUs releases $34,200 in trapped inventory capital, saves $8,100/year in carrying costs, and frees 18% of warehouse capacity.

## Example 2: Amazon Electronics Seller (800 SKUs)

**Input data**: 12 months Amazon Seller Central export, 800 SKUs across 12 subcategories.

**Scoring results**:
- Keep: 184 SKUs (23%) generating 82% of revenue
- Fix: 296 SKUs (37%) generating 15% of revenue
- Kill: 320 SKUs (40%) generating 3% of revenue

**Key findings**: The long tail is severe — 320 SKUs contribute only 3% of revenue but consume 41% of FBA storage fees. Top Kill candidates include 45 phone case SKUs for discontinued phone models and 28 cable variants with less than 1 unit sold per month.

**Fix bucket highlights**: 89 SKUs have strong margins but poor Best Seller Rank due to inadequate listing optimization. Prescribed actions include A+ content creation, keyword optimization, and vine review enrollment.

**Financial impact**: Removing 320 Kill SKUs saves $67,400/year in FBA storage fees, releases $142,000 in inventory capital, and reduces catalog management overhead by approximately 40 hours/month.

## Common Mistakes

1. **Using revenue as the only metric**: Revenue alone misses margin-destroying SKUs that sell well but lose money after returns, shipping, and platform fees. Always include margin and turnover dimensions.

2. **Ignoring seasonality**: Killing a winter product based on summer sales data leads to regret in Q4. Always ensure the analysis window covers at least one full seasonal cycle, or flag seasonal SKUs for manual review.

3. **Forgetting about new launches**: SKUs launched within the last 90 days lack sufficient data for reliable scoring. Exclude them from Kill recommendations and flag them separately as "Insufficient Data."

4. **Not accounting for strategic assortment**: Some low-performing SKUs exist to complete a category assortment (e.g., size runs, color options). Killing them may reduce conversion on the remaining variants. Flag SKUs that are part of a variant group.

5. **Applying uniform thresholds across categories**: A 2x turnover ratio is excellent for furniture but poor for phone accessories. Calibrate thresholds by category or subcategory, not globally.

6. **Skipping the financial impact calculation**: Recommendations without dollar values lack urgency. Always quantify the carrying cost savings, capital release, and storage fee reduction.

7. **Presenting Kill recommendations without liquidation strategy**: Simply saying "discontinue" is incomplete. Specify the exit path: clearance sale, bundle, donate, return to supplier, or destroy.

8. **Not validating against supplier constraints**: Killing a SKU may violate minimum order agreements or lose volume discounts that affect Keep SKUs from the same supplier. Always cross-reference supplier terms.

## Resources

- [Output template](references/output-template.md) — Structured report format for presenting rationalization results
- [Scoring methodology guide](references/scoring-methodology.md) — Detailed explanation of normalization, weighting, and threshold calibration
- [Liquidation strategies](references/liquidation-strategies.md) — Playbook for executing Kill recommendations across different channels
- [Quality checklist](assets/quality-checklist.md) — Pre-delivery validation checklist
