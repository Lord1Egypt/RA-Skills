# Free-Shipping Threshold Strategy Playbook

Framework for deciding if, when, and how to offer free shipping without destroying margin.

---

## Decision Tree

```
Can you afford free shipping on all orders?
├── Shipping < 30% of CM → Yes: offer universally, use as conversion lever
└── Shipping > 30% of CM → No: use a threshold
    ├── What threshold?
    │   ├── Method 1: AOV × 1.15–1.30 (nudge up basket size)
    │   ├── Method 2: Margin math (threshold where CM absorbs shipping)
    │   └── Method 3: Competitor benchmarking
    └── Should you threshold or just raise prices?
        ├── If price-sensitive market → Threshold (perceived savings)
        └── If premium positioning → Bake into price, show "free shipping"
```

---

## Threshold Calculation Methods

### Method 1: AOV Multiplier
```
Suggested threshold = AOV × 1.15 to 1.30

If AOV = $45 → threshold = $52–59
If AOV = $70 → threshold = $81–91
```
This encourages customers to add one more item. Works best when you have add-on products in the $10–25 range.

### Method 2: Margin Math
```
Minimum threshold = Shipping cost / (CM% - target net margin%)

Example:
- Avg shipping cost to absorb: $9.50
- CM% (before shipping): 55%
- Target net margin after shipping: 25%
- Minimum threshold: $9.50 / (0.55 - 0.25) = $31.67

Round up to $35 for clean number.
```

### Method 3: Order Distribution Analysis
Look at your actual order value distribution:

| Order Value Range | % of Orders | Cumulative % | Threshold Verdict |
|---|---|---|---|
| < $25 | XX% | XX% | Too low — most orders don't qualify |
| $25–50 | XX% | XX% | — |
| $50–75 | XX% | XX% | Sweet spot if 40–60% qualify |
| $75–100 | XX% | XX% | — |
| > $100 | XX% | 100% | Too high — threshold irrelevant |

**Target: 40–60% of orders should naturally qualify.** This creates incentive for the rest to add items without giving away shipping on orders that would have converted anyway.

---

## Policy Options Comparison

| Policy | Pros | Cons | Best For |
|---|---|---|---|
| Free on all orders | Highest conversion, simplest messaging | Most expensive, subsidizes small orders | High-margin products, AOV > $80 |
| Free over $X threshold | Lifts AOV, controllable cost | Threshold can frustrate low-value shoppers | Most DTC brands |
| Flat rate ($X.XX) | Simple, partially offsets cost | Less compelling than "free" | Medium-margin products |
| Calculated (exact) | No margin risk | Highest cart abandonment | B2B, heavy/bulky items |
| Free for members/subscribers | Drives loyalty, recurring revenue | Complexity, membership friction | Subscription-first brands |
| Free on specific items | Targeted, promotional | Confusing if overused | Clearance, high-margin items |

---

## Impact Measurement

Track these metrics before and after a free-shipping policy change:

| Metric | Before | After | Change | Impact |
|---|---|---|---|---|
| Conversion rate | X.X% | X.X% | +/- X.X% | [Significant / Marginal] |
| Average order value | $XX.XX | $XX.XX | +/- $X.XX | [Above / Below threshold lift] |
| Cart abandonment rate | XX% | XX% | +/- X.X% | [Improved / No change] |
| Shipping cost as % of rev | X.X% | X.X% | +/- X.X% | [Sustainable / Risky] |
| Gross margin | XX% | XX% | +/- X.X% | [Healthy / Compressed] |
| Units per order | X.X | X.X | +/- X.X | [Bundle effect / No change] |

---

## Common Threshold Mistakes

1. **Setting threshold too low** — Everyone already qualifies; no AOV lift, just margin giveaway
2. **Setting threshold too high** — Nobody qualifies; same as not offering free shipping
3. **Not showing progress bar** — Customers need to see "Add $12 more for free shipping"
4. **Ignoring zone variance** — Free shipping to Zone 8 costs 2× Zone 2 but revenue is the same
5. **No A/B test** — Launch with split test, not gut feel
6. **Forgetting seasonal surcharges** — Q4 peak surcharges can break a threshold that works in Q2
