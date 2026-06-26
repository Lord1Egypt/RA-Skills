# Supplier Risk Scoring System — Supplier Risk Index (SRI)
**Framework:** Supplier Risk Index (SRI)
**Price:** $19
**Category:** Productivity / Risk Management
**Tags:** supplier risk, vendor risk, procurement, risk scoring, ops, compliance
**last_validated:** 2026-03-03

---

## What This Is

The Supplier Risk Index (SRI) is a structured scoring system that produces a 0-100 risk score for every vendor across five dimensions. It classifies vendors into Green, Yellow, or Red tiers and prescribes specific actions for each tier. Run it at onboarding, annually, and whenever a vendor's situation changes materially.

**Problem it solves:** Ops teams can't manage vendor risk without a consistent framework. The SRI eliminates gut-feel risk assessments and gives procurement teams an objective, defensible methodology for prioritizing vendor oversight and making sourcing decisions.

**Output:** A risk score (0-100), tier classification (Green/Yellow/Red), and a recommended action plan for every supplier in your portfolio.

---

## The SRI Framework

**Five Risk Dimensions:**

```
┌─────────────────────────────────────────────────────────┐
│              SUPPLIER RISK INDEX (SRI)                  │
│                                                         │
│  D1: Financial Stability           (max 25 pts)         │
│  D2: Single-Source Dependency      (max 20 pts)         │
│  D3: Compliance History            (max 20 pts)         │
│  D4: Performance Track Record      (max 20 pts)         │
│  D5: Geographic / Regulatory Risk  (max 15 pts)         │
│                                                         │
│  Total SRI Score: 0-100                                 │
│  (Higher = LOWER risk — score is a "health" score)      │
└─────────────────────────────────────────────────────────┘
```

**Note:** The SRI is a health score, not a risk score — higher is better. A score of 90 means low risk; a score of 20 means high risk. This keeps it intuitive: you want vendors to score high.

---

## DIMENSION 1: Financial Stability (25 points)

**Why it matters:** A financially unstable supplier can't fulfill contracts, maintain quality, or stay in business. Financial instability is the leading cause of unexpected supply chain disruption.

**What to assess:**

| Indicator | How to Evaluate |
|-----------|----------------|
| Business age | Years in operation |
| Revenue stability | Growing / Stable / Declining |
| Funding/ownership | Bootstrapped stable, PE-backed, VC-backed, public |
| Credit risk signals | Late payments to their vendors, legal judgments |
| Concentration risk | Are they heavily dependent on a single customer? |

**Scoring Rubric:**

| Condition | Points |
|-----------|--------|
| Company 5+ years old, stable/growing revenue, no financial red flags | 25 |
| Company 3-5 years old, stable revenue, minor concerns | 18-22 |
| Company 1-3 years old (startup), VC-funded or early-stage | 10-17 |
| Company has known financial stress (late payments, restructuring, news of losses) | 3-9 |
| Company has declared bankruptcy, receivership, or is insolvent | 0-2 |

**Data Sources:**
- Dun & Bradstreet Paydex score (business credit)
- Dunn & Bradstreet or Experian Business Credit Report
- LinkedIn / public news search for financial distress signals
- SEC filings (public companies)
- Self-reported financials for small vendors ($25K+ spend: request last 2 years' financials)
- References from their other major customers

**Scoring Action:** For vendors scoring below 15 on D1, escalate to Finance for review before awarding new contracts.

---

## DIMENSION 2: Single-Source Dependency (20 points)

**Why it matters:** If you rely on one vendor for a critical product or service with no alternative, you're exposed. Any disruption — financial, operational, or relationship — creates immediate business risk.

**What to assess:**

| Factor | Question |
|--------|----------|
| Replaceability | How quickly can you replace this vendor if they disappear? |
| Alternatives | How many qualified alternatives exist in the market? |
| Revenue concentration | What % of your spend goes to this vendor? |
| Criticality | What happens to operations if this vendor stops delivering? |
| Switching cost | Time and cost to transition to an alternative |

**Scoring Rubric:**

| Condition | Points |
|-----------|--------|
| Multiple qualified alternatives exist, vendor is easily replaceable in <30 days | 20 |
| Some alternatives exist, 30-90 day replacement window, moderate switching cost | 13-19 |
| Few alternatives, 90-180 day replacement window, significant switching cost | 6-12 |
| No alternatives identified, critical dependency, >180 day replacement window | 0-5 |

**Dependency Multiplier (apply if both conditions are true):**
- Vendor is the ONLY source for a critical input/service **AND**
- Vendor accounts for >30% of your spend in that category

→ **Reduce D2 score by 5 points** (floor at 0)

**Scoring Action:**
- Any vendor scoring 0-5 on D2 should have a documented contingency plan
- Any vendor with the Dependency Multiplier applied should have a backup vendor identification project initiated

---

## DIMENSION 3: Compliance History (20 points)

**Why it matters:** Compliance failures are leading indicators — they signal process weakness, poor management, or risk-taking culture. A vendor that's had one compliance issue is statistically more likely to have another.

**What to assess:**

| Area | What to Check |
|------|--------------|
| Insurance compliance | COI gaps, lapses, late renewals |
| Regulatory compliance | Industry violations, fines, regulatory actions |
| Legal history | Lawsuits, judgments, settlements |
| Data / security incidents | Breaches, audit failures, security violations |
| Contract compliance | Prior vendor relationships, terminations for cause |
| Licensing | Valid licenses maintained in all required jurisdictions |

**Scoring Rubric:**

| Condition | Points |
|-----------|--------|
| Clean history — no known compliance issues in 3+ years | 20 |
| Minor issues, fully resolved, 1-2 instances in 3 years | 14-19 |
| Moderate issues (1-2 regulatory warnings, minor litigation) — resolved | 8-13 |
| Significant issues (major litigation, regulatory action, insurance lapse) — resolved | 3-7 |
| Active unresolved compliance issues, ongoing litigation, or recent serious violations | 0-2 |

**Data Sources:**
- Your internal vendor record (COI tracking, past issues)
- Court records search (PACER for federal, state court websites)
- Better Business Bureau
- State licensing board lookups
- Google News search: "[Vendor Name] lawsuit OR violation OR fine OR breach"
- Industry-specific databases (FDA for food/pharma, OSHA for contractors, etc.)

**Scoring Action:** Any vendor scoring 0-7 on D3 requires a Legal review before contract renewal.

---

## DIMENSION 4: Performance Track Record (20 points)

**Why it matters:** Past performance is the most reliable predictor of future performance. Vendors with consistent quality, on-time delivery, and responsive issue resolution are lower risk than vendors with spotty records.

**What to assess:**

| Metric | How to Measure |
|--------|---------------|
| On-time delivery rate | % of deliverables/invoices delivered on schedule |
| Quality defect rate | # of quality issues reported in last 12 months |
| Issue resolution time | Average days to resolve a reported problem |
| Communication responsiveness | Response time to queries and escalations |
| Contract adherence | Are they delivering exactly what was contracted? |
| Customer satisfaction | Internal stakeholder rating of the vendor |

**Scoring Rubric (for existing vendors with performance history):**

| Condition | Points |
|-----------|--------|
| Consistently exceeds expectations, <2 issues/year, fast resolution | 20 |
| Meets expectations, 2-5 minor issues/year, resolved promptly | 14-19 |
| Mostly meets expectations, occasional issues, moderate resolution time | 8-13 |
| Inconsistent, frequent issues, slow resolution, complaints from internal teams | 3-7 |
| Significant ongoing performance problems, at-risk relationship | 0-2 |

**For New Vendors (no internal history):**
- Default to 12 points (neutral)
- Adjust up/down based on references: +3 for strong references, -3 for weak references
- First 90 days: conduct a performance check-in (milestone review) and update score

**Scoring Action:** Any vendor scoring 0-7 on D4 should be on a Performance Improvement Plan (see Vendor Performance Audit skill).

---

## DIMENSION 5: Geographic & Regulatory Risk (15 points)

**Why it matters:** Where a vendor operates and where they're incorporated can create risk — political instability, regulatory changes, natural disaster exposure, data sovereignty requirements, and trade compliance complexity.

**What to assess:**

| Factor | Risk Indicators |
|--------|----------------|
| Country of operation | Political stability, sanctions risk, trade restrictions |
| Data sovereignty | Does data leave the country? GDPR, CCPA, HIPAA applicability? |
| Natural disaster exposure | Operations in high-risk zones (hurricanes, earthquakes, flooding) |
| Regulatory environment | Is their industry heavily regulated in their jurisdiction? |
| Currency / FX risk | Are payments in a volatile currency? |
| Export controls | Any ITAR, EAR, or export control applicability? |

**Geographic Risk Reference:**

| Vendor Location | Risk Level | Starting Points |
|----------------|------------|----------------|
| US, Canada, UK, EU (stable) | Low | 12-15 |
| Australia, New Zealand, Japan, South Korea | Low | 12-15 |
| Mexico, Brazil, India | Moderate | 8-11 |
| Eastern Europe, Middle East (stable countries) | Moderate-High | 5-9 |
| China (data handling concerns, regulatory risk) | High | 3-6 |
| Countries with active US sanctions or instability | Very High | 0-2 |

**Regulatory Complexity Modifier:**

| Condition | Adjustment |
|-----------|-----------|
| Vendor operates in a heavily regulated industry (healthcare, finance, defense) | -2 pts |
| Vendor handles personal data across international borders | -2 pts |
| Vendor has active export control considerations | -3 pts |
| Vendor has robust regulatory compliance program documented | +2 pts |

**Scoring Action:** Any vendor scoring 0-5 on D5 should be reviewed by Legal or Compliance before contract execution.

---

## SRI Score Calculation

### Step 1: Score Each Dimension

| Dimension | Max Points | Your Score |
|-----------|-----------|-----------|
| D1: Financial Stability | 25 | ___ |
| D2: Single-Source Dependency | 20 | ___ |
| D3: Compliance History | 20 | ___ |
| D4: Performance Track Record | 20 | ___ |
| D5: Geographic / Regulatory Risk | 15 | ___ |
| **TOTAL SRI SCORE** | **100** | **___** |

### Step 2: Classify the Tier

| SRI Score | Tier | Label |
|-----------|------|-------|
| 75-100 | 🟢 Green | Low Risk |
| 50-74 | 🟡 Yellow | Moderate Risk |
| Below 50 | 🔴 Red | High Risk |

---

## Recommended Actions by Tier

### 🟢 Green (75-100): Low Risk
- **Review frequency:** Annual
- **Oversight level:** Standard contract management
- **Actions:**
  - Include in standard quarterly performance reviews
  - Monitor for any D1/D2/D3 trigger events
  - Document score in vendor record
  - Eligible for preferred vendor status, extended contracts, increased spend

### 🟡 Yellow (50-74): Moderate Risk
- **Review frequency:** Semi-annual (every 6 months)
- **Oversight level:** Active monitoring
- **Actions:**
  - Identify the lowest-scoring dimension(s) and focus remediation there
  - Request a vendor meeting to discuss risk areas
  - For D2 issues: begin identifying backup vendors
  - For D3 issues: request compliance documentation
  - For D4 issues: initiate performance discussion
  - Set 90-day improvement targets for specific dimensions
  - Do not increase spend or award new contracts until score improves

### 🔴 Red (Below 50): High Risk
- **Review frequency:** Monthly
- **Oversight level:** Active risk management
- **Actions:**
  - Escalate to manager immediately
  - Notify internal stakeholders who depend on this vendor
  - Initiate contingency planning (backup vendor identification)
  - Place hold on new POs pending remediation plan
  - Send formal risk notification to vendor
  - Set 60-day remediation deadline
  - If score doesn't improve to Yellow within 90 days: recommend transition plan

---

## Trigger Events (Re-Score Immediately)

Outside of scheduled reviews, re-score a vendor immediately when:
- News of financial difficulty (layoffs, funding cuts, bankruptcy rumors)
- Insurance lapse or COI non-compliance detected
- Major customer of theirs announces they're switching vendors
- Significant leadership change at vendor
- Regulatory action or public litigation filed
- Security breach or data incident
- Merger, acquisition, or ownership change
- Natural disaster affecting their operations
- Your team reports a significant quality or delivery failure

---

## Portfolio-Level Risk Analysis

After scoring all vendors, conduct a portfolio review:

### Risk Distribution Target
| Tier | Target | Action if Exceeded |
|------|--------|--------------------|
| 🟢 Green | >70% of portfolio | — |
| 🟡 Yellow | <25% of portfolio | Address highest-risk Yellows first |
| 🔴 Red | <5% of portfolio | Immediate remediation or transition |

### Concentration Analysis
- Identify your top 5 vendors by annual spend
- If any top-5 vendor is Red tier → priority escalation
- If >50% of spend is concentrated in vendors below 75 SRI → portfolio risk alert

### Single-Source Audit
- List every vendor where your D2 score is ≤5
- These are your critical single-source dependencies
- Each one should have a documented contingency plan within 90 days

---

## SRI Registry Fields

Track these fields in your vendor registry:

| Field | Notes |
|-------|-------|
| Vendor ID | |
| Vendor Name | |
| D1: Financial Stability Score | 0-25 |
| D2: Single-Source Score | 0-20 |
| D3: Compliance History Score | 0-20 |
| D4: Performance Score | 0-20 |
| D5: Geographic Risk Score | 0-15 |
| Total SRI Score | 0-100 |
| Risk Tier | Green / Yellow / Red |
| Last Scored | Date |
| Next Review Date | Annual / Semi-annual / Monthly |
| Key Risk Notes | Free text |
| Contingency Plan | Y/N + link |
| Action Status | None / In Progress / Escalated |

---

## Expected Outputs

After implementing SRI:
1. ✅ Risk score (0-100) for every vendor in your portfolio
2. ✅ Tier classification (Green/Yellow/Red) with documented rationale
3. ✅ Prioritized list of vendors requiring active risk management
4. ✅ Identified single-source dependencies with contingency planning triggered
5. ✅ Portfolio-level risk distribution with trend tracking
6. ✅ Scheduled re-review cadence for every vendor

**Decision quality improvement:** Teams using structured risk scoring report 40-60% fewer vendor-related surprises because risk signals are identified before they become crises.

---

*Supplier Risk Index (SRI) — Part of the Vendor & Compliance Operations Pack by Remy Claw*
*More at remyclaw.com | @Remy_Claw on X*
