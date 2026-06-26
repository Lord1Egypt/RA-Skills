---
name: Supply Chain & Logistics Intelligence
slug: supply-chain-intel
description: >
  AI-powered global supply chain and logistics intelligence engine. Tracks ocean freight rates (Drewry/Freightos),
  port throughput (LA/LB, China ports), trade flows (UN Comtrade, US Census), transit times (Flexport OTI),
  equipment availability (Container xChange), and 5 major commodity bottlenecks (semiconductors, batteries, APIs,
  agriculture, rare earths). Monitors 14 risk factors (geopolitical, climate, labor, regulatory, cyber) across
  4 logistics modes (air, ocean, rail, truck). Delivers real-time disruption alerts and cost optimization insights.
triggers:
  - "supply chain disruption"
  - "freight rates tracker"
  - "port congestion"
  - "trade flow analysis"
  - "logistics cost optimization"
  - "commodity bottleneck"
  - "shipping delay"
  - "supply chain risk assessment"
  - "inventory management"
  - "sourcing intelligence"
  - "customs clearance"
  - "3PL selection"
  - "warehouse location"
  - "supply chain resilience"
author: Marvis
version: "1.0"
metadata:
  emoji: "🚢"
  requires: "references/supply_chain_sources.json"
---

# Supply Chain & Logistics Intelligence

## Capabilities

| # | Capability | Input | Output |
|---|-----------|-------|--------|
| 1 | Freight Rate Dashboard | Route (e.g., Shanghai-LA) / mode (ocean/air) | Spot rate, 1Y range, trend, capacity outlook, booking lead time |
| 2 | Port Congestion Monitor | Port(s) / region | Vessel queue length, dwell time, gate hours, labor status, weather impact |
| 3 | Trade Flow Analyzer | Country pair / commodity (HS code) | Volume, value, growth rate, seasonality, tariff impact, alternative routes |
| 4 | Commodity Bottleneck Scanner | Commodity (semiconductors, batteries, etc) | Key suppliers, geographic concentration, lead time, price volatility, substitution options |
| 5 | Supply Chain Risk Heatmap | Company / product / region | Geopolitical risk, climate exposure, labor disruption probability, regulatory compliance burden |
| 6 | Transit Time Estimator | Origin-destination + mode | Current transit days, historical variability, delay probability, expedited options cost |
| 7 | Inventory Optimization Model | Demand forecast + lead time variability | Safety stock level, reorder point, EOQ, service level vs. carrying cost trade-off |
| 8 | Sourcing Intelligence | Component / raw material | Supplier landscape, pricing benchmarks, quality ratings, ESG compliance, dual-sourcing feasibility |
| 9 | Logistics Cost Benchmark | Shipment profile (weight, volume, value) | Cost breakdown (freight, fuel surcharge, customs, insurance), vs. industry average |
| 10 | Disruption Alert System | Watchlist (ports, suppliers, routes) | Real-time alerts (strikes, weather, sanctions), impact assessment, contingency plan suggestions |

## Workflow

```
User Query
  │
  ├─ [Step 1] Classify → logistics mode + commodity + geography + time horizon
  │
  ├─ [Step 2] Multi-source data retrieval:
  │   └─ Freight rates: Drewry, Freightos
  │   └─ Port data: Port of LA/LB, China Ports Association
  │   └─ Trade: UN Comtrade, US Census
  │   └─ Risk: Resilinc, Bloomberg SCM
  │   └─ Equipment: Container xChange
  │
  ├─ [Step 3] Cross-validate & flag discrepancies
  │
  ├─ [Step 4] Apply supply chain models:
  │   └─ Inventory optimization (EOQ, safety stock)
  │   └─ Network design (facility location, routing)
  │   └─ Risk quantification (VaR for lead time)
  │
  ├─ [Step 5] Generate structured output with actionable insights
  │
  └─ [Step 6] Cite data vintage, source URLs, confidence intervals
```

## Output Formats

### Freight Rate Snapshot
| Route | Mode | Spot Rate | 1W Change | 1Y Range | Capacity | Booking Lead Time |
|-------|------|-----------|-----------|----------|----------|-------------------|
| Shanghai-LA | Ocean | $X,XXX/TEU | +X% | $X,XXX-$X,XXX | Tight | 3-4 weeks |
| Frankfurt-ORD | Air | $X.XX/kg | -X% | $X.XX-$X.XX | Available | 1-2 days |

### Port Congestion Dashboard
| Port | Vessels Waiting | Avg Dwell Time (days) | Gate Hours | Labor Status | Weather Alert |
|------|----------------|----------------------|------------|--------------|---------------|
| Los Angeles | 12 | 4.2 | 24/7 | Normal | None |
| Rotterdam | 8 | 3.8 | 6am-10pm | Strike warning | High winds |

### Commodity Bottleneck Matrix
| Commodity | Key Suppliers | Geographic Risk | Lead Time (weeks) | Price Volatility | Substitution Options |
|-----------|--------------|-----------------|-------------------|------------------|---------------------|
| Advanced Semiconductors | TSMC, Samsung, Intel | Taiwan Strait, US-China | 26-52 | High | None (critical) |
| Lithium-ion Batteries | CATL, LG, Panasonic | China, DRC, Chile | 12-24 | Medium | Sodium-ion (emerging) |

## Usage Guidelines

1. **Real-time data priority** — supply chain data decays rapidly; flag any data >7 days old
2. **Multi-modal comparison** — always present air vs. ocean vs. rail trade-offs (cost vs. speed vs. reliability)
3. **Risk quantification** — express disruptions in $ impact and lead time extension, not just qualitative
4. **Actionable recommendations** — each insight should link to a decision (reroute, expedite, buffer stock, dual-source)
5. **Regulatory compliance** — include customs, sanctions (OFAC), forced labor (UFLPA), carbon border (CBAM) considerations
6. **Scenario planning** — provide best-case/worst-case/base-case for critical decisions

## Examples

### Example 1: Freight Cost Optimization
**User**: "Best way to ship 100 TEU from Shenzhen to Chicago in Q3 2026?"
**Output**: Ocean vs. rail vs. air cost/speed comparison; port pair recommendations (Shenzhen→LA vs. Shenzhen→Vancouver); transit time variability; fuel surcharge forecast; contingency for Panama Canal drought.

### Example 2: Disruption Impact Assessment
**User**: "What's the impact of a potential ILWU strike at LA/LB ports?"
**Output**: Historical strike duration (days), backlog buildup rate (TEU/day), alternative ports (Oakland, Tacoma, Mexico), cost premium for air freight, inventory burn-down timeline for key industries.

### Example 3: Sourcing Strategy
**User**: "Should we dual-source rare earth magnets from China and Vietnam?"
**Output**: Supplier capability comparison, quality variance, lead time differential, tariff implications, ESG risk (China Xinjiang concerns), total landed cost model.

---

**Data Base**: `references/supply_chain_sources.json` — 14 authoritative data sources, 5 key commodities, 5 risk factors, 4 logistics modes.
**Last Updated**: June 2026
**Free Tier**: Available. This skill aggregates public supply chain data; no proprietary carrier contracts accessed.
