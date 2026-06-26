---
name: valuation-comps
description: >
  Comparable company analysis (comps) and business valuation for startups and private companies.
  Build trading comps, transaction comps (M&A precedents), and DCF valuation. Calculate EV/Revenue,
  EV/EBITDA, P/E, and SaaS-specific multiples (ARR multiples, NTM revenue). Outputs investor-ready
  valuation range, football field chart data, and supporting narrative. Use when: a startup needs a
  409A valuation reference, preparing for a fundraise, modeling acquisition price, or benchmarking
  against public peers. NOT for: formal 409A appraisals requiring a licensed appraiser, audit-grade
  fairness opinions, tax filings requiring a certified valuation, or real-time stock price tracking.
version: 1.0.0
author: PrecisionLedger
tags:
  - finance
  - valuation
  - comps
  - m-and-a
  - startups
  - investors
  - saas
  - dcf
---

# Valuation Comps Skill

Build comparable company and transaction analyses for startups, growth companies, and private businesses. This skill guides Sam Ledger through selecting peer companies, pulling multiples, running DCF, and producing a defensible valuation range for fundraising, M&A, or strategic planning.

---

## When to Use This Skill

**Trigger phrases:**
- "What's our company worth?"
- "Build a comps analysis"
- "What multiple should we use for valuation?"
- "We're raising a Series A — what's a fair valuation?"
- "Run comps against public SaaS peers"
- "What's the M&A precedent for companies like ours?"
- "Build a football field chart"
- "What's our DCF value?"
- "Benchmark our valuation vs. competitors"
- "Help me justify our $20M valuation to investors"

**NOT for:**
- Formal 409A appraisals — requires a licensed appraiser (IRC 409A compliance)
- Audit-grade fairness opinions — requires Big 4 or investment bank sign-off
- Tax filings requiring certified business valuation
- Real-time public stock screening (use financial data APIs directly)
- Crypto/token valuation (different methodology — see `defi-position-tracker`)
- Debt valuation or fixed-income analysis

---

## Valuation Methodologies

### 1. Trading Comps (Public Company Comparables)

Benchmarks your company against publicly traded peers. Most relevant for growth-stage companies approaching IPO or raising later-stage rounds.

**Key multiples by stage and type:**

| Company Type | Primary Multiple | Secondary Multiple |
|---|---|---|
| Pre-revenue SaaS | EV/Forward ARR | Team/market multiple |
| Growth SaaS (<$10M ARR) | EV/NTM Revenue | Rule of 40 premium |
| Scale SaaS (>$50M ARR) | EV/NTM Revenue + EV/NTM EBITDA | FCF yield |
| Marketplace | EV/NTM GMV or Revenue | Take rate × GMV multiple |
| Services/Agency | EV/EBITDA | EV/Revenue |
| B2B SaaS | EV/ARR | NTM Revenue growth multiple |
| FinTech | P/E or EV/Revenue | AUM multiple |

**EV (Enterprise Value) formula:**
```
EV = Market Cap + Total Debt - Cash & Equivalents
   = Share Price × Diluted Shares + Debt - Cash
```

**Common multiples:**
```
EV/Revenue = EV ÷ LTM (or NTM) Revenue
EV/EBITDA  = EV ÷ LTM EBITDA
EV/ARR     = EV ÷ Annual Recurring Revenue
P/E        = Share Price ÷ EPS
EV/FCF     = EV ÷ Free Cash Flow
```

**Growth-adjusted multiple (PEG-style for SaaS):**
```
Revenue Multiple ÷ Revenue Growth Rate = Growth-Adjusted Multiple
Example: 10x EV/Revenue at 50% growth = 0.2x growth-adjusted (attractive)
         10x EV/Revenue at 10% growth = 1.0x growth-adjusted (expensive)
```

---

### 2. Transaction Comps (M&A Precedents)

Historical acquisition prices paid for comparable companies. Always reflects a **control premium** (20-40% above trading comps). Most useful for M&A exit modeling.

**Data sources for precedent transactions:**
- SEC EDGAR (8-K filings for public acquirees)
- PitchBook / CapIQ (subscription)
- CB Insights (startup M&A)
- TechCrunch / Crunchbase (public disclosures)
- Press releases and deal announcements

**Transaction comp template:**
```
Target Company | Acquirer | Date | Deal Size | Revenue | EBITDA | EV/Rev | EV/EBITDA | Notes
Acme SaaS      | BigCo    | 2024 | $120M    | $12M    | $2M    | 10.0x  | 60x       | 85% gross margin
Rival Corp     | PE Firm  | 2023 | $80M     | $10M    | $0.5M  | 8.0x   | 160x      | High growth, -$3M EBITDA adj.
```

**Control premium guidance:**
```
Typical range: 20-40% premium over public trading comps
Strategic buyer: 30-50% (synergy value)
Financial buyer (PE): 15-25% (return-driven)
Distressed asset: at or below trading comps
```

---

### 3. DCF (Discounted Cash Flow)

Intrinsic value methodology. Most defensible for mature cash-flow-positive companies; less reliable for early-stage startups with negative FCF.

**DCF formula:**
```
Intrinsic Value = Σ [FCF_t / (1 + WACC)^t] + Terminal Value / (1 + WACC)^n

Where:
  FCF_t = Free Cash Flow in year t
  WACC  = Weighted Average Cost of Capital
  n     = projection period (typically 5-10 years)
  Terminal Value = FCF_n × (1 + g) / (WACC - g)  [Gordon Growth Model]
  g     = perpetual growth rate (typically 2-3%)
```

**WACC for private companies:**
```
WACC = (E/V × Re) + (D/V × Rd × (1 - Tax Rate))

Where:
  E/V = Equity weight (for pre-revenue startup ≈ 1.0)
  Re  = Cost of equity (CAPM: Rf + β × ERP + size/illiquidity premium)
  D/V = Debt weight
  Rd  = Cost of debt (interest rate)

For early-stage startups:
  Rf  = 10-year Treasury yield (~4.5% as of 2026)
  ERP = Equity Risk Premium (~5-6%)
  β   = 1.5-2.5 (high-growth tech)
  Size/illiquidity premium = 3-8%
  → Typical startup discount rate: 20-35%
```

**EBITDA → FCF bridge:**
```
EBITDA
  - Cash Taxes (EBITDA × effective tax rate)
  - CapEx
  ± Change in Working Capital
= Unlevered FCF (UFCF)
```

---

### 4. VC Method (Venture Capital Valuation)

Standard for pre-revenue and early-revenue startups raising VC. Works backward from exit value.

**VC Method formula:**
```
Post-Money Valuation = Exit Value / (1 + Target Return)^years

Step 1: Estimate exit value at year 5-7
  Exit Value = Projected Revenue × Exit Multiple
  Example: $20M revenue × 8x = $160M exit

Step 2: Apply required return
  VC target return: 10x+ (Series A), 5x+ (Series B)
  Post-Money = $160M / 10x = $16M

Step 3: Calculate pre-money
  Pre-Money = Post-Money - Investment Amount
  Example: $16M - $3M = $13M pre-money

Step 4: Calculate dilution
  Ownership = Investment / Post-Money
  Example: $3M / $16M = 18.75%
```

---

### 5. Revenue Multiple Benchmarks (SaaS 2025-2026)

Current market multiples for private SaaS companies (approximate, varies by growth profile):

| ARR Range | Growth Rate | Typical EV/ARR Multiple |
|---|---|---|
| <$1M | >100% YoY | 3-6x ARR |
| $1M-$5M | 80-120% YoY | 5-10x ARR |
| $5M-$20M | 50-80% YoY | 6-12x ARR |
| $20M-$50M | 30-50% YoY | 8-15x ARR |
| $50M+ | 20-30% YoY | 10-20x ARR |

**Multiple adjustments (+ or - from base):**
```
+2-4x: NRR > 130%, CAC payback < 12 months, gross margin > 80%
+1-2x: Strong brand moat, enterprise contracts, zero churn
-2-4x: High churn (>5%/month), single-customer concentration >30%
-3-5x: Declining growth, commodity product, low gross margin (<60%)
```

---

## Comparable Company Selection Framework

### Step 1: Define the Peer Group

Criteria for selecting comps:
```
□ Business model (SaaS, marketplace, services, etc.)
□ Revenue scale (within 0.3x-3x of subject company)
□ Growth rate (similar trajectory ± 20%)
□ Gross margin profile (within 10-15% of subject)
□ Geography (domestic vs. international)
□ End market / vertical (fintech, HR tech, etc.)
□ Customer type (SMB, mid-market, enterprise)
```

**Minimum comp set:** 5-8 companies
**Ideal comp set:** 10-15 companies (trim outliers)

### Step 2: Collect Multiples

For each comp, gather:
```
Company Name | Ticker | EV | LTM Rev | NTM Rev | LTM EBITDA | ARR | Growth % | NTM EV/Rev | EV/EBITDA
```

**Data sources:**
- Public: SEC filings (10-K, 10-Q), Yahoo Finance, Bloomberg, CapIQ
- Private: PitchBook, Crunchbase, CB Insights press releases
- SaaS benchmarks: Bessemer Cloud Index, Battery Ventures Cloud 100

### Step 3: Calculate Statistics

```
Mean, Median, 25th percentile, 75th percentile for each multiple

Use median as primary reference (eliminates outlier distortion)
Use 25th-75th percentile as defensible range

Example:
  NTM EV/Revenue multiples: [6x, 8x, 9x, 10x, 11x, 14x, 20x]
  Mean: 11.1x | Median: 10x | 25th: 8x | 75th: 13x
  → Valuation range: 8x-13x NTM Revenue
```

---

## Football Field Chart

Visual representation of valuation across methodologies.

**Format (text output for import to Excel/Sheets):**

```
Methodology              | Low      | Mid      | High     | Implied EV Range
-------------------------|----------|----------|----------|-----------------
Trading Comps            | $45M     | $62M     | $85M     | 8x-13x NTM Rev
Transaction Comps        | $60M     | $80M     | $110M    | +30% control prem.
DCF (Base Case)          | $40M     | $58M     | $75M     | 20-25% discount rate
DCF (Bull Case)          | $55M     | $78M     | $105M    | 18% discount rate
VC Method (5yr exit)     | $50M     | $70M     | $95M     | 10x return target
52-Week Public Peer Range| $48M     | $65M     | $90M     | Market range
-------------------------|----------|----------|----------|-----------------
COMPOSITE RANGE          | $45M     | $69M     | $110M    |
RECOMMENDED RANGE        | $60M     | $75M     | $90M     | Defensible to investors
```

---

## Step-by-Step Workflow

When a user requests a valuation or comps analysis:

### Step 1: Intake
```
□ Company name, stage (seed/A/B/growth)
□ Business model (SaaS, marketplace, services)
□ Current ARR/MRR or LTM Revenue
□ Revenue growth rate (YoY or MoM)
□ Gross margin %
□ EBITDA (or burn rate if negative)
□ NTM (next 12 month) revenue projection
□ Valuation purpose: fundraising, M&A, 409A reference, board reporting
□ Any prior round valuations or term sheets received
```

### Step 2: Select Methodology
- **Pre-revenue / seed:** VC Method + market comps (qualitative)
- **<$1M ARR:** VC Method + ARR multiple
- **$1M-$20M ARR:** ARR multiple + transaction comps
- **>$20M ARR:** Trading comps + DCF + transaction comps

### Step 3: Identify Comps
- List 5-10 comparable companies
- Gather multiples from public sources or proxies
- Apply adjustments for private company discount (20-30% vs. public)

### Step 4: Calculate Range
- Apply median multiple to subject company metrics
- Build 25th-75th percentile range
- Add DCF check if cash-flow profile warrants

### Step 5: Football Field
- Assemble valuation outputs across methodologies
- Identify point where 3+ methods converge → defensible range

### Step 6: Output
- Valuation range table
- Football field data
- Narrative: "Based on comps and growth profile, a $X-$Y valuation is defensible because..."
- Key sensitivity: what variable most affects valuation?

---

## Example Usage

**User:** "We're raising a Series A. $1.2M ARR, growing 15% MoM, 75% gross margin, B2B SaaS. What valuation can we defend?"

**Sam's response:**

```
Valuation Analysis — Series A

Company Profile:
  ARR: $1.2M | MoM Growth: 15% (214% annualized) | Gross Margin: 75%
  NTM ARR estimate: ~$4.8M (at 15% MoM sustained)

Methodology 1 — ARR Multiple (Current ARR)
  Peer range for high-growth B2B SaaS at $1M-$5M ARR: 6x-12x ARR
  At median (8x): $9.6M post-money
  At high (12x): $14.4M post-money

Methodology 2 — NTM Revenue Multiple
  NTM ARR ~$4.8M × 6x-10x = $28.8M-$48M
  Discount 30% for early stage: $20M-$33M

Methodology 3 — VC Method
  Exit at year 5: $50M ARR × 10x = $500M
  Required 10x return on Series A → Post-money = $50M
  (Optimistic; assumes execution to plan)

DEFENSIBLE RANGE: $12M-$18M post-money
  → $10-14M pre-money + $2-4M raise = 17-28% dilution

Why: 15% MoM is elite growth. 75% gross margin is healthy. 
At $1.2M ARR, comps support 8-12x current ARR. Investors 
paying for NTM will want to underwrite to $4-5M ARR delivery.

Investor pushback prep:
  - "Why not 15x ARR?" → Only justified if NRR > 120% or enterprise logo density
  - "Why not 5x ARR?" → Growth rate doesn't support pessimistic multiple
  - Anchor: $15M post-money, accept $12M if lead investor adds strategic value
```

---

## SaaS Benchmarking Reference

**Rule of 40 premium:**
```
Rule of 40 = Revenue Growth % + EBITDA Margin %
Score ≥ 40: Standard multiple applies
Score ≥ 60: +15-25% multiple premium
Score < 20: -20-30% discount

Example: 80% growth + (-30% EBITDA) = 50 → healthy, standard multiple
```

**NRR impact on multiples:**
```
NRR < 90%:   -30% to multiple (churn destroying value)
NRR 90-100%: Baseline
NRR 100-110%: +10-15% 
NRR 110-120%: +20-30%
NRR > 120%:  +30-50% (expansion-led growth)
```

**Gross margin impact:**
```
< 50%:  -25% to SaaS multiple (cost of delivery too high)
50-65%: -10%
65-75%: Baseline
75-85%: +10-15%
> 85%:  +20-30% (pure software economics)
```

---

## Integration Points

- **`startup-financial-model`** — Build the NTM projections that feed into NTM multiple valuation
- **`cap-table-manager`** — Translate valuation range into dilution modeling and SAFE conversion
- **`investor-memo-generator`** — Wrap the valuation analysis into the investor narrative
- **`due-diligence-dataroom`** — Package comps analysis alongside other diligence materials
- **`fractional-cfo-playbook`** — Valuation section of the CFO advisory playbook

---

## Quick Reference: Multiple Cheat Sheet

```
Stage            | Typical Multiple  | Basis
Pre-seed/seed    | 5-15x ARR         | ARR or VC method
Series A         | 8-20x ARR         | NTM Revenue × multiple
Series B         | 10-25x ARR        | NTM Revenue, Rule of 40
Series C+        | 8-20x NTM Rev     | Growth + margin mix
Profitable SaaS  | 5-12x EBITDA      | EBITDA quality
Distressed       | 1-2x Revenue      | Acqui-hire or liquidation value

Market Context (2025-2026):
  High-growth SaaS (>50% YoY): 8-15x NTM Revenue
  Mid-growth SaaS (20-50%):    5-10x NTM Revenue
  Mature SaaS (<20%):          3-7x NTM Revenue
  Services/Consulting:         0.8-2x Revenue, 4-10x EBITDA
  Marketplace (high take rate): 5-12x NTM Revenue
```

**Private company discount:** Apply 20-30% discount vs. public trading comps to reflect:
- Illiquidity premium
- Concentration risk (founder-dependent)
- Limited operating history / smaller scale
- Less rigorous financial controls
