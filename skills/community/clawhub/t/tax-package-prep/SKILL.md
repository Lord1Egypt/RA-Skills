---
name: Tax Package Preparation
slug: tax-package-prep
version: 1.0.0
description: >
  Year-end tax package preparation pipeline for QBO-connected clients. Generates a 9-tab
  Excel workbook: Tax Summary, Income, Expenses, Depreciation, 1099s, State Nexus, Crypto
  (Form 8949), Checklist, and CDC. Reads client SOP for entity type, crypto wallet, vehicle,
  home office, and FBAR flags. Maps every line item to IRS form and schedule codes.
tags:
  - finance
  - accounting
  - tax
  - qbo
  - excel
  - year-end
license: MIT
---

# Tax Package Preparation

Prepare a complete year-end tax package for client filing. Pulls full-year financial data from QBO, reads the client SOP for entity configuration, and generates all tax-ready schedules with IRS form mapping.

## When To Use

Use when:
- Client needs year-end tax package for CPA/tax preparer
- Generating income/expense schedules with IRS line mapping
- Identifying 1099 vendors (paid >$600)
- Flagging crypto exposure (Form 8949) from SOP wallet address
- Checking for FBAR requirement (FinCEN 114)
- Detecting multi-state nexus risk
- Building carryforward analysis (NOL, Sec 179, charitable)
- Tracking year-over-year tax position changes (CDC)

**NOT for:**
- Monthly close → use `month-end-close.py`
- Bank reconciliation → use `bank-reconciliation.py`
- P&L variance analysis → use `pl-deep-analysis.py`
- Payroll tax returns (941, 940, W-2s) — separate workflow
- Actual tax return preparation (CPA reviews all output before filing)

## Quick Start

```bash
# Standard run — pulls full year from QBO
python3 scripts/pipelines/tax-package-prep.py --slug my-client --year 2025

# Skip GL drill (faster, less vendor detail)
python3 scripts/pipelines/tax-package-prep.py --slug my-client --year 2025 --skip-gl

# Custom output directory
python3 scripts/pipelines/tax-package-prep.py --slug my-client --year 2025 --out ~/Desktop/tax-2025

# QBO sandbox
python3 scripts/pipelines/tax-package-prep.py --slug my-client --year 2025 --sandbox
```

## Requirements

```bash
pip install openpyxl
# QBO auth token must already be configured
```

## Output: 9-Tab Excel Workbook

| Tab | Contents |
|-----|----------|
| **Tax Summary** | Entity info, key tax metrics, special flags (crypto/FBAR/vehicle/home office), SOP watch items |
| **Income Schedule** | Revenue by category with IRS Sch C / 1120 / 1065 line mapping |
| **Expense Schedule** | Expenses with IRS line mapping, 50% meal limit applied, deductible amounts |
| **Depreciation** | Fixed assets from GL + BS, MACRS / Section 179 / Straight-Line detection |
| **1099 Vendors** | Vendors paid >$600, form type (NEC/MISC), corp exemption flag, W-9 action list |
| **State Nexus** | Multi-state revenue/expense pattern detection, HIGH/MEDIUM/LOW risk rating |
| **Crypto Flag** | Form 8949 flag, wallet address, FBAR assessment, action item checklist |
| **Checklist** | READY / NEEDS INPUT / MISSING for every tax package item |
| **CDC Log** | Year-over-year income and expense position changes |

## SOP Integration

The pipeline reads `clients/{slug}/sop.md` to auto-configure:

| SOP Signal | What It Triggers |
|------------|-----------------|
| `S-Corp` / `1120-S` | Entity = S-Corp, officer W-2 flag, K-1 checklist item |
| `C-Corp` / `1120` | Entity = C-Corp, E&P tracking, charitable 10% limit |
| `Partnership` / `1065` | K-1 prep checklist, partner basis tracking |
| `0x[wallet]` (ETH address) | Crypto flag, Form 8949, wallet address in output |
| `crypto` / `bitcoin` / `defi` | Crypto flag, Form 8949 required |
| `vehicle` / `mileage` | Vehicle schedule, mileage log requirement |
| `home office` / `Form 8829` | Home office flag, sq footage action items |
| `SAFE` / `convertible note` | SAFE treatment watch item |
| `foreign` / `offshore` | FBAR flag, FinCEN 114 action |
| `NOL` / `loss carryforward` | Carryforward analysis |
| `Section 179 carry` | Section 179 carryover check |
| `interest expense` | Watch item: verify deductibility |

## IRS Schedule Mapping

### Expense Categories (auto-mapped)
- Advertising → Sch C Ln 8 / 1120 Ln 22 / 1065 Ln 21a
- Vehicle/Auto → Sch C Ln 9 (standard mileage or actual)
- Contract Labor → Sch C Ln 11 (triggers 1099-NEC scan)
- Depreciation → Sch C Ln 13 / Form 4562
- Interest → Sch C Ln 16 / 1120 Ln 18
- Legal/Professional → Sch C Ln 17
- Wages → Sch C Ln 26 / 1120 Ln 13
- Meals/Entertainment → Sch C Ln 24 (50% limit applied automatically)
- Home Office → Sch C Form 8829

### Income Categories (auto-mapped)
- Service Revenue → Sch C Ln 1 / 1120 Ln 1a
- Product Sales → Sch C Ln 1 / 1120 Ln 1a
- Interest Income → Sch B
- Crypto → Form 8949 / Sch D

## 1099 Vendor Logic

Scans all GL expense accounts and aggregates by vendor name:
- **Include:** Vendors paid ≥$600 via check/ACH/wire (not credit card)
- **1099-NEC:** Contractors, consultants, attorneys, freelancers
- **1099-MISC:** Rent, royalties, medical payments
- **Exempt:** C-Corps and S-Corps (except attorneys and medical providers)
- **Flag:** "Inc", "Corp", "LLC" in vendor name → verify entity type
- **Deadline:** January 31 (1099-NEC), January 31/March 31 (1099-MISC)

## State Nexus Detection

Scans GL memos, vendor names, and account names for US state indicators:
- **HIGH risk:** 5+ indicators in a state → likely nexus, recommend registration review
- **MEDIUM risk:** 2-4 indicators → investigate further
- **LOW risk:** 1 indicator → monitor

Physical nexus (employees, office), economic nexus ($100K revenue threshold), and payroll nexus are all flagged.

## Crypto / FBAR Logic

**Crypto:**
- Detects from SOP wallet address (0x... pattern) or crypto keywords in GL
- Flags Form 8949 and Schedule D requirement
- Detects staking (ordinary income) vs. sales (capital gains) from GL memos
- Action list includes exchange export, cost basis calculation, software recommendation

**FBAR (FinCEN 114):**
- Triggers on foreign account keywords in GL or SOP
- FBAR threshold: $10,000 aggregate foreign account balance at any point in the year
- Also checks Form 8938 (FATCA) thresholds
- Deadline: April 15 with automatic extension to October 15

## CDC Cache

Each run saves a snapshot to `.cache/tax-package-prep/{slug}-{year}.json`.  
The next year's run computes year-over-year deltas for income and expense accounts.  
CDC events are shown in the **CDC Log** tab sorted by absolute dollar change.

## Depreciation Detection

Scans GL and Balance Sheet for:
- Fixed asset account names (equipment, vehicle, computer, furniture, leasehold)
- Accumulated depreciation account names
- Memo keywords: "section 179", "MACRS", "bonus depreciation", "straight-line"
- P&L depreciation expense line items

Output includes: account, year-end balance, period activity, detected method, Section 179 flag.

## Estimated Tax Payments

Scans GL for estimated tax payment entries:
- Account names: "estimated tax", "quarterly payment", "1040-es", "1120-w"
- Memo keywords: same
- Classifies by quarter (Q1-Q4) based on payment date
- Flags missing quarters → client must verify with bank statements

## Checklist Status Definitions

| Status | Meaning |
|--------|---------|
| ✅ READY | Data found in QBO — no client action needed |
| ⚠ NEEDS INPUT | Requires additional documentation from client |
| ❌ MISSING | Not found — QBO pull failed or data doesn't exist |

## File Locations

- **Pipeline:** `scripts/pipelines/tax-package-prep.py`
- **CDC Cache:** `.cache/tax-package-prep/{slug}-{year}.json`
- **Output:** `~/Desktop/TaxPackage_{slug}_{year}.xlsx` (or `--out` dir)
- **Skill:** `skills/tax-package-prep/SKILL.md`

## Notes

- All financial math uses Python `Decimal` — no float rounding errors
- Output is for CPA/tax preparer review — not a filed return
- Vehicle deduction: requires mileage log from client; pipeline flags but cannot calculate
- Home office: requires square footage from client; pipeline flags Form 8829 requirement
- Entity-specific items (K-1s, basis tracking, E&P) are flagged as checklist items, not generated
- Carryforward amounts require prior-year return — pipeline flags for review but cannot pull from prior returns
