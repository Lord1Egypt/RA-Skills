# Entry Examples

Concrete examples of well-formatted supply chain entries with all fields.

## Learning: Forecast Error (Seasonal Demand Spike)

```markdown
## [LRN-20250415-001] forecast_error

**Logged**: 2025-04-15T10:30:00Z
**Priority**: high
**Status**: pending
**Area**: demand_planning

### Summary
Q4 seasonal demand spike not captured in baseline forecast model, caused 30% understock on top 15 SKUs

### Details
The demand planning model used a 12-week rolling average with no seasonality decomposition.
Q4 holiday demand for gift-category SKUs spiked 45% above the rolling average. The model
predicted 8,200 units; actual demand was 11,900 units. This resulted in stockouts on 15 of
our top 50 SKUs for 9 days during peak selling season. Estimated lost revenue: $340,000.

The root cause is that the rolling average smooths out seasonal patterns. SKUs in the gift
category have a consistent Q4 lift that should be modeled with a seasonal index.

### Suggested Action
Implement seasonal decomposition (Holt-Winters or similar) for SKUs with >20% seasonal
variance. Apply category-level seasonal indices where item-level history is insufficient.
Validate forecast accuracy monthly using MAPE and bias metrics.

### Metadata
- Source: demand_forecast_review
- SKU Category: gift, seasonal
- Related Files: demand_model/forecast_q4_2025.xlsx
- Tags: forecast, seasonal, MAPE, understock, holiday
- Pattern-Key: forecast_error.seasonal_miss
- Impact: $340,000 lost revenue, 9-day stockout on 15 SKUs

---
```

## Learning: Supplier Risk (Single-Source Critical Component)

```markdown
## [LRN-20250416-001] supplier_risk

**Logged**: 2025-04-16T09:15:00Z
**Priority**: critical
**Status**: pending
**Area**: procurement

### Summary
Single-source supplier for MCU-7200 microcontroller with no qualified backup; 6-week lead time increase threatens production

### Details
Supplier Shenzhen MicroTech is the sole qualified source for the MCU-7200 microcontroller
used in our flagship product line. They communicated a lead time increase from 8 weeks to
14 weeks due to wafer allocation constraints at their foundry. No alternative supplier is
qualified, and qualifying a new source takes 16-20 weeks including first-article inspection.

Current inventory covers 5 weeks of production. With the new 14-week lead time, there is a
9-week gap that cannot be bridged without production line stoppage or emergency spot buys
at 3-4x standard cost.

### Suggested Action
1. Recommend bridge replenishment order for human approval before lead time extends further
2. Begin qualification of Taiwan Semiconductor Components as alternate source
3. Evaluate pin-compatible alternatives (MCU-7210, MCU-7250) for design flexibility
4. Add supplier diversification policy: no single-source for components with >$50K annual spend

### Metadata
- Source: supplier_communication
- Supplier: Shenzhen MicroTech (SMT-4421)
- Component: MCU-7200 microcontroller
- Related Files: procurement/supplier_scorecards/smt-4421.xlsx
- Tags: single-source, microcontroller, lead-time, qualification, critical-component
- Pattern-Key: supplier_risk.single_source
- Impact: potential 9-week production stoppage, $2.1M revenue at risk

---
```

## Learning: Demand Signal Shift (Viral Social Media Spike)

```markdown
## [LRN-20250418-001] demand_signal_shift

**Logged**: 2025-04-18T14:00:00Z
**Priority**: high
**Status**: resolved
**Area**: demand_planning

### Summary
Viral TikTok post caused 10x overnight demand spike for SKU-8842; safety stock depleted in 4 hours

### Details
A TikTok creator with 2.3M followers featured our SKU-8842 (portable blender) in a
morning routine video. The post went viral overnight, generating 12M views. Daily orders
jumped from ~80 units to ~850 units within 6 hours. Safety stock of 320 units was depleted
by 10:00 AM. Backorder queue reached 2,400 units over the next 3 days.

Standard demand planning models cannot predict viral social media events. However, the
response playbook was slow — it took 18 hours to escalate to the supplier and 72 hours
to get an expedited production commitment.

### Suggested Action
1. Implement social media listening alerts for brand mentions exceeding 5x baseline
2. Create demand spike response playbook with pre-negotiated expedite lanes
3. Establish safety stock buffer for social-media-sensitive SKUs (2x standard)
4. Add real-time POS/order velocity monitoring with automatic alerts at 3x daily run rate

### Metadata
- Source: order_management_system
- SKU: SKU-8842 (portable blender)
- Related Files: demand_planning/spike_analysis_apr2025.xlsx
- Tags: viral, social-media, demand-spike, tiktok, safety-stock, response-time
- Pattern-Key: demand_signal_shift.viral_social

### Resolution
- **Resolved**: 2025-04-25T16:00:00Z
- **Notes**: Expedited 3,000 units from supplier in 10 days; implemented social listening alert

---
```

## Supply Chain Issue: Logistics Delay (Port Congestion)

```markdown
## [SCM-20250420-001] logistics_delay

**Logged**: 2025-04-20T08:00:00Z
**Priority**: high
**Status**: pending
**Area**: logistics

### Summary
Port congestion at Shenzhen Yantian terminal added 14 days to ocean freight, affecting 12 inbound containers

### Details
Yantian terminal experienced severe congestion due to a combination of typhoon season delays
and increased export volume. Vessel berthing wait times increased from 1-2 days to 8-10 days.
Twelve of our inbound containers carrying Q3 inventory for the North America distribution center
were affected. Original ETA was May 5; revised ETA is May 19.

Downstream impact: safety stock at the Dallas DC will be depleted by May 12 for 23 SKUs.
Customer order fill rate is projected to drop from 97% to 82% for the affected period.

### Impact
- 14-day delay on 12 containers (TEU: 24)
- 23 SKUs at risk of stockout
- Projected fill rate drop: 97% → 82%
- Estimated cost: $180,000 (expedite fees + lost sales)

### Mitigation Steps
1. Divert 4 containers to Nansha port (7-day shorter queue)
2. Air-freight top 8 critical SKUs (cost: $45,000, saves 10 days)
3. Activate West Coast routing for next 2 shipments
4. Notify customer service of potential delays for affected SKUs

### Metadata
- Carrier: COSCO Shipping Lines
- Route: Shenzhen Yantian → Los Angeles → Dallas DC
- Containers: 12 (24 TEU)
- Related Files: logistics/congestion_report_apr2025.pdf
- Tags: port-congestion, yantian, ocean-freight, delay, fill-rate

---
```

## Supply Chain Issue: Inventory Mismatch (WMS vs Physical Count)

```markdown
## [SCM-20250422-001] inventory_mismatch

**Logged**: 2025-04-22T11:30:00Z
**Priority**: high
**Status**: pending
**Area**: warehousing

### Summary
WMS shows 500 units of SKU-3301 at Chicago DC; physical cycle count reveals only 340 units (32% variance)

### Details
During routine cycle counting at the Chicago distribution center, SKU-3301 (wireless earbuds)
showed a 160-unit discrepancy between WMS recorded quantity (500) and physical count (340).
This is a 32% variance, far exceeding the 2% acceptable threshold.

Preliminary root cause analysis points to:
1. Receiving discrepancy: 2 inbound shipments in March may have been short-shipped but
   receipted at PO quantity without verification
2. Pick/pack errors: the SKU is stored adjacent to SKU-3302 (similar packaging), and 3
   mispick incidents were logged in the past 30 days
3. Possible shrinkage: the SKU is high-value ($89 retail) and small form factor

### Impact
- 160 units unaccounted ($14,240 at cost)
- 3 customer orders at risk if allocated against phantom inventory
- Inventory accuracy metric dropped from 98.2% to 96.1% for the DC

### Corrective Actions
1. Perform wall-to-wall count for all SKU-33XX items in zone B3
2. Audit March receiving records against supplier ASN data
3. Relocate SKU-3301 away from SKU-3302 to prevent mispicks
4. Install bin-level barcode scanning for high-value SKU zones
5. Reduce cycle count interval for A-class SKUs from monthly to weekly

### Metadata
- DC: Chicago Distribution Center (CHI-DC-01)
- Location: Zone B3, Rack 14, Levels 2-4
- Related Files: warehouse/cycle_count_apr2025.xlsx
- Tags: cycle-count, variance, mispick, receiving, shrinkage, accuracy

---
```

## Feature Request: Automated Supplier Risk Scoring

```markdown
## [FEAT-20250415-001] automated_supplier_risk_scoring

**Logged**: 2025-04-15T17:00:00Z
**Priority**: medium
**Status**: pending
**Area**: procurement

### Requested Capability
Automated supplier risk scoring dashboard that aggregates lead time performance, quality
rejection rates, financial health indicators, and geographic concentration risk into a
composite score updated weekly.

### User Context
Currently supplier risk is assessed manually via quarterly business reviews. Two critical
supplier failures in the past year were not flagged until they caused production impact.
An automated scoring system would provide early warning by detecting trend deterioration
(e.g., lead time creeping up 5% per month, rejection rate trending from 0.5% to 1.8%).

### Complexity Estimate
complex

### Suggested Implementation
1. Aggregate data from ERP (PO lead times, on-time delivery), QMS (rejection rates,
   SCAR count), and financial feeds (D&B scores, news alerts)
2. Calculate composite risk score: 40% delivery performance, 25% quality, 20% financial
   health, 15% geographic/concentration risk
3. Set tier thresholds: Green (0-30), Yellow (31-60), Red (61-100)
4. Trigger alerts when a supplier moves from Green to Yellow or Yellow to Red
5. Dashboard showing trend lines, top 10 at-risk suppliers, and recommended actions

### Metadata
- Frequency: recurring (requested 3 times in past 6 months)
- Related Features: supplier scorecard, ERP integration, quality management system

---
```

## Learning: Promoted to Safety Stock Policy

```markdown
## [LRN-20250410-003] forecast_error

**Logged**: 2025-04-10T11:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: safety stock policy (INVENTORY_POLICY.md)
**Area**: inventory

### Summary
Consistent 2-3 week supplier lead time variability requires safety stock buffer of 3 weeks for ocean-freight sourced SKUs

### Details
Analysis of 6 months of inbound shipment data shows that ocean-freight-sourced SKUs
experience lead time variability of 10-21 days (mean: 14 days). The existing safety stock
calculation assumed a 3-day standard deviation. In reality, the variability is driven by
port congestion, vessel schedule changes, and customs clearance delays that are not
normally distributed — they exhibit a fat right tail.

Stockout events correlated with periods when actual lead time exceeded the assumed 95th
percentile by more than 7 days. Increasing safety stock from 2 weeks to 3 weeks of
average demand for ocean-freight SKUs would have prevented 4 of 5 stockout events in
the past 6 months.

### Suggested Action
Updated safety stock policy: Ocean-freight SKUs must carry 3 weeks of average weekly
demand as safety stock. Air-freight SKUs retain 1-week buffer. Domestic-sourced SKUs
retain 1.5-week buffer. Review quarterly against actual lead time data.

### Metadata
- Source: inventory_analysis
- SKU Group: ocean-freight-sourced (142 SKUs)
- Related Files: inventory/safety_stock_policy_v2.xlsx
- Tags: safety-stock, lead-time, variability, ocean-freight, stockout
- Pattern-Key: forecast_error.lead_time_variability
- Recurrence-Count: 5
- First-Seen: 2024-10-15
- Last-Seen: 2025-04-10

---
```

## Learning: Promoted to Skill (Supplier Diversification Checklist)

```markdown
## [LRN-20250412-001] supplier_risk

**Logged**: 2025-04-12T15:00:00Z
**Priority**: critical
**Status**: promoted_to_skill
**Skill-Path**: skills/supplier-diversification-checklist
**Area**: procurement

### Summary
Systematic supplier diversification checklist developed after 3 single-source failures in 12 months

### Details
Developed a repeatable qualification and diversification workflow after encountering 3
separate single-source supplier failures: MCU-7200 lead time crisis (Jan), adhesive
supplier factory fire (Apr), and connector supplier financial distress (Aug). Each
incident caused 2-6 weeks of production disruption.

The checklist covers: identification of single-source risk, qualification timeline
estimation, dual-source cost-benefit analysis, first-article inspection requirements,
and ongoing performance monitoring.

### Suggested Action
Follow the supplier diversification checklist:
1. Identify all single-source components with >$50K annual spend
2. Assess qualification timeline for each (typically 16-20 weeks)
3. Run cost-benefit: qualification cost vs. expected disruption cost (probability × impact)
4. Prioritize by risk score (lead time × spend × sole-source flag)
5. Begin qualification for top 5 highest-risk components per quarter
6. Require dual-source for any component in revenue-critical BOM

### Metadata
- Source: procurement_review
- Related Files: procurement/supplier_diversification_policy.md
- Tags: single-source, diversification, qualification, risk, BOM
- See Also: LRN-20250116-001, SCM-20250401-003, SCM-20250820-001

---
```
