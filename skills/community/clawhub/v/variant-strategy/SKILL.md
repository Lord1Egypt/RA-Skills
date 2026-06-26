---
name: Variant Strategy
description: Optimize product color, size, and variant offerings based on sales data, market trends, and inventory constraints.
---

# Variant Strategy

Optimize your product variant mix — colors, sizes, materials, bundles, and configurations — by analyzing sales performance patterns, market demand signals, and inventory holding costs. This skill helps ecommerce operators eliminate underperforming variants that drain resources while identifying high-potential variant gaps that competitors are filling.

## Quick Reference

| Decision | Strong | Acceptable | Weak |
|---|---|---|---|
| Variant count per product | 4-8 variants each generating ≥5% of SKU revenue | 9-15 variants with clear performers identified | 20+ undifferentiated variants with long tail |
| Retirement threshold | Retire variants below 3% revenue share after 90-day evaluation | Retire below 2% after 180 days | No retirement criteria; keep everything forever |
| Size curve methodology | Platform-specific sales data + category benchmarks + target demo | General category benchmarks only | Copy competitor sizing without data validation |
| Color selection process | Trend data + seasonal analysis + competitor gap mapping | Based on supplier availability and margin | Personal preference or random selection |
| Bundle strategy | Data-driven pairings from cart analysis + margin optimization | Logical product pairings based on category | Random groupings to increase AOV without analysis |
| Variant pricing | Margin-tiered pricing reflecting perceived value differences | Flat pricing across all variants | Arbitrary pricing with no cost or value logic |
| Launch testing approach | Test 3-5 variants with pre-launch demand signals before full rollout | Launch full variant set and measure after 30 days | Launch all variants simultaneously with no testing plan |
| Inventory allocation | Sales-velocity-weighted allocation with safety stock by variant | Equal allocation across all variants | Allocation based on supplier minimum orders only |

## Solves

- **Variant bloat diagnosis**: Identify which of your 15+ color/size options are dragging down average margin and confusing buyers with decision paralysis
- **Size curve optimization**: Build data-driven size distributions for apparel, footwear, and accessories launches using category benchmarks and target demographic profiles
- **Color rationalization**: Determine which colors to keep, retire, or add based on sales velocity, return rates, seasonal trends, and competitor gap analysis
- **Bundle strategy design**: Create profitable product bundles by analyzing cart co-occurrence data, margin math, and perceived value uplift
- **New variant launch validation**: Test market demand for potential new variants before committing inventory investment using search volume, competitor analysis, and pre-launch signals
- **Inventory allocation optimization**: Distribute inventory across variants proportionally to expected demand rather than equally or by supplier minimums
- **Variant cannibalization detection**: Find variants that are stealing sales from each other rather than expanding total demand

## Workflow

### Step 1 — Gather variant performance data
Collect current variant-level sales data including units sold, revenue, return rate, conversion rate, and inventory turnover for each variant over the past 90 days minimum. Request the product category, target audience, platform, and any planned launches or seasonal considerations.

**Required data points per variant:**
- Units sold (last 30/60/90 days)
- Revenue contribution (% of total SKU revenue)
- Conversion rate (sessions to purchase)
- Return rate and top return reasons
- Current inventory level and days of supply
- Holding cost or storage fee exposure
- Customer ratings/reviews by variant (if available)

### Step 2 — Classify variants using the performance matrix
Plot each variant on a 2x2 matrix of Revenue Contribution (high/low) vs. Growth Trend (increasing/decreasing). This produces four categories:

- **Stars** (High revenue + Growing): Invest more, expand inventory
- **Cash Cows** (High revenue + Flat/declining): Maintain but monitor closely
- **Question Marks** (Low revenue + Growing): Evaluate for potential promotion
- **Dogs** (Low revenue + Declining): Candidates for retirement

**Classification thresholds:**
- High revenue: ≥8% of total SKU revenue
- Low revenue: <5% of total SKU revenue
- Growing: ≥10% unit increase over prior period
- Declining: ≥10% unit decrease over prior period

### Step 3 — Analyze variant-level economics
Calculate the true profitability of each variant including COGS, fulfillment cost differentials, storage costs, return processing costs, and any platform-specific fees. Some variants may appear profitable on revenue but are negative-margin after accounting for higher return rates or storage costs.

**Key economic metrics:**
- Gross margin per variant (after COGS and fulfillment)
- Net margin per variant (after returns, storage, advertising allocation)
- Inventory turns per year
- Days of supply at current velocity
- Storage cost per unit per day
- Return-adjusted revenue (revenue minus return processing cost)

### Step 4 — Conduct competitive gap analysis
Map your variant offerings against top 3-5 competitors in the same category and price range. Identify variants competitors offer that you lack (gap opportunities) and variants you offer that no competitor carries (differentiation opportunities or warning signs).

**Analysis framework:**
- Which variants do ALL top competitors offer? (table stakes)
- Which variants does only the category leader offer? (premium signals)
- Which variants do competitors stock that you lack? (gap opportunities)
- Are there search volume signals for variants nobody offers? (blue ocean)

### Step 5 — Build the optimized variant mix recommendation
Based on performance data, economics, and competitive analysis, produce a recommended variant mix with specific actions for each variant: Keep, Promote, Retire, Add, or Test. Include a size/color curve if applicable showing recommended inventory allocation percentages.

**Recommendation structure:**
- Keep (no change): Variants performing well with positive economics
- Promote: Underperforming variants with positive signals worth investing in
- Retire: Variants failing both revenue and economic thresholds
- Add: Gap opportunities validated by demand signals
- Test: Potential additions requiring market validation before commitment

### Step 6 — Design the implementation and testing plan
Create a phased rollout plan for variant changes. Retiring variants requires inventory sell-through strategy. Adding variants requires demand validation and inventory planning. Include KPIs and measurement timeline for tracking the impact of changes.

**Implementation phases:**
- Phase 1 (Week 1-2): Retire clear "Dogs" with sell-through pricing
- Phase 2 (Week 3-4): Promote "Question Marks" with targeted advertising
- Phase 3 (Week 5-8): Test new variant additions with limited inventory
- Phase 4 (Week 9-12): Measure results and adjust ongoing mix

### Step 7 — Create monitoring dashboard specifications
Define the ongoing monitoring metrics and review cadence to keep the variant mix optimized over time. Variant performance shifts with seasons, trends, and competitive moves — a one-time optimization degrades without ongoing monitoring.

**Monitoring cadence:**
- Weekly: Sales velocity by variant, inventory levels, return rates
- Monthly: Performance matrix re-classification, margin analysis
- Quarterly: Full competitive gap analysis, seasonal adjustment
- Annually: Complete variant strategy review with trend forecasting

## Example 1: Apparel Brand T-Shirt Color Optimization

**Input provided:**
- Product: Premium cotton t-shirt, $38, sold on Shopify DTC + Amazon
- Current variants: 12 colors (Black, White, Navy, Gray, Red, Green, Olive, Burgundy, Tan, Pink, Lavender, Coral)
- Target audience: Men and women 25-40, urban professionals, basics-focused
- 90-day sales data provided

**Analysis results:**

Performance Matrix Classification:
| Variant | Revenue % | Trend | Category | Margin | Return Rate |
|---|---|---|---|---|---|
| Black | 28.2% | +5% | Star | 62% | 4.1% |
| White | 18.5% | +3% | Star | 58% | 6.8% |
| Navy | 14.1% | Flat | Cash Cow | 61% | 3.9% |
| Gray | 11.3% | -2% | Cash Cow | 60% | 4.5% |
| Olive | 7.8% | +18% | Star | 59% | 5.2% |
| Burgundy | 5.1% | +8% | Question Mark | 57% | 5.8% |
| Red | 4.2% | -12% | Dog | 55% | 8.3% |
| Tan | 3.8% | -5% | Dog | 56% | 7.1% |
| Green | 2.9% | -8% | Dog | 54% | 6.2% |
| Pink | 2.1% | +2% | Question Mark | 53% | 9.4% |
| Lavender | 1.3% | -15% | Dog | 51% | 11.2% |
| Coral | 0.7% | -22% | Dog | 49% | 13.5% |

Competitive Gap Analysis: Top 3 competitors all carry Charcoal (you lack it). Category leader offers a "Washed Black" variant at premium (+$4). None carry Coral or Lavender. Search volume shows growing demand for Sage Green and Oatmeal.

**Recommendations:**
- **Keep**: Black, White, Navy, Gray, Olive (79.9% of revenue, healthy margins)
- **Promote**: Burgundy (growing, improve imagery and push to fall collection feature)
- **Retire**: Coral (0.7% revenue, -22% trend, 13.5% returns, negative net margin), Lavender (1.3%, declining, high returns)
- **Test**: Charcoal (competitor validation + demand signals), Sage Green (search trend growth)
- **Monitor**: Red, Tan, Green, Pink — set 60-day performance gates

Projected outcome: Reducing from 12 to 8-9 colors reduces SKU complexity by 25-33%, improves average margin by ~3 points, and reduces inventory holding costs by ~$2,400/quarter.

## Example 2: Electronics Accessory Size/Bundle Optimization

**Input provided:**
- Product: Phone case, $24.99, sold on Amazon US
- Current variants: 18 variants (6 phone models × 3 materials: silicone, leather, clear)
- Target audience: iPhone and Samsung flagship users, 20-45, style-conscious
- 90-day sales data provided, total revenue $147K

**Analysis results:**

Revenue Concentration Analysis:
- Top 5 variants (iPhone 15 Pro Max × all materials + iPhone 15 Pro Silicone): 68% of revenue
- Bottom 8 variants: 9% of revenue combined
- Samsung variants (all 9): 12% of revenue total, declining 8% QoQ

Material preference by platform data:
- Silicone: 52% of units (highest velocity, lowest margin at 41%)
- Clear: 31% of units (medium velocity, medium margin at 48%)
- Leather: 17% of units (lowest velocity, highest margin at 63%)

Bundle opportunity from cart analysis:
- 23% of phone case buyers also purchase screen protector within 7 days
- 12% also purchase charging cable
- Case + screen protector bundle at $34.99 would yield 55% margin vs. 41-63% individual

**Recommendations:**
- **Keep**: All current iPhone variants (88% of revenue)
- **Retire**: Samsung S23 leather and clear (0.8% combined revenue, declining, high return rate). Keep Samsung S24 line only.
- **Add**: iPhone 16 series variants (pre-launch preparation based on leaked dimensions)
- **Add**: Case + Screen Protector bundle for top 3 iPhone models (projected +$18K/quarter revenue at 55% margin)
- **Test**: MagSafe-compatible material variant for iPhone lineup (growing search volume, premium positioning at $34.99)

Projected outcome: Reducing from 18 to 14 variants while adding 3 bundles. Expected revenue lift of 12-15% from bundles and reduced decision paralysis, margin improvement of 4 points from retiring low-margin Samsung variants.

## Common Mistakes

1. **Making variant decisions on revenue alone without margin analysis**: A variant doing 8% of revenue looks healthy until you discover its 12% return rate and premium material cost make it negative-margin after returns. Always calculate return-adjusted net margin per variant.

2. **Retiring variants too quickly without sell-through strategy**: Cutting a variant with $5K of inventory creates a dead stock problem. Plan a 30-60 day sell-through with progressive discounting before officially retiring any variant.

3. **Copying competitor variant mixes without context**: A competitor offering 20 colors may have different audience demographics, price positioning, or supply chain economics. Validate competitor gaps against YOUR demand signals before adding variants.

4. **Ignoring seasonal and trend cycles**: A color performing poorly in January may be a top seller in June. Evaluate at least 12 months of data before retirement, and flag seasonal variants rather than eliminating them.

5. **Equal inventory allocation across variants**: Allocating 100 units each to 10 colors when Black outsells Coral 40:1 guarantees stockouts on winners and dead stock on losers. Use sales-velocity-weighted allocation with safety stock buffers.

6. **Treating variant addition as zero-cost**: Each new variant adds complexity in inventory management, photography, listing optimization, advertising, and customer service. Calculate the true cost of variant complexity before adding.

7. **Not measuring variant cannibalization**: Adding a "Charcoal" variant may not create net-new demand — it may split purchases from "Black" and "Gray." Monitor whether total SKU revenue increases or redistributes after adding similar variants.

8. **Ignoring the decision paralysis effect**: Research consistently shows that too many options reduce conversion rates. For most product categories, 5-8 variants optimize the balance between choice and conversion. Beyond 12, diminishing returns accelerate.

## Resources

- [Output Template](references/output-template.md) — Structured variant analysis report format
- [Size Curve Reference](references/size-curve-reference.md) — Standard size distributions by apparel category and demographic
- [Color Trend Guide](references/color-trend-guide.md) — Seasonal color performance patterns and trend analysis framework
- [Quality Checklist](assets/quality-checklist.md) — 40-item quality assurance checklist for variant analysis completeness
