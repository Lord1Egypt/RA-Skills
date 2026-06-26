---
name: tax-deadline-calendar
description: >
  Tax deadline tracking and compliance calendar for businesses and individuals. Tracks federal and state
  tax filing deadlines, estimated tax payment due dates, payroll tax deposit schedules, W-2/1099 issuance
  deadlines, and extension request windows. Generates proactive reminders, compliance checklists, and
  penalty exposure calculations for missed deadlines. Use when a business owner, CFO, or accountant needs
  to know what's due and when, set up compliance reminders, or assess penalty risk for late filings.
  NOT for: preparing or filing tax returns (use a licensed CPA or PTIN-backed service), calculating actual
  tax liability, state nexus analysis beyond deadline awareness, or multi-jurisdiction sales tax filing.
version: 1.0.0
author: PrecisionLedger
tags:
  - tax
  - compliance
  - deadlines
  - accounting
  - payroll
  - calendar
  - IRS
---

# Tax Deadline Calendar Skill

Track federal and state tax filing deadlines, estimated tax payment windows, payroll deposit schedules,
and information return due dates. This skill helps Sam Ledger proactively manage compliance calendars,
generate reminders, and calculate penalty exposure for late filings.

---

## When to Use This Skill

**Trigger phrases:**
- "What taxes are due this month?"
- "When is [entity type]'s tax return due?"
- "Set up a tax deadline calendar for [client]"
- "When do I need to pay estimated taxes?"
- "What's the penalty for filing [form] late?"
- "Did we miss any tax deadlines?"
- "Extension deadline for [form]?"
- "Payroll tax deposit schedule for [company]"
- "1099 deadline this year?"
- "W-2 due date?"

**NOT for:**
- Preparing or filing tax returns — requires licensed CPA / PTIN
- Calculating actual tax liability (income, payroll, sales tax owed)
- Multi-state nexus analysis or sales tax registration advice
- State-specific filing requirements beyond major deadlines (consult state CPA)
- International tax deadlines (FBAR, Form 5471, etc.) — specialized skill needed
- Prior-year amended return deadlines beyond standard 3-year lookback guidance

---

## Federal Tax Deadline Reference

### Business Entity Filing Deadlines

| Entity Type | Form | Standard Deadline | Extended Deadline |
|---|---|---|---|
| S-Corporation | 1120-S | **March 15** | September 15 |
| Partnership | 1065 | **March 15** | September 15 |
| C-Corporation (Dec. 31 FYE) | 1120 | **April 15** | October 15 |
| C-Corporation (other FYE) | 1120 | 15th day of 4th month after FYE | 6-month extension |
| LLC (single-member, disregarded) | Schedule C / 1040 | **April 15** | October 15 |
| LLC (multi-member, partnership) | 1065 | **March 15** | September 15 |
| Non-profit | 990 / 990-EZ | **15th day of 5th month after FYE** | 6-month extension |
| Sole Proprietor | Schedule C / 1040 | **April 15** | October 15 |
| Trust / Estate | 1041 | **April 15** | September 30 |

> **Key rule:** S-Corps and Partnerships file March 15 so that K-1s reach shareholders/partners before
> the individual April 15 deadline. Missing March 15 cascades to missed individual returns.

### Individual Filing Deadlines

| Form | Standard Deadline | Extended Deadline | Notes |
|---|---|---|---|
| Individual (1040) | **April 15** | October 15 | Extension via Form 4868 |
| FBAR (FinCEN 114) | April 15 | October 15 | Auto-extended; no separate filing needed |
| FATCA (Form 8938) | April 15 (with 1040) | October 15 (with extension) | |
| Gift Tax (709) | April 15 | October 15 (with 1040 extension) | |

### Estimated Tax Payment Schedule (Federal)

Applies to: individuals with self-employment income, pass-through owners, sole proprietors.

| Payment | Tax Year | Due Date |
|---|---|---|
| Q1 | January 1 – March 31 | **April 15** |
| Q2 | April 1 – May 31 | **June 15** |
| Q3 | June 1 – August 31 | **September 15** |
| Q4 | September 1 – December 31 | **January 15 (following year)** |

> If April 15 or other dates fall on a weekend or holiday, the deadline shifts to the next business day.

**Safe harbor thresholds (avoid underpayment penalty):**
```
Option A: Pay 100% of prior-year tax liability (110% if prior-year AGI > $150,000)
Option B: Pay 90% of current-year actual tax liability
Use whichever results in lower required payment.
```

**Underpayment penalty rate:** Federal funds rate + 3% (IRS adjusts quarterly). Currently ~7-8% annualized.

---

## Payroll Tax Deadlines

### Federal Payroll Deposits

**Deposit schedule depends on lookback period (July 1 – June 30 of prior year):**

| Lookback Period Tax Liability | Deposit Schedule | Deposit Deadline |
|---|---|---|
| ≤ $50,000 | Monthly depositor | 15th of following month |
| > $50,000 | Semi-weekly depositor | Wed–Fri payroll → following Wednesday; Mon–Tue payroll → following Friday |
| < $2,500/quarter | Quarterly depositor | With Form 941 filing |
| $100,000+ in single day | Next-day depositor | Next banking day — no exceptions |

**Key payroll tax forms and deadlines:**

| Form | What | Deadline |
|---|---|---|
| Form 941 | Quarterly payroll tax return | Last day of month following quarter end (Apr 30, Jul 31, Oct 31, Jan 31) |
| Form 940 | Annual FUTA return | **January 31** (or Feb 10 if all deposits made on time) |
| Form W-2 | Wage statements to employees | **January 31** |
| Form W-3 | Transmittal to SSA | **January 31** |
| Form W-2 corrections (W-2c) | Corrected wages | ASAP; penalties increase with delay |

### Form 941 Quarterly Calendar (2026)

| Quarter | Period | Filing Deadline | Deposit Deadline (monthly) |
|---|---|---|---|
| Q1 | Jan–Mar | **April 30, 2026** | 15th of each following month |
| Q2 | Apr–Jun | **July 31, 2026** | 15th of each following month |
| Q3 | Jul–Sep | **October 31, 2026** | 15th of each following month |
| Q4 | Oct–Dec | **January 31, 2027** | 15th of each following month |

---

## Information Return Deadlines

### 1099 Series

| Form | Purpose | Recipient Copy | IRS Paper | IRS E-File |
|---|---|---|---|---|
| 1099-NEC | Non-employee compensation ≥ $600 | **January 31** | **January 31** | **January 31** |
| 1099-MISC | Rents, royalties, other income ≥ $600 | January 31 | February 28 | March 31 |
| 1099-INT | Interest ≥ $10 | January 31 | February 28 | March 31 |
| 1099-DIV | Dividends ≥ $10 | January 31 | February 28 | March 31 |
| 1099-R | Retirement distributions | January 31 | February 28 | March 31 |
| 1099-K | Payment card transactions ≥ $5,000 (2024 threshold) | January 31 | February 28 | March 31 |
| 1099-B | Brokerage proceeds | February 15 | February 28 | March 31 |

> **E-file mandate:** Filers with 10+ information returns (combined all types) MUST e-file starting 2024.
> The 10-return threshold replaced the prior 250-return threshold.

### W-2 Deadlines
- **January 31**: Send to employees AND file Copy A with SSA (paper AND e-file — same deadline)
- **No extension available** for W-2 filing with SSA without Form 8809

---

## Extension Filing Reference

| Form | What | How to File | Extends To |
|---|---|---|---|
| Form 4868 | Individual 1040 extension | File by April 15 | October 15 |
| Form 7004 | Business return extension (1120, 1065, 1120-S) | File by original deadline | +6 months |
| Form 8868 | Non-profit 990 extension | File by original deadline | +6 months |
| Form 8809 | Information return extension (W-2, 1099) | File by original deadline | +30 days (hardship only) |

> **Critical: Extensions extend the TIME TO FILE, not the time to pay.**
> Tax owed must still be estimated and paid by the original deadline or interest + penalties accrue.

---

## Penalty Exposure Calculator

### Failure to File (FTF)

```
FTF Penalty = 5% of unpaid tax per month (or fraction of month) late
Maximum: 25% of unpaid tax
Minimum: greater of $450 (2024) or 100% of tax due if >60 days late

formula:
months_late = ceiling((filing_date - original_due_date).days / 30)
ftf_penalty = min(unpaid_tax * 0.05 * months_late, unpaid_tax * 0.25)
if months_late > 2:
    ftf_penalty = max(ftf_penalty, min(450, unpaid_tax))
```

### Failure to Pay (FTP)

```
FTP Penalty = 0.5% of unpaid tax per month (reduced to 0.25% if on installment agreement)
Maximum: 25% of unpaid tax
Continues to accrue after filing if balance remains unpaid

formula:
months_unpaid = ceiling((payment_date - original_due_date).days / 30)
ftp_penalty = min(unpaid_tax * 0.005 * months_unpaid, unpaid_tax * 0.25)
```

### Combined FTF + FTP (when both apply)

```
Combined monthly rate: 5% - 0.5% credit for FTP = 4.5% per month on FTF
After 5 months: FTF maxes at 25%, FTP continues at 0.5%/month until 25% max

Total max combined penalty: 47.5% of unpaid tax (25% FTF + 22.5% FTP at max)
```

### Information Return Penalties (1099/W-2)

```
Tier 1: Filed within 30 days of deadline → $60/return (max $220,000/year; $75K for small biz)
Tier 2: Filed by August 1 → $120/return (max $660,000/year; $200K for small biz)
Tier 3: Filed after August 1 or not filed → $310/return (max $3.78M/year; $588K for small biz)
Intentional disregard: $630/return with no cap
```

**Small business definition:** Average annual gross receipts ≤ $5M for 3 prior tax years.

### Payroll Tax Failure to Deposit (FTD)

```
1-5 days late:   2% of undeposited tax
6-15 days late:  5% of undeposited tax
16+ days late:  10% of undeposited tax
Demand from IRS: 15% of undeposited tax
```

---

## 2026 Key Dates Calendar

```
JANUARY 2026
  Jan 15  — Q4 2025 estimated tax payment (individuals)
  Jan 31  — W-2s to employees
  Jan 31  — 1099-NEC to recipients AND to IRS
  Jan 31  — Form 940 (FUTA annual return)
  Jan 31  — Form 941 Q4 2025

FEBRUARY 2026
  Feb 15  — 1099-B to recipients (brokerage)
  Feb 28  — 1099-MISC / 1099-INT / 1099-DIV to IRS (paper filers)

MARCH 2026
  Mar 15  — S-Corp (1120-S) and Partnership (1065) returns DUE
  Mar 15  — S-Corp / Partnership extension deadline (Form 7004)
  Mar 31  — 1099-MISC / 1099-INT / 1099-DIV to IRS (e-filers)

APRIL 2026
  Apr 15  — Individual (1040) return DUE
  Apr 15  — C-Corp (1120, Dec 31 FYE) return DUE
  Apr 15  — Individual extension deadline (Form 4868)
  Apr 15  — Q1 2026 estimated tax payment
  Apr 30  — Form 941 Q1 2026

JUNE 2026
  Jun 15  — Q2 2026 estimated tax payment

JULY 2026
  Jul 31  — Form 941 Q2 2026

SEPTEMBER 2026
  Sep 15  — S-Corp / Partnership extended returns DUE (if extended)
  Sep 15  — Q3 2026 estimated tax payment
  Sep 30  — Trust/Estate (1041) extended return DUE

OCTOBER 2026
  Oct 15  — Individual (1040) extended return DUE
  Oct 15  — C-Corp (1120) extended return DUE
  Oct 31  — Form 941 Q3 2026

JANUARY 2027
  Jan 15  — Q4 2026 estimated tax payment
  Jan 31  — Form 941 Q4 2026 / W-2s / 1099-NECs
```

---

## Compliance Checklist Generator

When a user asks for a client compliance calendar, generate a checklist:

**Inputs required:**
```
□ Entity type (S-Corp, C-Corp, Partnership, LLC, Individual, Non-profit)
□ Tax year end (calendar year = Dec 31, or fiscal year end date)
□ Number of employees (for payroll obligations)
□ Number of 1099 vendors (for information return obligations)
□ State(s) of operation
□ Whether entity makes estimated tax payments
```

**Output: Client Compliance Checklist**

```
CLIENT: [Name] | ENTITY: [Type] | TAX YEAR: 2025

INFORMATION RETURNS (January–March):
  [ ] Jan 31: Send W-2s to [X] employees
  [ ] Jan 31: Send 1099-NECs to [X] contractors
  [ ] Jan 31: File W-3 + W-2 copies with SSA
  [ ] Jan 31: File 1099-NECs with IRS
  [ ] Mar 31: File remaining 1099s with IRS (if e-filing)

ENTITY RETURN:
  [ ] [March 15 / April 15]: File [1120-S / 1065 / 1040 / 1120]
  [ ] [Same date]: Pay any balance due (extension ≠ extension to pay)
  [ ] If extending: File Form [4868 / 7004] by original deadline

ESTIMATED TAXES (if applicable):
  [ ] Apr 15, Jun 15, Sep 15, Jan 15 — $[amount] each installment

PAYROLL TAXES (if employees):
  [ ] Monthly/semi-weekly deposits per schedule
  [ ] Apr 30 / Jul 31 / Oct 31 / Jan 31: Quarterly Form 941
  [ ] Jan 31: Annual Form 940 (FUTA)

NOTES:
  - State return deadlines: [list state-specific deadlines here]
  - Any pending elections or forms: [e.g., S-election, 1045, etc.]
```

---

## State Tax Deadline Overview

Most states conform to federal deadlines, but key exceptions:

| State | Notable Difference |
|---|---|
| California | FTB: C-Corp April 15; S-Corp March 15; Individual April 15 (or next business day) |
| New York | Conforms to federal dates; NYC adds separate NYC-4S/NYC-4 for C-Corps |
| Texas | No state income tax; franchise tax (TX No Tax Due/05-163) due May 15 |
| Florida | C-Corp F-1120 due: April 1 (or 4.5 months after FYE) |
| Illinois | Conforms to federal with IL-specific extensions |
| Pennsylvania | Conforms to federal for individuals; RCT-101 for C-Corps April 15 |

> **Always verify:** State deadlines change. Use this as a starting framework, not the definitive source.
> Confirm with state revenue department or state-licensed CPA.

---

## Reminder Setup (OpenClaw Cron)

To set up automated deadline reminders via cron:

```
Recommended lead times:
  - 30 days before: "Coming up" awareness notice
  - 14 days before: Action required — gather documents
  - 7 days before:  Final prep — return should be in progress
  - 1 day before:   Due tomorrow — confirm filed/extension submitted
```

**Sample cron payload (S-Corp March 15 deadline):**
```json
{
  "schedule": { "kind": "at", "at": "2026-03-01T09:00:00-06:00" },
  "payload": {
    "kind": "systemEvent",
    "text": "TAX REMINDER: S-Corp/Partnership returns (Form 1120-S / 1065) due March 15 — 14 days away. Confirm K-1s being prepared, extension decisions made, and balance due estimated."
  }
}
```

---

## Penalty Abatement Notes

**First-time penalty abatement (FTA):**
- Available for FTF, FTP, and FTD penalties
- Requires: clean compliance history (no penalties in prior 3 years) + all returns filed
- Request via Form 843 or by calling the IRS
- IRS grants FTA liberally — always ask before paying FTF/FTP penalties

**Reasonable cause abatement:**
- Available when failure was due to circumstances beyond taxpayer's control
- Document: what happened, why it prevented compliance, steps taken to comply ASAP
- Examples: natural disaster, serious illness, reliance on erroneous IRS advice

---

## Integration Points

- **`qbo-automation`** — Pull payroll and vendor payment data to identify 1099 filing obligations
- **`crypto-tax-agent`** — Crypto tax events feed into individual 1040 and Schedule D deadlines
- **`kpi-alert-system`** — Trigger compliance calendar reminders via cron/alert system
- **`compliance-monitor`** — Broader compliance tracking beyond tax deadlines
- **`startup-financial-model`** — Estimated tax payments flow from projected taxable income model

---

## Quick Reference: Most Common Deadline Misses

1. **1099-NEC January 31** — Most commonly missed information return (same day recipient AND IRS)
2. **S-Corp March 15** — Founders forget pass-through entities file earlier than individuals
3. **Estimated Q1 taxes April 15** — Individual owners skip this and face underpayment penalty
4. **Form 940 January 31** — FUTA often forgotten since it's only annual
5. **Extension ≠ payment extension** — Filing an extension without paying causes FTP penalties to accrue
