---
name: price-monitor
description: Monitor competitor and product pricing changes across websites. Set price thresholds, get alerts on drops/increases, track historical pricing, and identify pricing patterns. Works for e-commerce, SaaS, and service pricing.
metadata:
  version: 1.0.0
  author: TKDigital
  category: E-Commerce & Intelligence
  tags: [price monitoring, competitor tracking, e-commerce, pricing intelligence, alerts, market research]
---

# Price Monitor

Track competitor pricing changes, set alerts on thresholds, and identify pricing patterns.

## What It Does

1. **Price Tracking** — Monitor product/service prices across competitor websites
2. **Change Detection** — Alert when prices drop, increase, or hit a threshold
3. **Historical Analysis** — Track pricing trends over time
4. **Pattern Detection** — Identify sale cycles, seasonal pricing, A/B price tests
5. **Competitive Comparison** — Side-by-side pricing across multiple competitors
6. **Report Generation** — Weekly/monthly pricing intelligence reports

## Usage

### Set Up Price Monitoring
```
Monitor these competitor prices:

1. [Product/Service] at [URL] — current price: $[X]
2. [Product/Service] at [URL] — current price: $[X]
3. [Product/Service] at [URL] — current price: $[X]

Alert me when:
- Any price drops more than 10%
- Any price goes below $[threshold]
- Any new products/tiers are added
- Any products are discontinued

Check frequency: [daily / weekly]
Report: [weekly summary / only on changes]
```

### Competitive Pricing Analysis
```
Compare pricing across these competitors for [PRODUCT CATEGORY]:

1. [Competitor A] — [URL/pricing page]
2. [Competitor B] — [URL]
3. [Competitor C] — [URL]
4. [Competitor D] — [URL]

For each:
- List all pricing tiers
- Feature comparison at each tier
- Highlight the cheapest option per feature set
- Identify pricing strategies (freemium, value-based, competition-based)
- Recommend where my product should price
```

### SaaS Pricing Intelligence
```
Analyze the SaaS pricing landscape for [CATEGORY]:

Track:
- Pricing page changes (new tiers, price changes, feature additions)
- Free trial / freemium strategy changes
- Annual vs monthly discount trends
- Enterprise / custom pricing signals

Companies: [List 5-10]
Period: Last 6 months (from Wayback Machine / cached pages)
```

## Output Format

```
# Price Monitor Report — [Date]

## Price Changes Detected

| Product | Competitor | Old Price | New Price | Change | Date |
|---------|-----------|-----------|-----------|--------|------|
| [Product] | [Company] | $[X] | $[X] | [+/-X%] | [Date] |

## Alerts Triggered
🔴 [Product] at [Competitor] dropped below $[threshold]
🟡 [Product] at [Competitor] increased by [X]%

## Competitive Pricing Matrix
| Feature / Tier | You | Comp A | Comp B | Comp C |
|---------------|-----|--------|--------|--------|
| Basic | $[X] | $[X] | $[X] | $[X] |
| Pro | $[X] | $[X] | $[X] | $[X] |
| Enterprise | $[X] | $[X] | $[X] | $[X] |

## Pricing Trends
[Observations about pricing direction, patterns, or strategy shifts]

## Recommendations
[What this means for your pricing strategy]
```

## Best Practices

- Monitor 3-5 direct competitors (more = noise)
- Check pricing pages weekly (SaaS changes less frequently than e-commerce)
- Track feature changes alongside price changes
- Use historical data to predict sale cycles
- Combine with `competitor-intel` for full competitive picture

## References

- `references/pricing-strategies.md` — Common SaaS and e-commerce pricing strategies
- `references/monitoring-setup.md` — How to configure effective price monitoring
