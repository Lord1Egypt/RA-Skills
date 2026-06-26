---
name: SCF Quick Compare
slug: scf-quick-compare
version: 1.0.0
description: >
  Period-over-period variance analysis on the Statement of Cash Flows pulled
  from QuickBooks Online. Outputs a 4-tab Excel workbook: Summary, Detail,
  Flags, CDC Log. Covers Operating, Investing, and Financing sections with
  balance validation and SCF-specific analysis notes on flagged items.
tags:
  - finance
  - accounting
  - cash-flow
  - qbo
  - excel

negative_boundaries:
  - 13-week rolling cash flow forecasting → use cash-flow-forecast skill
  - P&L variance analysis → use pl-quick-compare skill
  - AR aging / collections tracking → use ar-collections skill
  - Balance sheet analysis → use bs-quick-compare skill
  - Deep CF quality analysis → use scf-deep-analysis skill
---

# SCF Quick Compare — Skill

## What This Skill Does

Runs a period-over-period variance analysis on the **Statement of Cash Flows (SCF)** pulled directly from QuickBooks Online. Outputs a 4-tab Excel workbook: Summary | Detail | Flags | CDC Log.

Mirrors the `pl-quick-compare` pattern exactly but for the Cash Flow Statement — Operating / Investing / Financing sections, balance validation, and SCF-specific analysis notes on flagged items.

## When to Use

**Use when:**
- A client needs month-over-month or YTD cash flow variance analysis
- Reviewing SCF as part of monthly close deliverables
- Investigating a material shift in operating, investing, or financing cash flows
- Client asks: "why did our cash position change?" or "what drove the cash swing?"

**NOT for:**
- 13-week rolling cash flow forecasting → use `cash-flow-forecast.py`
- P&L variance analysis → use `pl-quick-compare.py`
- AR aging / collections tracking → use `ar-collections`
- Balance sheet analysis (not cash flows)

## Script Location

```
scripts/pipelines/scf-quick-compare.py
```

## Requirements

- `pip install openpyxl` (already installed in workspace)
- Node.js QBO client with valid auth token
- QBO credentials configured

## Usage

```bash
# Current month vs. prior month (auto-detects prior)
python3 scripts/pipelines/scf-quick-compare.py \
    --slug my-client \
    --current-start 2026-03-01 --current-end 2026-03-31

# Explicit prior period
python3 scripts/pipelines/scf-quick-compare.py \
    --slug my-client \
    --current-start 2026-02-01 --current-end 2026-02-28 \
    --prior-start 2026-01-01 --prior-end 2026-01-31

# YTD vs prior YTD (Jan 1 → end of last completed month)
python3 scripts/pipelines/scf-quick-compare.py \
    --slug my-client --ytd --year 2026

# Custom output directory
python3 scripts/pipelines/scf-quick-compare.py \
    --slug my-client \
    --current-start 2026-03-01 --current-end 2026-03-31 \
    --out ~/Desktop/reports

# Sandbox mode (QBO sandbox environment)
python3 scripts/pipelines/scf-quick-compare.py \
    --slug my-client \
    --current-start 2026-03-01 --current-end 2026-03-31 \
    --sandbox
```

## Arguments

| Flag | Required | Description |
|------|----------|-------------|
| `--slug` | ✅ | Company slug (must be connected in qbo-client) |
| `--current-start` | ✅* | Current period start date (YYYY-MM-DD) |
| `--current-end` | ✅* | Current period end date (YYYY-MM-DD) |
| `--prior-start` | ❌ | Prior period start (auto-shifts 1 month if omitted) |
| `--prior-end` | ❌ | Prior period end (auto-shifts 1 month if omitted) |
| `--ytd` | ✅* | YTD mode (alternative to explicit dates) |
| `--year` | ❌ | Year for --ytd (default: current year) |
| `--out` | ❌ | Output directory (default: ~/Desktop) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

*Either `--current-start`/`--current-end` OR `--ytd` is required.

## Output

Excel file: `SCF_QuickCompare_{slug}_{period}.xlsx` saved to Desktop (or `--out` directory).

### Tab 1: Summary
- Operating / Investing / Financing section totals (current vs prior, $ variance, % variance, F/U)
- Net Change in Cash
- Beginning and Ending Cash Balance
- SCF validation: `Operating + Investing + Financing = Net Change` and `Beginning + Net Change = Ending Cash`

### Tab 2: Detail
- Every SCF line item with hierarchy preserved
- Prior period | Current period | $ Variance | % Variance | F/U label
- Color-coded by section (Operating = blue, Investing = gold, Financing = purple)

### Tab 3: ⚠ Flags
- Material variances: **≥10% change OR ≥$2,500 absolute**
- Analysis note for each flagged item — plain-English explanation of what the variance likely means
- SCF-specific interpretation (AR buildup, D&A add-back, capex, debt repayment, distributions)

### Tab 4: CDC Log
- Change Data Capture: compares current SCF flat map against last cached run
- First run: full snapshot saved (no deltas)
- Subsequent runs: shows exactly what line items changed since last run
- Cache location: `.cache/scf-quick-compare/{slug}.json`

## SCF Logic

### Section Classification
The parser classifies each QBO CF row into sections by keyword matching on row names:
- **Operating**: net income, depreciation, amortization, AR, AP, inventory, prepaid, accrued, working capital
- **Investing**: equipment, property, asset, purchase, capex, investing
- **Financing**: loan, line of credit, note payable, distribution, equity, contribution, SAFE, financing
- **Net Change**: net change, net increase/decrease in cash
- **Beginning/Ending Cash**: beginning, ending (balance check rows)

### Variance F/U Logic
For SCF: **positive delta = Favorable** (more cash generated/retained vs prior).
This is directionally correct for all sections — the goal is always more net cash.

### Balance Validation
```
Net Change = Operating + Investing + Financing      (≤$1 tolerance)
Ending Cash = Beginning Cash + Net Change           (≤$1 tolerance)
```
Both checks run on both periods and displayed in the Summary tab.

### YTD Mode
`--ytd`: Current = Jan 1 → end of last completed month. Prior = same date range in prior year.
Example: run on March 17, 2026 → Current = Jan 1 – Feb 28, 2026 | Prior = Jan 1 – Feb 28, 2025.

## Analysis Notes (Flags Tab)

The Flags tab includes an **Analysis Note** column with SCF-specific interpretation for each material variance:

| Item | Note logic |
|------|-----------|
| Net Income | Profitability driver — directs to P&L for root cause |
| Depreciation / Amortization | Non-cash add-back explanation |
| Accounts Receivable | AR buildup (cash tied up) vs. collection acceleration |
| Accounts Payable | AP extension (cash benefit) vs. paydown (cash use) |
| Inventory | Buildup (cash use) vs. drawdown (cash release) |
| Equipment / CapEx | Strategic capex alert — verify against growth plan |
| Loan proceeds / repayments | Debt structure activity — review debt schedule |
| Distributions | Owner draw alert — verify cash availability |
| SAFE / Equity | Cap table activity — verify with investor records |
| Net Change | Overall cash generation summary |

## CDC Cache

```
.cache/scf-quick-compare/{slug}.json
```

Stores the flat map of all SCF line names → amounts for the most recent run. On re-run, diffs against the prior cache and shows exactly what changed. Useful for catching mid-month QBO adjustments or reconciliation entries.

## Decimal Math

All calculations use Python `Decimal` with `ROUND_HALF_UP` — no floating-point rounding errors in financial outputs.

