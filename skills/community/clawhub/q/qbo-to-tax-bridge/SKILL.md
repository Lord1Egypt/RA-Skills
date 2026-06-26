---
name: qbo-to-tax-bridge
description: >
  Map QuickBooks Online (QBO) chart of accounts and transaction categories to IRS tax schedules
  (Schedule C, E, F, 1120S, 1120, 1065, and more). Generate trial balance exports, produce
  tax-ready workpapers, track crypto asset cost basis within QBO, and bridge bookkeeping data
  to tax preparation workflows. PTIN-backed advisory context included. Use when: (1) preparing
  year-end workpapers from QBO data, (2) mapping QBO categories to IRS schedule line items,
  (3) identifying reclassification needs before tax filing, (4) generating crypto cost basis
  reports from QBO transactions. NOT for: filing tax returns directly, providing legal tax
  advice, replacing a licensed CPA or EA review, or accessing QBO without proper credentials.
metadata:
  openclaw:
    tags:
      - accounting
      - tax
      - quickbooks
      - irs
      - compliance
      - crypto
      - workpapers
---

# QBO → Tax Bridge

Maps QuickBooks Online bookkeeping data to IRS tax schedules and generates tax-ready workpapers.

---

## Core Capabilities

1. **QBO Category → IRS Schedule Mapping** — Translate chart of accounts to Schedule C, E, F, 1120S, 1120, 1065 line items
2. **Trial Balance → Workpaper Generation** — Export QBO trial balance and format into tax-ready supporting schedules
3. **Reclassification Identification** — Flag misclassified transactions that need adjustment before filing
4. **Crypto Cost Basis Tracking** — Calculate FIFO/LIFO/HIFO cost basis for crypto assets recorded in QBO
5. **Schedule Line Mapping Reference** — Authoritative line-by-line crosswalk tables

---

## Workflow

### Step 1 — Export QBO Trial Balance

1. In QBO: **Reports → Trial Balance**
2. Set date range to the full tax year (Jan 1 – Dec 31)
3. Customize → Show Non-Zero rows only
4. Export as **Excel or CSV**
5. Also export: **Profit & Loss (by month)** and **Balance Sheet (year-end)**

```
QBO Export Path:
Reports > Standard > Trial Balance > Export (Excel icon, top right)
```

---

### Step 2 — Entity + Schedule Selection

Identify the filing entity type to determine the correct IRS schedule:

| Entity Type | Primary Schedule | Supporting |
|---|---|---|
| Sole Proprietor / Single-Member LLC | Schedule C (Form 1040) | SE, 4562 |
| Rental Activity | Schedule E (Page 1) | 4562, 8582 |
| Farm | Schedule F | 4562, SE |
| S-Corporation | Form 1120-S + K-1 | 4562, 4797 |
| C-Corporation | Form 1120 | 4562, 4797 |
| Partnership / Multi-Member LLC | Form 1065 + K-1 | 4562, 4797 |

---

### Step 3 — Schedule C Mapping (Sole Proprietors)

**Income Accounts → Schedule C, Part I**

| QBO Account Name (Common) | Schedule C Line | Notes |
|---|---|---|
| Sales / Revenue | Line 1 (Gross receipts) | Exclude returns |
| Returns and Allowances | Line 2 | Deducted from gross |
| Cost of Goods Sold | Line 4 (via Part III) | COGS detail required |
| Other Income | Line 6 | Non-operating income |

**Expense Accounts → Schedule C, Part II**

| QBO Account Name | Sch C Line | IRS Description |
|---|---|---|
| Advertising | Line 8 | Advertising |
| Bank Charges | Line 27a (Other) | Bank service charges |
| Car & Truck Expenses | Line 9 | Requires Form 4562 or actual method |
| Commissions | Line 10 | Commissions and fees |
| Contract Labor | Line 11 | Non-employee compensation (1099-NEC trigger) |
| Depreciation | Line 13 | Form 4562 required |
| Dues & Subscriptions | Line 27a | Other expenses |
| Employee Benefits | Line 14 | Health insurance, retirement |
| Insurance (Business) | Line 15 | Not health insurance here |
| Interest - Mortgage | Line 16a | On business real property |
| Interest - Other | Line 16b | Business loans |
| Legal & Professional | Line 17 | Attorney, CPA, consultants |
| Meals (Business) | Line 24b | 50% deductible — apply haircut |
| Office Expense | Line 18 | Supplies vs. equipment distinction |
| Rent (Equipment) | Line 20a | Equipment rentals |
| Rent (Property) | Line 20b | Office/workspace rent |
| Repairs & Maintenance | Line 21 | Maintenance only; improvements → capitalize |
| Payroll Taxes | Line 23 | Employer portion FICA/FUTA |
| Wages (Employees) | Line 26 | W-2 wages (not owner draws) |
| Utilities | Line 25 | Business portion only |
| Home Office | Line 30 | Form 8829 required |
| Travel | Line 24a | Business travel (not commuting) |
| Telephone | Line 27a | Business portion of phone/internet |
| Software Subscriptions | Line 27a | Business software |

**⚠ Meals Haircut:** Apply 50% reduction to QBO Meals balance before reporting on Sch C Line 24b.

---

### Step 4 — Schedule E Mapping (Rental)

**Per-Property Tracking Required**

| QBO Account | Schedule E Line | Notes |
|---|---|---|
| Rental Income | Line 3 | Gross rents received |
| Advertising (Rental) | Line 5 | Vacancy advertising |
| Auto & Travel (Rental) | Line 6 | Property management travel |
| Cleaning & Maintenance | Line 7 | Cleaning between tenants |
| Commissions | Line 8 | Leasing agent fees |
| Insurance (Rental) | Line 9 | Property insurance |
| Legal & Professional (Rental) | Line 10 | Eviction, lease drafting |
| Management Fees | Line 11 | Property management company |
| Mortgage Interest (Rental) | Line 12 | From 1098 |
| Other Interest (Rental) | Line 13 | HELOC on rental, etc. |
| Repairs (Rental) | Line 14 | Repairs only; improvements → capitalize |
| Supplies (Rental) | Line 15 | Small supplies |
| Property Taxes | Line 16 | Real estate taxes |
| Utilities (Rental) | Line 17 | Landlord-paid utilities |
| Depreciation (Rental) | Line 18 | Form 4562; 27.5-yr residential |
| Other Expenses | Line 19 | HOA, snow removal, etc. |

---

### Step 5 — Form 1120-S / S-Corp Mapping

**Income → Form 1120-S, Page 1**

| QBO Account | 1120-S Line | Notes |
|---|---|---|
| Gross Receipts / Sales | Line 1a | Net of returns |
| Cost of Goods Sold | Line 2 | Schedule A detail |
| Other Income | Line 5 | Interest, rents, royalties |

**Deductions → Form 1120-S, Lines 7-19**

| QBO Account | 1120-S Line |
|---|---|
| Compensation of Officers | Line 7 |
| Salaries & Wages | Line 8 |
| Repairs & Maintenance | Line 9 |
| Bad Debts | Line 10 |
| Rents | Line 11 |
| Taxes & Licenses | Line 12 |
| Interest | Line 13 |
| Depreciation | Line 14 |
| Depletion | Line 15 |
| Advertising | Line 16 |
| Employee Benefit Programs | Line 17 |
| Other Deductions | Line 19 |

**K-1 Pass-Through Items (Schedule K)**

| QBO Account | K-1 Box | Description |
|---|---|---|
| Ordinary Business Income | Box 1 | Net income from operations |
| Interest Income | Box 4 | Taxable interest |
| Dividends | Box 5a/5b | Ordinary vs. qualified |
| Net Rental Income | Box 2 | Rental real estate |
| Section 179 | Box 11 | Must track separately |
| Charitable Contributions | Box 12a | Separately stated |
| Meals (50%) | Box 16C | Must track and separate |

---

### Step 6 — Crypto Asset Cost Basis (QBO-Tracked)

**QBO Setup for Crypto:**
- Create a separate **Other Current Asset** account per crypto type (e.g., "Bitcoin Holdings", "Ethereum Holdings")
- Record purchases as asset debits; sales as credits with gain/loss to **Other Income** or **Other Expense**

**Cost Basis Methods:**

| Method | Description | IRS Compliance |
|---|---|---|
| FIFO | First purchased = first sold | Default, IRS-accepted |
| LIFO | Last purchased = first sold | Accepted but must be consistent |
| HIFO | Highest cost = first sold | Accepted; minimizes gains |
| Specific ID | Choose exact lot | Requires documentation |

**Crypto Workpaper Template (per asset):**

```
Asset: Bitcoin (BTC)
QBO Account: Bitcoin Holdings

Date       | Type     | Units    | Price    | Cost Basis | Proceeds | Gain/Loss
-----------|----------|----------|----------|------------|----------|----------
2025-02-14 | Purchase | 0.50000  | $48,000  | $24,000    | —        | —
2025-06-01 | Purchase | 0.25000  | $62,000  | $15,500    | —        | —
2025-09-15 | Sale     | 0.25000  | $71,000  | $12,000*   | $17,750  | $5,750 ST
2025-11-30 | Sale     | 0.25000  | $95,000  | $12,000*   | $23,750  | $11,750 LT

*FIFO basis from 2025-02-14 purchase

Short-term gains: $5,750 → Schedule D, Part I / Form 8949 (held < 1 year)
Long-term gains: $11,750 → Schedule D, Part II / Form 8949 (held > 1 year)
```

**QBO Journal Entry for Crypto Sale:**
```
DR  Checking / USD Received         $23,750
CR  Bitcoin Holdings (cost)         $12,000
CR  Long-Term Capital Gain          $11,750
```

**DeFi / Staking Income:**
- Record staking rewards as **Other Income** at FMV on date received
- Taxed as ordinary income (not capital gains) at receipt
- Future sale creates capital gain/loss from FMV basis

---

### Step 7 — Reclassification Identification

Run these checks against QBO trial balance before workpaper finalization:

**Common Misclassifications:**

| Issue | Check | Fix |
|---|---|---|
| Capital improvements coded as repairs | Single transaction > $2,500 in Repairs & Maint. | Reclassify to Fixed Assets; depreciate |
| Owner draws in payroll | Distributions in wage accounts | Move to Owner's Draw / Equity |
| Personal expenses in business | Mixed personal charges | Reclassify to Due from Owner / Shareholder |
| Meals coded as Entertainment | Pre-2018 habit; Entertainment 0% deductible | Separate Meals (50%) from Entertainment (0%) |
| Loan proceeds in Income | Deposit from business loan coded as revenue | Reclassify to Liability account |
| Prepaid expenses expensed | Subscriptions paid for future periods | Pro-rate; book prepaid asset |
| Security deposits as income | Refundable deposits in revenue | Reclassify to Liability |

**Threshold Rules:**
- **Section 179 / Bonus Depreciation:** Fixed assets ≥ $2,500 (safe harbor) → track in 4562
- **1099-NEC Trigger:** Any contractor receiving ≥ $600/year → verify W-9 on file
- **Meals Documentation:** Receipt + business purpose required for deductibility

---

### Step 8 — Trial Balance → Workpaper Output Format

**Workpaper Header (required per SSVS standards):**
```
Client:          [Business Name]
EIN:             XX-XXXXXXX
Tax Year:        2025
Prepared By:     [Preparer Name], PTIN: PXXXXXXXXX
Reviewed By:     [Reviewer Name]
Date Prepared:   [Date]
Purpose:         Supporting schedule for [Form/Schedule]
```

**Standard Workpaper Tabs (Excel):**
1. `TB` — Trial Balance (direct QBO export, unadjusted)
2. `AJE` — Adjusting Journal Entries (reclassifications, accruals)
3. `ATB` — Adjusted Trial Balance (TB + AJE)
4. `Sch-C` or `1120-S` — Schedule mapping with line references
5. `Fixed-Assets` — 4562 depreciation schedule
6. `Crypto` — Cost basis tracker (if applicable)
7. `1099` — Contractor payment summary for 1099-NEC filing

---

## Quick Reference: Common QBO → IRS Line Crosswalk

```
QBO Account              → IRS Form/Line
─────────────────────────────────────────
Advertising              → Sch C L8 / 1120-S L16
Bank Charges             → Sch C L27a (other)
Car & Truck              → Sch C L9 (+ 4562 or actual)
Commissions              → Sch C L10
Contract Labor           → Sch C L11 (1099-NEC!)
Depreciation             → Sch C L13 / 1120-S L14
Dues & Subscriptions     → Sch C L27a
Health Insurance (self)  → 1040 L17 (not Sch C)
Insurance (business)     → Sch C L15
Interest (mortgage)      → Sch C L16a
Interest (other)         → Sch C L16b
Legal & Professional     → Sch C L17
Meals (50%)              → Sch C L24b (50% of QBO balance)
Office Expense           → Sch C L18
Payroll Taxes (ER)       → Sch C L23
Rent (equipment)         → Sch C L20a
Rent (space)             → Sch C L20b
Repairs                  → Sch C L21
Travel                   → Sch C L24a
Utilities                → Sch C L25
Wages (W-2)              → Sch C L26
Home Office              → Sch C L30 (+ 8829)
```

---

## Negative Boundaries (When NOT to Use)

- ❌ **Filing tax returns** — This skill maps and prepares workpapers; actual filing requires licensed tax software (Drake, UltraTax, ProConnect) and a licensed preparer
- ❌ **Legal tax advice** — Specific tax strategies, elections, or planning require CPA/EA/attorney opinion
- ❌ **Replacing CPA review** — Workpapers always require professional review before filing
- ❌ **Non-QBO accounting systems** — Mappings assume QBO chart of accounts; adapt for Xero, Wave, or FreshBooks
- ❌ **International tax (non-US)** — IRS schedules only; no VAT, GST, or foreign jurisdiction guidance
- ❌ **State tax returns** — State conformity varies; this skill covers federal only
- ❌ **Real-time QBO API access** — This is a workpaper and mapping skill, not a live QBO integration (see qbo-automation skill for API work)

---

## Examples

### Example 1 — Sole Prop Workpaper Summary
```
Client: Jane Smith Photography, LLC (SMLLC)
EIN: 87-1234567 | Tax Year: 2025 | Schedule C

QBO Trial Balance (Adjusted):
  Revenue                  $142,500
  COGS (equipment rental)  ($18,200)
  Gross Profit             $124,300

Schedule C Expenses:
  L8  Advertising          $3,400
  L9  Car & Truck          $4,200   (actual method, Form 4562 attached)
  L13 Depreciation         $2,800   (camera equipment, Form 4562)
  L15 Insurance            $1,200
  L17 Legal & Prof         $2,500
  L18 Office               $890
  L24b Meals               $1,450   (QBO balance $2,900 × 50%)
  L25 Utilities            $600
  L27a Other               $1,100   (software subscriptions)
  Total Expenses           $18,140

Net Profit (Line 31):      $106,160
SE Tax (Sch SE):           $14,993
```

### Example 2 — Crypto Reclassification
```
Issue found: Client coded $15,000 ETH sale proceeds as "Sales Revenue"
Fix: Reclassify to Long-Term Capital Gain (held 14 months)
AJE: DR Sales Revenue $15,000 / CR LT Capital Gain $15,000
     DR LT Capital Gain $8,200 / CR Cost Basis (ETH Holdings) $8,200
Net: $6,800 LTCG → Form 8949, Part II → Schedule D, Line 8
```

### Example 3 — S-Corp K-1 Prep
```
Form 1120-S → Schedule K Items to Separately State:
  Box 1: Ordinary Income        $87,400
  Box 4: Interest Income        $320
  Box 12a: Charitable Contrib   $2,500
  Box 16C: Meals Disallowed     $1,800 (50% of $3,600 meals)
  
Per-shareholder K-1 (50% ownership):
  Box 1: $43,700
  Box 4: $160
  Box 12a: $1,250
  Box 16C: $900
```

---

## Related Skills

- **qbo-automation** — QBO API integration, bank rules, chart of accounts setup
- **crypto-tax-agent** — Advanced crypto tax calculations, DeFi, NFTs, multi-chain
- **financial-analysis-agent** — Ratio analysis, variance reporting, management reporting
