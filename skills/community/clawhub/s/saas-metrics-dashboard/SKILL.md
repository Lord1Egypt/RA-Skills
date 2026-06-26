---
name: saas-metrics-dashboard
description: >
  SaaS metrics calculator and dashboard builder for subscription businesses.
  Compute MRR, ARR, churn rate, NRR/GRR, LTV, CAC, CAC payback period,
  magic number, Rule of 40, quick ratio, and cohort retention. Accepts raw
  subscription data and outputs a structured metrics snapshot ready for
  investor reporting, board decks, or feeding into kpi-alert-system and
  startup-financial-model skills. Use when founders, CFOs, or analysts need
  a full SaaS health check, want to track metrics over time, or are preparing
  investor materials.
  NOT for: e-commerce or transactional businesses (no recurring revenue),
  real-time streaming data pipelines (use a dedicated BI tool), or QBO
  bookkeeping reconciliation (use qbo-automation). Not a replacement for
  a full data warehouse — designed for structured inputs and spot analysis.
version: 1.0.0
author: PrecisionLedger
tags:
  - saas
  - metrics
  - finance
  - startups
  - subscription
  - mrr
  - churn
  - ltv
  - investors
---

# SaaS Metrics Dashboard Skill

Calculate every critical SaaS metric from raw subscription data and produce an investor-ready health snapshot. This skill guides Sam Ledger through computing MRR/ARR, churn, retention, unit economics (LTV/CAC), growth efficiency, and Rule of 40 scoring — then formats the output for board decks, investor updates, or feeding into **kpi-alert-system** threshold monitoring.

---

## When to Use This Skill

**Trigger phrases:**
- "What's our MRR / ARR?"
- "Calculate churn rate for last quarter"
- "Give me our LTV:CAC ratio"
- "Build a SaaS metrics snapshot"
- "Are we Rule of 40 compliant?"
- "Show net revenue retention"
- "Prepare metrics for the investor update"
- "What's our quick ratio / magic number?"
- "Track cohort retention"

**Fits between:**
- `startup-financial-model` — feeds historical actuals into the 3-statement model
- `kpi-alert-system` — outputs threshold-ready metric values for alert monitoring
- `investor-memo-generator` — supplies the metrics section of investor memos

**NOT for:**
- Businesses without recurring subscription revenue
- Real-time live dashboards (needs a BI tool like Metabase/Looker)
- Revenue recognition accounting (use `revenue-recognition-agent`)
- QBO bookkeeping entries (use `qbo-automation`)

---

## Core Metric Definitions

### Revenue Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| MRR | Sum of all monthly recurring charges | — |
| ARR | MRR × 12 | — |
| New MRR | MRR from new customers this period | — |
| Expansion MRR | Upsells + seat adds from existing customers | — |
| Churned MRR | MRR lost from cancellations | — |
| Contraction MRR | Downgrades from existing customers | — |
| Net New MRR | New + Expansion − Churned − Contraction | Positive = growing |

### Retention Metrics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| Logo Churn | Customers churned / Customers at start | <5%/yr for SMB, <2% enterprise |
| Revenue Churn (GRR) | Churned+Contraction MRR / MRR at start | >80% GRR good |
| Net Revenue Retention (NRR) | (Start MRR + Expansion − Churn − Contraction) / Start MRR | >110% excellent, >100% good |
| Quick Ratio | (New + Expansion) / (Churned + Contraction) | >4 = excellent, >2 = healthy |

### Unit Economics

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| LTV | ARPU / Monthly Churn Rate | 3× CAC minimum |
| CAC | (S&M Spend) / New Customers | — |
| LTV:CAC | LTV / CAC | >3:1 healthy, >5:1 strong |
| CAC Payback | CAC / (ARPU × Gross Margin%) | <12mo excellent, <18mo good |
| Magic Number | Net New ARR / Prior Quarter S&M Spend | >1.5 = efficient |

### Growth Efficiency

| Metric | Formula | Benchmark |
|--------|---------|-----------|
| MoM Growth | (MRR This Mo − Prior Mo) / Prior Mo | Top decile: 15%+ early stage |
| Rule of 40 | ARR Growth Rate % + FCF Margin % | ≥40 = healthy |
| Burn Multiple | Net Burn / Net New ARR | <1 = excellent, <2 = good |

---

## Data Inputs Required

Minimum viable inputs:
```
Period: [month/quarter]
MRR at start of period: $___
New MRR: $___
Expansion MRR: $___
Churned MRR: $___
Contraction MRR: $___
New customers acquired: ___
Customers churned: ___
Total customers at start: ___
S&M spend (period): $___
Gross margin %: ___
ARR growth rate (YoY %): ___
FCF or operating cash flow: $___
```

Optional (for deeper analysis):
```
Cohort data (monthly signup + retention by cohort)
Plan-level MRR breakdown
Customer segment breakdown (SMB / Mid-Market / Enterprise)
NPS or CSAT scores
```

---

## Computation Walkthrough

### Step 1: Validate Inputs
- Confirm all required fields are present
- Check: New MRR + Expansion − Churn − Contraction = Net New MRR
- Flag negative MRR values or impossible churn rates (>100%)

### Step 2: Calculate Revenue Metrics
```python
net_new_mrr = new_mrr + expansion_mrr - churned_mrr - contraction_mrr
arr = (mrr_start + net_new_mrr) * 12
```

### Step 3: Retention Metrics
```python
logo_churn = customers_churned / customers_start
grr = 1 - ((churned_mrr + contraction_mrr) / mrr_start)
nrr = (mrr_start + expansion_mrr - churned_mrr - contraction_mrr) / mrr_start
quick_ratio = (new_mrr + expansion_mrr) / (churned_mrr + contraction_mrr)
```

### Step 4: Unit Economics
```python
arpu = (mrr_start + net_new_mrr) / (customers_start + new_customers - customers_churned)
ltv = arpu / (logo_churn / 12)  # annualized to monthly churn
cac = sm_spend / new_customers
ltv_cac = ltv / cac
cac_payback_months = cac / (arpu * gross_margin)
magic_number = (net_new_arr) / prior_sm_spend
```

### Step 5: Growth Efficiency
```python
rule_of_40 = arr_growth_pct + fcf_margin_pct
burn_multiple = abs(net_burn) / net_new_arr  # only if burning cash
```

### Step 6: Score & Grade
Apply benchmark thresholds and assign health grades:
- 🟢 Green: At or above benchmark
- 🟡 Yellow: Within 20% of benchmark
- 🔴 Red: Below benchmark threshold

---

## Output Format

### Snapshot Output (Markdown/Structured)

```
═══════════════════════════════════════
  SAAS METRICS SNAPSHOT — [Period]
  Company: [Name] | As of: [Date]
═══════════════════════════════════════

REVENUE
  MRR:              $___,___
  ARR:              $___,___
  Net New MRR:      $___,___  (New: $X | Exp: $X | Churn: -$X)
  MoM Growth:       X.X%  [🟢/🟡/🔴]

RETENTION
  NRR:              XXX%  [🟢/🟡/🔴]  (benchmark: >110%)
  GRR:              XX%   [🟢/🟡/🔴]  (benchmark: >80%)
  Logo Churn:       X.X%  [🟢/🟡/🔴]  (benchmark: <5%/yr)
  Quick Ratio:      X.X   [🟢/🟡/🔴]  (benchmark: >2)

UNIT ECONOMICS
  LTV:CAC:          X.Xx  [🟢/🟡/🔴]  (benchmark: >3:1)
  CAC Payback:      XX mo [🟢/🟡/🔴]  (benchmark: <18mo)
  Magic Number:     X.X   [🟢/🟡/🔴]  (benchmark: >1.5)

EFFICIENCY
  Rule of 40:       XX    [🟢/🟡/🔴]  (benchmark: ≥40)
  Burn Multiple:    X.X   [🟢/🟡/🔴]  (benchmark: <2)

OVERALL HEALTH:  🟢 Strong / 🟡 Watch / 🔴 At Risk
TOP RISKS:  [1-3 specific metrics to address]
```

### CSV/JSON Output (for kpi-alert-system)
When feeding downstream systems, output as:
```json
{
  "period": "2026-Q1",
  "mrr": 125000,
  "arr": 1500000,
  "nrr": 118,
  "grr": 87,
  "logo_churn_annual": 4.2,
  "quick_ratio": 3.1,
  "ltv_cac": 4.5,
  "cac_payback_months": 11,
  "magic_number": 1.8,
  "rule_of_40": 52,
  "burn_multiple": 0.9
}
```

---

## Cohort Retention Analysis

When cohort data is available, build a retention table:

```
Cohort  Mo1   Mo2   Mo3   Mo6   Mo12
Jan-25  100%  89%   82%   74%   68%
Feb-25  100%  91%   85%   77%   —
Mar-25  100%  88%   81%   —     —
```

Key outputs:
- **Average Day-30 retention** (target: >85% for SMB, >90% enterprise)
- **12-month retention** (logo) — critical for LTV calculation
- **Revenue cohort retention** (expansion often offsets logo churn)

---

## Segment Benchmarks

### By Stage
| Stage | ARR | NRR Target | Logo Churn | Rule of 40 |
|-------|-----|-----------|------------|------------|
| Pre-Seed | <$1M | >100% | <10% | N/A |
| Seed | $1-5M | >105% | <8% | Growth-driven |
| Series A | $5-20M | >110% | <5% | ≥20 |
| Series B+ | $20M+ | >120% | <3% | ≥40 |

### By Customer Segment
| Segment | NRR Target | Logo Churn | CAC Payback |
|---------|-----------|------------|-------------|
| SMB | >100% | <10%/yr | <6 months |
| Mid-Market | >110% | <5%/yr | <12 months |
| Enterprise | >120% | <2%/yr | <18 months |

---

## Integration with Other Skills

### → startup-financial-model
Pass current-period actuals as seed inputs for the 3-statement model:
- Use NRR to project expansion revenue
- Use logo churn to model customer count trajectory
- CAC payback informs S&M budget efficiency

### → kpi-alert-system
Register thresholds for automated alerts:
```
NRR < 100%       → CRITICAL alert (negative net expansion)
Logo churn > 7%  → WARNING alert (annualized)
Quick ratio < 2  → WARNING alert
LTV:CAC < 3      → WARNING alert
Rule of 40 < 30  → INFO alert
```

### → investor-memo-generator
Feed the snapshot JSON into the metrics section of investor memos. Include MoM/QoQ trends, not just point-in-time values.

---

## Examples

### Example 1: Quick Snapshot
**Input:** "Our MRR is $125K. We added $18K new, $12K expansion, lost $8K churn, $3K contraction. 210 customers, lost 7. Spent $45K on S&M. 75% gross margin. YoY growth 85%. Burning $80K/mo."

**Output:** Full snapshot with grades, flagging Rule of 40 and burn multiple.

### Example 2: Investor Prep
**Input:** "Prepare Q1 2026 SaaS metrics for our Series A data room"
**Output:** Formatted snapshot + cohort table + segment breakdown + narrative summary with investor framing.

### Example 3: Board Deck Metrics Slide
**Input:** "Give me the 6 most important metrics for our board deck"
**Output:** MRR/ARR, NRR, Logo Churn, LTV:CAC, CAC Payback, Rule of 40 — each with prior period comparison and trend indicator.

---

## Red Flags to Surface

Always flag proactively:
- **NRR < 100%** — losing more than you're gaining from existing customers
- **Quick Ratio < 1** — churn eating new growth
- **LTV:CAC < 2** — acquiring customers unprofitably
- **CAC Payback > 24 months** — severe capital efficiency problem
- **Burn Multiple > 3** — burning too much per dollar of new ARR
- **Logo churn > 15%/yr** — product-market fit concern

---

*Precision. Integrity. Results. — PrecisionLedger*
