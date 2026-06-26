---
name: SCF Deep Analysis
slug: scf-deep-analysis
version: 1.0.0
description: >
  Controller-level Statement of Cash Flows deep analysis for QBO-connected
  clients. Computes CF Quality Ratio, Free Cash Flow, working capital movement
  drivers, 3-month rolling averages, GL drill-down for flagged accounts, and
  plain-English controller findings with HIGH/MEDIUM/LOW urgency action
  proposals. Outputs a 7-tab Excel workbook.
tags:
  - finance
  - accounting
  - cash-flow
  - qbo
  - excel

negative_boundaries:
  - Quick period-over-period CF snapshot → use scf-quick-compare instead
  - P&L variance analysis → use pl-deep-analysis skill
  - Budget vs. actual → use budget-vs-actual skill
  - 13-week rolling cash forecast → use cash-flow-forecast skill
---

# SCF Deep Analysis — SKILL.md

## What This Skill Does

Runs a controller-level Statement of Cash Flows deep analysis for a QBO-connected client. Extends the SCF Quick Compare with:

- **CF Quality Ratio**: Operating CF ÷ Net Income (>1.0 = cash-backed quality earnings)
- **Free Cash Flow**: Operating CF − CapEx (pulled from investing section)
- **Working Capital Movement**: AR, AP, Inventory, Prepaid — which WC components drove operating CF changes
- **3-Month Rolling Averages**: Per-account and per-section CF trend baseline
- **GL Drill-Down**: Vendor-level transaction detail for every flagged CF account
- **Controller Findings**: Plain-English narratives with urgency — "Operating CF decreased 15% because AR increased $8K (collections lagging) while AP decreased $4K (paying faster)"
- **Action Proposals**: Specific, actionable recommendations (HIGH / MEDIUM / LOW urgency)
- **CDC**: Tracks what changed in CF since last run

**Output**: Excel workbook with 7 tabs:
`Summary | Detail | ⚠ Flags | GL Drill-Down | Working Capital Movement | Controller Findings | CDC Log`

## When To Use

- Monthly close: controller-level CF review beyond the Quick Compare
- Client with CF concerns (declining operating CF, negative FCF, low CF quality)
- Board prep: need to explain *why* cash changed this period
- Internal review: identify AR collection problems, AP timing, capex overruns

## When NOT To Use

- Quick period-over-period CF snapshot → use `scf-quick-compare.py` instead
- P&L variance analysis → use `pl-deep-analysis.py`
- Budget vs. actual → use `budget-vs-actual` skill
- Non-QBO clients (no integration) → use `bank-reconciliation` skill

## Prerequisites

- QBO client connected for the slug
- QBO auth token configured
- `openpyxl` installed: `pip install openpyxl`
- Node.js available on PATH

## Script Location

```
scripts/pipelines/scf-deep-analysis.py
```

## Usage

```bash
# Basic: current month vs. prior month (auto-calculated)
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug my-client \
  --current-start 2026-03-01 --current-end 2026-03-31

# Explicit prior period
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug my-client \
  --current-start 2026-02-01 --current-end 2026-02-28 \
  --prior-start 2026-01-01 --prior-end 2026-01-31

# YTD vs prior YTD
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug my-client --ytd --year 2026

# Skip GL drill-down (faster — use when GL is unavailable or not needed)
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug my-client \
  --current-start 2026-03-01 --current-end 2026-03-31 --skip-gl

# Custom output directory
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug glowlabs \
  --current-start 2026-03-01 --current-end 2026-03-31 \
  --out ~/Desktop/reports

# Sandbox mode (QBO sandbox environment)
python3 scripts/pipelines/scf-deep-analysis.py \
  --slug glowlabs \
  --current-start 2026-03-01 --current-end 2026-03-31 --sandbox
```

## Arguments

| Argument | Required | Description |
|---|---|---|
| `--slug` | ✅ | Company slug (must match qbo-client connection) |
| `--current-start` | ✅* | Current period start YYYY-MM-DD |
| `--current-end` | ✅* | Current period end YYYY-MM-DD |
| `--prior-start` | ❌ | Prior period start — auto-calculated if omitted |
| `--prior-end` | ❌ | Prior period end — auto-calculated if omitted |
| `--ytd` | ❌ | YTD mode: Jan 1 → end of last completed month |
| `--year` | ❌ | Year for --ytd (default: current year) |
| `--skip-gl` | ❌ | Skip GL drill-down (faster run) |
| `--out` | ❌ | Output directory (default: ~/Desktop) |
| `--sandbox` | ❌ | Use QBO sandbox environment |

*Required unless `--ytd` is used.

## Pipeline Steps (8 Steps)

1. **Pull CF** — current + prior period CF from QBO via `report {slug} cf`
2. **Pull P&L** — current + prior period P&L for Net Income extraction (CF quality ratio)
3. **Rolling Averages** — pull 3 prior months of CF; compute per-account and per-section averages
4. **CDC** — compare current flat map vs. `.cache/scf-deep-analysis/{slug}.json`
5. **CF Quality + FCF** — compute ratio + extract CapEx from investing section
6. **Working Capital Movement** — classify AR / AP / Inventory / Prepaid from operating section
7. **Variance + Flags + GL** — flag material variances (≥10% or ≥$2,500); pull GL for flagged accounts
8. **Controller Findings** — generate narrative findings with urgency and action proposals

## Output: Excel Workbook (7 Tabs)

### Tab 1: Summary
- Section totals: Operating / Investing / Financing / Net Change / Beginning / Ending Cash
- vs. prior period + 3-month rolling average
- CF Quality Ratio block (with color coding)
- Free Cash Flow calculation
- Controller Findings summary (top 8 findings, HIGH in red)

### Tab 2: Detail
- Every CF line item with prior period, current period, $ variance, % variance, rolling avg
- Section-grouped with color bands (Operating = blue, Investing = yellow, Financing = purple)
- F/U column (Favorable = more cash, Unfavorable = less cash)

### Tab 3: ⚠ Flags
- Material variances only: ≥10% change OR ≥$2,500 absolute delta
- Includes rolling avg comparison
- Sorted by absolute dollar variance

### Tab 4: GL Drill-Down
- Vendor-level transaction detail for every flagged account
- Top 3 vendor contributors shown in sub-header per account
- Max 50 transactions per account
- Skipped if `--skip-gl` flag used

### Tab 5: Working Capital Movement
- AR, AP, Inventory, Prepaid, Other WC — current vs. prior vs. delta
- Cash Impact column (Source / Use)
- Plain-English analysis note per component (e.g., "AR increased $8K — collections lagging sales")
- Total WC impact row

### Tab 6: Controller Findings
- Full narrative findings sorted HIGH → MEDIUM → LOW
- Detail / GL attribution per finding
- Specific recommended action per finding
- $ Impact column

### Tab 7: CDC Log
- All accounts/line items that changed vs. last cached run
- Prior value, current value, $ delta, % change, note (New / Changed / Removed)
- Color coded: green = cash increased, red = cash decreased

## Cache

```
.cache/scf-deep-analysis/{slug}.json
```

Stored after each run. Contains:
- `flat_map` — all CF line items and amounts
- `totals` — section totals (operating, investing, financing, net_change, ending_cash)
- `cf_quality` — CF quality label
- `fcf` — Free Cash Flow amount
- `net_income` — Net Income for the period
- `saved_at` — ISO date of last run

## Key Metrics Explained

### CF Quality Ratio
```
Operating CF / Net Income
```
| Ratio | Quality | Color |
|---|---|---|
| ≥ 1.0x | ✅ Quality Earnings — cash-backed | Green |
| 0.5–1.0x | ⚠ Adequate — partially cash-backed | Yellow |
| < 0.5x | ⚠ Low Quality — accrual-heavy | Orange |
| < 0 | 🔴 Cash Drain — cash negative despite reported profit | Red |

### Free Cash Flow
```
FCF = Operating CF + CapEx (CapEx is negative outflow, so this subtracts it)
```
CapEx detected by keyword matching in investing section (equipment, property, asset, capital expenditure, etc.)

### Working Capital Movement (in Operating section)
- **AR change** (negative = AR grew = cash used; positive = AR shrank = cash released)
- **AP change** (positive = AP grew = cash deferred; negative = AP shrank = cash paid out)
- **Inventory change** (negative = inventory built = cash used; positive = inventory drawn = cash released)
- **Prepaid change** (negative = more prepaid = cash used; positive = prepaid expensed = cash released)

## Materiality Thresholds

- **Percent threshold**: ≥10% change in any CF line item
- **Absolute threshold**: ≥$2,500 absolute variance
- **Both thresholds** checked — either triggers a flag

## Safety Rules

- **Read-only**: No writes to QBO — only pulls reports
- **All Decimal math**: No floating-point for financial calculations
- **Disclaimer footer**: Controller Findings tab includes audit disclaimer
- **Cache separation**: Uses `.cache/scf-deep-analysis/` — separate from scf-quick-compare cache

## Related Pipelines

| Pipeline | Use When |
|---|---|
| `scf-quick-compare.py` | Quick CF period-over-period snapshot (4 tabs, no GL) |
| `scf-deep-analysis.py` | Controller-level CF with GL drill-down, CF quality, FCF, WC movement |
| `pl-deep-analysis.py` | Same depth for P&L (not CF) |
| `budget-builder.py` | Build annual CF budget / BvA |
