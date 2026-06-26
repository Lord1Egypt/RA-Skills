---
name: vendor-payment-optimizer
description: >
  Optimize vendor payment timing to maximize cash flow and capture early payment discounts.
  Analyzes open AP, scores discount opportunities (2/10 net 30, etc.), calculates annualized ROI of
  early payment vs. holding cash, generates payment priority queue, and flags late payment risk.
  Use when reviewing AP aging, deciding which invoices to pay early, or building a cash-efficient
  payment strategy. NOT for: paying invoices directly (use QBO or banking integrations), vendor
  contract negotiation (use contract-review-agent), or payroll processing (use payroll-gl-reconciliation).
version: 1.0.0
author: PrecisionLedger
tags:
  - accounts-payable
  - cash-flow
  - vendor-management
  - finance
  - optimization
---

# Vendor Payment Optimizer

Turns your AP aging report into a cash flow weapon. This skill analyzes open vendor invoices, calculates the true annualized ROI of early payment discounts, scores each invoice by priority, and generates an optimized payment queue — so you capture discounts worth capturing and hold cash when you shouldn't pay early.

---

## When to Use

**Trigger phrases:**
- "Which invoices should we pay early this week?"
- "We have a 2/10 net 30 — is it worth taking the discount?"
- "Optimize our AP payment schedule"
- "What's our cash position if we pay all invoices due this month?"
- "Flag any invoices about to go late"
- "Build a payment priority list from our AP aging"

**NOT for:**
- Actually sending payments or syncing to bank — use QBO or banking tools
- Vendor contract renegotiation — use `contract-review-agent`
- Payroll — use `payroll-gl-reconciliation`
- AR (receivables) — use `ar-collections-agent`
- Real-time QBO AP sync — use `qbo-automation` to pull data first, then feed here

---

## Core Concepts

### Early Payment Discount Math

The most common discount term is **2/10 net 30**: pay within 10 days, get 2% off; otherwise pay in 30 days.

**Annualized ROI of taking the discount:**

```
Annualized ROI = (Discount % / (1 - Discount %)) × (365 / (Net Days - Discount Days))

Example: 2/10 net 30
= (0.02 / 0.98) × (365 / 20)
= 0.0204 × 18.25
= 37.2% annualized ROI
```

**Decision rule:**
- If annualized ROI > your cost of capital (or opportunity cost of cash) → **take the discount**
- If annualized ROI < cost of capital → **hold cash, pay at net due date**
- Typical cost of capital for small business: 8–15%; most 2/10 net 30 discounts are worth taking

### Payment Priority Scoring

Score each invoice (0–100) using:

```
Score = (Discount ROI Weight × 40)
      + (Days-to-Late-Fee Weight × 30)
      + (Vendor Relationship Weight × 20)
      + (Invoice Size Weight × 10)
```

| Factor | High Score | Low Score |
|---|---|---|
| Discount ROI | >30% annualized | No discount available |
| Days to late | ≤3 days | >15 days |
| Vendor criticality | Key supplier, sole source | Easily replaceable |
| Invoice size | >$10k (high absolute $ saved) | <$500 |

---

## Workflow

### Step 1: AP Aging Input

Accept AP data in any of these formats:
- Pasted table from QBO AP Aging Summary report
- CSV export from accounting software
- Manual entry: vendor, invoice #, amount, due date, discount terms

**Minimum fields needed:**
```
Vendor Name | Invoice # | Amount | Invoice Date | Due Date | Terms | Discount Terms
```

**Example input:**
```
Vendor          | Inv #   | Amount    | Due Date   | Terms     | Discount
Acme Supplies   | INV-101 | $5,200    | 2026-03-22 | Net 30    | 2/10
Tech Services   | INV-205 | $12,000   | 2026-03-25 | Net 45    | None
Office Depot    | INV-089 | $840      | 2026-03-19 | Net 30    | 1/10
Contractor LLC  | INV-312 | $18,500   | 2026-04-01 | Net 60    | None
Cloud Hosting   | INV-410 | $3,200    | 2026-03-20 | Net 30    | 2/10
```

---

### Step 2: Discount Opportunity Analysis

For each invoice with discount terms, calculate:

```
DISCOUNT ANALYSIS — [Vendor] [Invoice #]

Invoice Amount:       $X,XXX
Discount Terms:       2/10 net 30
Discount Amount:      $XX.XX (2% of invoice)
Payment if early:     $X,XXX - $XX = $X,XXX
Days to discount exp: X days
Days to net due:      X days

Annualized ROI:       XX.X%
Recommendation:       TAKE / SKIP
Reason:               [ROI vs. cost of capital analysis]
Cash impact:          Pay $X,XXX today vs. $X,XXX in X days
```

---

### Step 3: Payment Priority Queue

Output a ranked payment list:

```
PAYMENT PRIORITY QUEUE — [Date]
Cash Available for AP This Week: $[amount] (enter or estimate)

RANK | VENDOR          | INV #   | AMOUNT   | DUE DATE   | DISCOUNT | SCORE | ACTION
-----|-----------------|---------|----------|------------|----------|-------|-------
  1  | Cloud Hosting   | INV-410 | $3,136*  | 2026-03-20 | 2/10 ✓  |  94   | PAY TODAY — discount exp. tomorrow
  2  | Office Depot    | INV-089 | $831.60* | 2026-03-19 | 1/10 ✓  |  91   | PAY TODAY — overdue risk
  3  | Acme Supplies   | INV-101 | $5,096*  | 2026-03-22 | 2/10 ✓  |  87   | PAY BY 3/22 for discount
  4  | Tech Services   | INV-205 | $12,000  | 2026-03-25 | None    |  62   | PAY BY DUE DATE
  5  | Contractor LLC  | INV-312 | $18,500  | 2026-04-01 | None    |  41   | HOLD — due in 15 days

* = discount-adjusted amount
```

---

### Step 4: Cash Flow Impact Summary

```
AP CASH FLOW SUMMARY

Total Open AP:              $39,740
Invoices due this week:     $21,236
Discount savings available: $186.40 (if all discounts taken)

Scenario A — Pay all discounts now + hold rest:
  Cash out this week:       $9,063.60
  Cash out by month-end:    $30,503.60
  Discount savings:         $186.40

Scenario B — Pay only what's overdue:
  Cash out this week:       $3,200
  Late fee risk:            Office Depot INV-089 (already at due date)

Scenario C — Pay everything now:
  Cash out today:           $39,553.60 (with all discounts)
  Cash freed from AP:       $39,740 obligation cleared

RECOMMENDATION: Scenario A — capture $186 in discounts, preserve $30k for week 2+
```

---

### Step 5: Late Payment Risk Flags

```
⚠️ LATE PAYMENT ALERTS

CRITICAL (0-2 days to due):
  - Office Depot INV-089: DUE TODAY — $840. Pay now or incur late fee.
  - Cloud Hosting INV-410: Due tomorrow — discount expires in 1 day.

WARNING (3-7 days to due):
  - Acme Supplies INV-101: Due in 4 days. Discount expires in 4 days.

WATCH (8-14 days):
  - Tech Services INV-205: Due in 8 days. No discount. Monitor cash.

NO URGENCY (15+ days):
  - Contractor LLC INV-312: Due in 15 days. Hold.
```

---

## Advanced Features

### Stretching Payment Terms (Ethically)

When cash is tight, identify which vendors are safe to pay at the tail end of net terms:

```
PAYMENT STRETCH ANALYSIS

Vendor: [Name]
Current terms: Net 30
Grace period (if any): 5 days (industry standard)
Relationship risk: LOW (long-term vendor, no prior issues)
Maximum safe payment date: Day 35 without relationship damage
Savings from stretching: [Interest on held cash for 5 days]

Vendor: [Name]
Current terms: Net 30
Relationship risk: HIGH (new vendor, critical sole-source supplier)
Recommendation: DO NOT STRETCH — pay on time
```

### Dynamic Discounting Offers

When you have excess cash and want to negotiate discounts with vendors who don't offer them:

```
DYNAMIC DISCOUNT PROPOSAL — [Vendor]

Current terms: Net 30, no discount
Proposed: Pay in 5 days for 1.5% discount
Your annualized cost: 12.2% (worth it at our hurdle rate)
Vendor benefit: Early cash, improved their cash flow
Script: "We'd love to settle INV-[X] today if you can extend a 1.5% early-pay discount."
```

### Vendor Spend Concentration Report

Identify AP risk concentration:

```
VENDOR CONCENTRATION — Last 90 Days

Top vendors by spend:
  1. [Vendor A]: $45,200 (38% of AP)  ← concentration risk
  2. [Vendor B]: $22,100 (18%)
  3. [Vendor C]: $15,800 (13%)
  4. All others: $37,000 (31%)

Risk flag: Single vendor >30% of AP = supply chain dependency
Recommendation: Qualify backup vendor for [Vendor A]'s category
```

---

## Output Formats

### Weekly AP Decision Brief (default)
Short, actionable: what to pay, by when, and why. Fits in one screen.

### Full AP Analysis Report
Comprehensive with all scenarios, discount math, vendor concentrations. For CFO/board review.

### CSV Payment Queue
For importing into QBO or banking batch payment tools:
```csv
Vendor,Invoice,AmountToPay,PayBy,DiscountTaken,Notes
Cloud Hosting,INV-410,3136.00,2026-03-19,Yes (2%),Discount expires tomorrow
Office Depot,INV-089,831.60,2026-03-19,Yes (1%),Due today
...
```

---

## Usage Examples

### Example 1: Quick Weekly Scan

**Input:** "Here's my AP aging. What should I pay this week? Cash available: $15k."

**Agent output:**
1. Parses AP data
2. Flags overdue and discount-expiring invoices
3. Calculates discount ROIs
4. Returns priority queue capped at $15k cash
5. Shows total discount savings captured

### Example 2: Discount Decision

**Input:** "We got an invoice for $8,500 with 2/10 net 30. We have cash. Should we take it?"

**Agent output:**
```
2/10 net 30 Discount Analysis — $8,500 invoice

Discount amount:    $170.00
Pay now:            $8,330
Hold 20 more days:  $8,500

Annualized ROI of taking discount: 37.2%
Your implied cost of capital:      ~10-12%

VERDICT: TAKE THE DISCOUNT ✓
You're earning 37.2% annualized by paying $8,330 today vs $8,500 in 20 days.
That beats any savings account or short-term investment.
```

### Example 3: Cash Constraint Scenario

**Input:** "I only have $5k available. I have $20k in AP due this week. What's the triage?"

**Agent output:**
1. Ranks invoices by criticality (late fee risk + vendor relationship)
2. Identifies which $5k subset to pay to avoid the most damage
3. Flags which vendors to contact proactively about delayed payment
4. Suggests script for requesting payment extension from lowest-risk vendors

---

## Integration Points

- **`qbo-automation`** — Pull live AP aging data from QuickBooks to feed this skill
- **`thirteen-week-cash-flow`** — Feed payment queue output into 13-week cash model
- **`ar-collections-agent`** — Pair AP optimization with AR acceleration for complete cash cycle management
- **`kpi-alert-system`** — Trigger alerts when AP aging shows invoices approaching due dates
- **`financial-analysis-agent`** — Use vendor spend data for cost analysis and budget variance

---

## Key Formulas Reference

```
Annualized Discount ROI = (d / (1-d)) × (365 / (net_days - discount_days))
  where d = discount rate (e.g., 0.02 for 2%)

Days Payable Outstanding (DPO) = (AP Balance / COGS) × Days in Period
  Healthy range: 30-60 days (industry-dependent)

Cash Conversion Cycle = DSO + DIO - DPO
  (Days Sales Outstanding + Days Inventory Outstanding - Days Payable Outstanding)
  Lower = more efficient cash cycle

Payment Stretch Savings = Invoice × (1 + risk_free_rate)^(stretch_days/365) - Invoice
  (Small but meaningful at scale)
```

---

## Privacy & Compliance Notes

- AP data contains sensitive vendor relationships and pricing — never share externally
- Payment timing decisions should be reviewed by Irfan for amounts >$10k
- Document all payment decisions with rationale for audit trail
- Never pay invoices directly from this skill — outputs are decision support only
