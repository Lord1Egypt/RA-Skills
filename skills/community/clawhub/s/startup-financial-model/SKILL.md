---
name: startup-financial-model
description: >
  Build investor-ready 3-statement financial models for startups: P&L, Balance Sheet, Cash Flow Statement.
  Revenue forecasting with growth assumptions, burn rate analysis, runway calculator, scenario modeling
  (base/bull/bear), and cohort-based SaaS/subscription metrics. Outputs structured data for Excel/Google Sheets
  export. Use when a founder, CFO, or analyst needs a from-scratch financial model, wants to project runway,
  stress-test scenarios, or prepare for an investor diligence request.
  NOT for: public-company financial analysis (use DCF/comps), tax preparation, bookkeeping or reconciliation,
  or real-time data pulls from accounting software (use qbo-automation for that).
version: 1.0.0
author: PrecisionLedger
tags:
  - finance
  - startups
  - modeling
  - forecasting
  - investors
---

# Startup Financial Model Skill

Build complete 3-statement financial models for early-stage and growth-stage startups. This skill guides Sam Ledger through constructing investor-ready models, running scenario analysis, calculating burn/runway, and producing structured output ready for Excel or Google Sheets.

---

## When to Use This Skill

**Trigger phrases:**
- "Build a financial model for…"
- "How much runway do we have?"
- "Create a 3-statement model"
- "What's our burn rate?"
- "Model out our revenue forecast"
- "Investor asks for a 3-year model"
- "Show me base/bull/bear scenarios"

**NOT for:**
- Public company valuation (DCF, comps) — different methodology
- Tax filing or tax planning — use compliance workflows
- Historical bookkeeping — use QBO/accounting integrations
- Real-time actuals syncing — use `qbo-automation` skill
- Cap table modeling — use `cap-table-manager` skill

---

## Core Model Components

### 1. Revenue Model

Start by identifying the **revenue driver type**:

| Business Type | Primary Driver | Key Metric |
|---|---|---|
| SaaS / Subscription | MRR/ARR growth | Churn rate, expansion MRR |
| Marketplace | GMV × take rate | Transaction volume |
| Services / Agency | Headcount × utilization | Billable hours |
| E-commerce | Orders × AOV | Repeat purchase rate |
| Usage-based | Units × price | Volume growth curve |

**Revenue forecasting inputs to collect:**
```
- Current MRR/revenue (starting point)
- Monthly or annual growth rate assumption
- Churn rate (monthly, for subscription)
- New customer acquisition volume (monthly)
- ARPU / ACV (average revenue per user/contract value)
- Expansion/upsell rate (if applicable)
- Seasonality adjustments (if applicable)
```

**SaaS Revenue Formula (monthly):**
```
MRR(t) = MRR(t-1) 
        + New MRR (new customers × ARPU)
        + Expansion MRR
        - Churned MRR (MRR(t-1) × churn rate)
```

### 2. Expense Model (P&L)

**Expense categories to model:**

**COGS (Cost of Goods Sold):**
- Hosting/infrastructure (% of revenue or fixed)
- Payment processing fees (% of revenue)
- Customer support costs (headcount-driven)

**Operating Expenses:**
```
Sales & Marketing:
  - Paid acquisition (CAC budget)
  - Sales team salaries + commission
  - Marketing tools / events

Research & Development:
  - Engineering salaries (FTE × loaded cost)
  - Contractor/freelance dev costs
  - Tools and licenses

General & Administrative:
  - Executive salaries
  - Legal, accounting, compliance
  - Office / remote infrastructure
  - Insurance
```

**Headcount Planning Template:**
```
Role | Start Date | Monthly Salary | Benefits % | Total Loaded Cost
-----|------------|----------------|------------|------------------
CTO  | Jan 2026   | $15,000        | 25%        | $18,750
Eng  | Mar 2026   | $10,000        | 25%        | $12,500
...
```

### 3. P&L Statement

```
Revenue
  - COGS
= Gross Profit
  Gross Margin %

  - S&M Expense
  - R&D Expense
  - G&A Expense
= EBITDA
  EBITDA Margin %

  - Depreciation & Amortization
= EBIT

  - Interest Expense
= EBT (Earnings Before Tax)

  - Income Tax
= Net Income
```

### 4. Cash Flow Statement

**Three sections:**

```
Operating Activities:
  Net Income
  + D&A (non-cash add-back)
  ± Changes in Working Capital:
    - Accounts Receivable (increase = use of cash)
    - Accounts Payable (increase = source of cash)
    - Deferred Revenue (SaaS advance payments = source)
    - Prepaid Expenses

Investing Activities:
  - CapEx (equipment, IP capitalization)
  - Security deposits

Financing Activities:
  + Capital raises (equity funding rounds)
  + Debt proceeds
  - Debt repayments
  - Dividends (rare for startups)

= Net Change in Cash
+ Beginning Cash Balance
= Ending Cash Balance
```

### 5. Balance Sheet

```
ASSETS
Current Assets:
  Cash & Cash Equivalents  ← from Cash Flow ending balance
  Accounts Receivable
  Prepaid Expenses

Non-Current Assets:
  PP&E (net of depreciation)
  Intangibles / Capitalized Software

LIABILITIES
Current Liabilities:
  Accounts Payable
  Deferred Revenue
  Accrued Expenses

Non-Current Liabilities:
  Long-term Debt / Convertible Notes

EQUITY
  Paid-in Capital (cumulative fundraising)
  Retained Earnings (cumulative Net Income)
  Total Equity

CHECK: Assets = Liabilities + Equity ← must balance
```

---

## Burn Rate & Runway Calculator

### Gross Burn Rate
```
Gross Burn = Total Monthly Cash Outflows
           = COGS + OpEx (cash basis, pre-revenue)
```

### Net Burn Rate
```
Net Burn = Gross Burn - Revenue Collected
         = Monthly cash out - monthly cash in
```

### Runway
```
Runway (months) = Current Cash Balance ÷ Net Burn Rate

Example:
  Cash: $1,200,000
  Net Burn: $80,000/month
  Runway: 15 months
```

### Runway with Milestones
```
Milestone-adjusted runway = months until Series A, profitability, or breakeven
Break-even month = month where Net Burn = $0 (revenue ≥ expenses)
```

---

## Scenario Modeling

Build three scenarios with different assumptions:

| Assumption | Bear (Pessimistic) | Base (Expected) | Bull (Optimistic) |
|---|---|---|---|
| MoM Revenue Growth | 5% | 10% | 18% |
| Monthly Churn | 5% | 2.5% | 1% |
| CAC | $800 | $500 | $300 |
| Hiring pace | 50% of plan | 100% of plan | 120% of plan |
| Fundraise timing | +3 months delay | On schedule | -2 months early |

**Output for each scenario:**
- Runway (months from today)
- Break-even month
- Cash at end of model period
- Revenue at 12/24/36 months
- Key risk: what causes bear scenario?

---

## SaaS-Specific Metrics

When modeling SaaS businesses, include these unit economics:

```
LTV (Lifetime Value):
  LTV = ARPU / Monthly Churn Rate
  Example: $500 ARPU ÷ 2% churn = $25,000 LTV

CAC (Customer Acquisition Cost):
  CAC = Total S&M Spend / New Customers Acquired
  Example: $50,000 S&M ÷ 100 new customers = $500 CAC

LTV:CAC Ratio:
  Healthy = 3:1 minimum, 5:1+ strong
  $25,000 LTV ÷ $500 CAC = 50:1 (excellent)

CAC Payback Period:
  Payback = CAC / (ARPU × Gross Margin %)
  Example: $500 ÷ ($500 × 70%) = 1.4 months

Net Revenue Retention (NRR):
  NRR = (Beginning MRR + Expansion - Contraction - Churn) / Beginning MRR
  Target: >100% = expansion offsets churn
```

---

## Output Format

### Structured JSON for Export

When generating model output, produce structured data in this format:

```json
{
  "model_meta": {
    "company": "Acme SaaS Inc.",
    "model_date": "2026-03-15",
    "currency": "USD",
    "period": "monthly",
    "horizon_months": 36
  },
  "assumptions": {
    "starting_mrr": 50000,
    "mom_growth_rate": 0.10,
    "monthly_churn_rate": 0.025,
    "gross_margin_pct": 0.70,
    "starting_cash": 1200000,
    "monthly_burn_base": 95000
  },
  "scenarios": {
    "base": {
      "runway_months": 15,
      "breakeven_month": 18,
      "arr_12m": 960000,
      "arr_24m": 2400000,
      "cash_end_of_model": 340000
    },
    "bear": { ... },
    "bull": { ... }
  },
  "monthly_projections": [
    {
      "month": 1,
      "mrr": 55000,
      "gross_profit": 38500,
      "total_opex": 90000,
      "ebitda": -51500,
      "net_burn": 51500,
      "cash_balance": 1148500
    },
    ...
  ]
}
```

### Google Sheets Export Instructions

When producing a Sheets-ready model:
1. Output as CSV blocks per tab: `Revenue Model`, `P&L`, `Cash Flow`, `Balance Sheet`, `Scenarios`
2. Use formula notation where helpful: `=B2*(1+$B$1)` style references
3. Highlight assumption cells (color note: yellow = input, blue = formula)
4. Include a **Dashboard tab** with: Runway, MRR, Burn Rate, Gross Margin % as headline KPIs

---

## Step-by-Step Workflow

When a user asks to build a financial model:

### Step 1: Intake
Collect these inputs (ask if not provided):
```
□ Company name and stage (pre-seed, seed, Series A?)
□ Business model (SaaS, marketplace, services, etc.)
□ Current MRR / ARR or monthly revenue
□ Current cash balance
□ Monthly headcount and loaded cost estimate
□ Key growth assumption (growth rate, sales targets)
□ Model horizon (12, 24, or 36 months?)
□ Purpose (internal planning, investor diligence, board deck?)
```

### Step 2: Build Revenue Forecast
- Apply driver-based model for the business type
- Calculate monthly revenue for each period
- Show MRR bridge (new / expansion / churn)

### Step 3: Build Expense Model
- Headcount plan with hire dates
- COGS as % of revenue or fixed
- OpEx categories per above

### Step 4: Assemble 3 Statements
- P&L from revenue and expenses
- Cash flow from P&L + working capital changes
- Balance sheet from cumulative cash flow + equity raises

### Step 5: Burn & Runway
- Calculate net burn per month
- Project runway from current cash
- Identify break-even month

### Step 6: Scenario Analysis
- Run base, bear, bull with varied assumptions
- Summarize: how bad does it have to get before we run out of cash?

### Step 7: Output
- Structured JSON or CSV for export
- Narrative summary: key risks, milestones, funding gaps
- Investor-ready summary table

---

## Example Usage

**User:** "We have $800k in the bank, burning $65k/month net, growing MRR at 8% per month from $30k base. How long is our runway and when do we break even?"

**Sam's response:**

```
Runway Analysis:

Starting MRR: $30,000 | Net Burn: $65,000/month | Cash: $800,000

Month-by-month (base case, 8% MoM growth):
  Month 1:  MRR $32,400  | Burn est. $62,500  | Cash $737,500
  Month 6:  MRR $47,600  | Burn est. $47,000  | Cash $421,000 ← near breakeven
  Month 7:  MRR $51,400  | Burn est. $44,000  | Cash $377,000 → Cash flow positive
  
Runway: ~13 months before cash hits $0 (bear) / 18+ months if growth holds (base)
Break-even: Month 6-7 at ~$50k MRR (assuming costs stay relatively flat)

Key risks:
  - Growth slows to 4%: runway drops to 9 months
  - Unexpected hiring: 2 engineers = -$25k/month → runway -4 months
  
Recommendation: Fundraise at month 8-9 (Series A prep) or hit $60k MRR as proof point first.
```

---

## Integration Points

- **`crypto-tax-agent`** — for token/equity-based compensation modeling
- **`cap-table-manager`** — for equity dilution modeling alongside funding scenarios
- **`kpi-alert-system`** — set alerts when actual vs. model variance exceeds threshold
- **`qbo-automation`** — pull actuals from QuickBooks to compare against model
- **`report-generator`** — format model output into investor-ready PDF/deck

---

## Reference: Key Formulas Cheat Sheet

```
Gross Margin %     = (Revenue - COGS) / Revenue × 100
Net Burn           = Cash Out - Cash In (monthly)
Runway (months)    = Cash Balance / Net Burn
MoM Growth         = (Current MRR - Prior MRR) / Prior MRR × 100
ARR                = MRR × 12
LTV                = ARPU / Churn Rate
CAC Payback        = CAC / (ARPU × Gross Margin %)
Rule of 40         = Revenue Growth % + EBITDA Margin % (target ≥ 40 for SaaS)
Magic Number       = Net New ARR / Prior Quarter S&M Spend (target > 0.75)
```
