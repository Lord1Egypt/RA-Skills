# Financial Frameworks

## NPV/IRR

### What It Is
Investment decision criteria for evaluating whether a project or acquisition creates value.

### Definitions
- **NPV** (Net Present Value): Sum of all future cash flows discounted to today. NPV > 0 means the project creates value above the cost of capital
- **IRR** (Internal Rate of Return): The discount rate at which NPV = 0. Compare to hurdle rate (typically 10-20% for strategic investments)
- **Payback Period**: When cumulative cash flows turn positive. Simple but ignores time value of money

### How to Build
1. **Project cash flows**: Revenue - Costs - Capex - Tax, by year
2. **Choose discount rate**: WACC for corporate projects, target return for PE/VC
3. **Calculate NPV**: `NPV = Σ [CFt / (1 + r)^t]` for each year t
4. **Calculate IRR**: The rate r where NPV = 0 (use solver or iteration)
5. **Run sensitivity**: Vary discount rate ±2pp, vary cash flows ±15%, find break-even points

### Decision Rules
- **NPV > 0**: Project creates value → proceed (subject to other considerations)
- **IRR > hurdle rate**: Project exceeds minimum return threshold → proceed
- **When NPV and IRR conflict**: Prefer NPV for mutually exclusive projects (IRR can mislead with non-standard cash flow patterns)

### Common Pitfalls
- Using nominal cash flows with a real discount rate (or vice versa) — be consistent
- Ignoring terminal value (often 50-70% of total NPV for growth businesses)
- False precision: Projecting to the dollar when assumptions have ±20% uncertainty
- Forgetting to include integration costs, restructuring charges, or working capital changes in acquisition models

### Quality Check
- Cash flows and discount rate use consistent inflation treatment
- Terminal value approach is stated and justified (perpetuity growth vs. exit multiple)
- Sensitivity analysis covers the 2-3 most uncertain assumptions
- Break-even values identified for the key decision variables

---

## Build/Buy/Partner

### What It Is
A framework for evaluating how to acquire a capability, enter a market, or grow — by building internally, acquiring, or partnering.

### Evaluation Criteria

| Criterion | Build | Buy | Partner |
|-----------|-------|-----|---------|
| Speed to market | Slow (2-5 years) | Fast (6-12 months) | Medium (1-2 years) |
| Control | Full | Full (post-integration) | Shared |
| Cost | Lower upfront, higher ongoing | High upfront, potentially lower ongoing | Moderate ongoing |
| Risk | Execution risk | Integration risk | Alignment risk |
| Capability transfer | Organic learning | Acquired expertise | Limited transfer |
| Reversibility | Sunk cost | Very difficult | Can be dissolved |

### How to Apply
1. Define the capability or market access needed
2. Score each option (Build/Buy/Partner) against the criteria above
3. Add deal-specific factors: Is there a suitable acquisition target? Does the client have partnership track record? Does internal talent exist to build?
4. Assess time sensitivity: If the market window is closing, "build" may not be viable regardless of other merits
5. Model the economics of each option (NPV comparison)

### When Each Wins
- **Build**: When the capability is core to competitive advantage and speed isn't critical
- **Buy**: When speed matters, a suitable target exists, and the client has integration capability
- **Partner**: When risk sharing is important, capabilities are complementary, or regulatory/political factors favor collaboration

### Quality Check
- All three options genuinely evaluated (not just validating a pre-determined answer)
- Economics modeled for each option, not just qualitative pros/cons
- Integration risk explicitly assessed for "Buy" option
- Time-to-value compared across options

---

## Zero-Based Budgeting (ZBB)

### What It Is
A cost optimization approach where every expense must be justified from zero each period, rather than adjusting the prior year's budget incrementally.

### How to Apply
1. **Categorize costs**: Group all costs into decision packages — discrete activities or functions that can be independently evaluated
2. **For each package, answer**:
   - What does this cost exist to achieve?
   - What would happen if we stopped it entirely?
   - What is the minimum cost to achieve the objective?
   - Are there alternative ways to achieve the same objective at lower cost?
3. **Rank packages** by return on investment or strategic importance
4. **Fund from zero**: Allocate budget starting with highest-priority packages until the budget constraint is reached. Everything below the line gets cut or redesigned
5. **Implement**: Build execution plan with timelines, owners, and tracking metrics

### ZBB Cost Categories
- **Non-negotiable**: Regulatory requirements, safety, contractual obligations. Fund at required levels
- **Strategic**: Directly supports competitive advantage. Fund at competitive parity or above
- **Enabling**: Supports operations but doesn't differentiate. Fund at efficient levels — benchmark against best-in-class
- **Discretionary**: Nice to have. Fund last, cut first

### Quality Check
- Every cost category has been challenged, not just low-hanging fruit
- Savings estimates are realistic (achievable within timeframe, with implementation costs included)
- Risks of cuts are identified (e.g., cutting customer service capacity may increase churn)
- Quick wins (<90 days) distinguished from structural changes (6-18 months)

---

## Should-Cost Modeling

### What It Is
A procurement and pricing framework that estimates what a product or service *should* cost based on its components, rather than accepting the supplier's price.

### How to Build
1. **Decompose the product/service** into constituent components (materials, labor, overhead, margin)
2. **Price each component independently**:
   - Raw materials: commodity prices, market benchmarks
   - Labor: hours × wage rates (benchmarked by region/skill)
   - Overhead: industry standard as % of direct cost (typically 15-30%)
   - Margin: reasonable supplier margin (benchmark against industry, typically 5-15%)
3. **Sum components** to derive the "should-cost"
4. **Compare to actual price**: The gap between actual and should-cost is the negotiation opportunity

### When to Use
- Procurement negotiations (justify price reduction demands)
- Make-or-buy decisions (compare internal cost to supplier quotes)
- Pricing strategy (ensure product pricing covers true costs plus target margin)
- Due diligence (validate target company's cost structure)

### Quality Check
- All components identified and independently priced
- Benchmark data is recent and relevant (same geography, same scale)
- Overhead and margin assumptions are reasonable (not artificially low to manufacture a gap)
- Analysis accounts for supplier switching costs and relationship value
