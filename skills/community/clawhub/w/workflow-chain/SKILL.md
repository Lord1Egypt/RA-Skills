---
name: workflow-chain
description: >
  Chain multiple pipeline scripts into a single sequential or parallel workflow.
  Acts as a "playlist" for PrecisionLedger pipeline scripts. Use when a task
  requires multiple pipelines in sequence (e.g., "full close + analysis package
  for Paulson") or when building reusable workflow templates for recurring
  multi-step client work. Reads the pipeline manifest and client SOPs to
  auto-detect which pipelines apply. Can run ad-hoc chains or saved templates.
  NOT for: single-pipeline tasks (use the specific skill), non-pipeline work
  (email, web search, content creation), or tasks that don't involve QBO data
  or pipeline scripts.
license: MIT
metadata:
  openclaw:
    emoji: "⛓️"
    negative_boundaries:
      - Do NOT use for single-pipeline tasks; use the specific pipeline skill instead
      - Do NOT use for non-pipeline work like email, web search, or content creation
      - Do NOT use when the task does not involve QBO data, pipeline scripts, or multi-step orchestration
---

# Workflow Chain — Multi-Pipeline Orchestrator

Chain multiple PrecisionLedger pipeline scripts into a single coordinated workflow.
Think of it as a "playlist" for pipeline scripts — run them in sequence or parallel,
with data flowing between steps.

---

## Trigger

Use this skill when:
- User says "run full close and analysis", "complete financial package", "run all pipelines for [client]"
- A task clearly requires 2+ pipeline scripts in sequence
- User says "chain", "workflow", "run everything", "full suite"
- Building a reusable workflow template for a client
- Need to coordinate parallel pipeline execution with a merge step

Do NOT use for:
- Single pipeline tasks → use the specific skill (pl-quick-compare, month-end-close, etc.)
- Non-pipeline work → email, web search, content creation
- Tasks without QBO data or pipeline scripts

---

## Architecture

### Pipeline Registry

All available pipelines live in `scripts/pipelines/` with a manifest at `scripts/pipelines/manifest.json`.

Current production pipelines (19 scripts, all have argparse):

| Pipeline | Script | Typical Order |
|----------|--------|---------------|
| pl-quick-compare | pl-quick-compare.py | 1 (income statement first) |
| pl-deep-analysis | pl-deep-analysis.py | 2 (after quick compare flags) |
| bs-quick-compare | bs-quick-compare.py | 3 (balance sheet) |
| bs-deep-analysis | bs-deep-analysis.py | 4 (after BS flags) |
| scf-quick-compare | scf-quick-compare.py | 5 (cash flow) |
| scf-deep-analysis | scf-deep-analysis.py | 6 (after SCF flags) |
| financial-ratios | financial-ratios.py | 7 (cross-statement ratios) |
| bank-reconciliation | bank-reconciliation.py | parallel with above |
| payroll-reconciliation | payroll-reconciliation.py | parallel with above |
| ar-collections | ar-collections.py | parallel (if client has AR) |
| budget-builder | budget-builder.py | ad-hoc |
| cash-flow-forecast | cash-flow-forecast.py | after close |
| client-dashboard | client-dashboard.py | final (needs all data) |
| doc-ingestion | doc-ingestion.py | pre-close |
| document-ingestion | document-ingestion.py | pre-close |
| financial-package | financial-package.py | standalone TTM package |
| month-end-close | month-end-close.py | orchestrates close checklist |
| tax-package-prep | tax-package-prep.py | year-end only |
| vendor-compliance-1099 | vendor-compliance-1099.py | year-end only |

### Common Arguments (all pipelines share these)

```
--slug <client-slug>        QBO company identifier (required)
--start YYYY-MM-DD          Period start
--end YYYY-MM-DD            Period end
--out <directory>            Output directory (default: ~/Desktop)
--sandbox                   Use QBO sandbox
```

---

## Workflow Execution

### Step 1: Identify the Task

Parse the user's request to determine:
1. **Client** (slug) — from name/alias matching against `clients/*/sop.md`
2. **Period** — month, quarter, or year
3. **Scope** — which pipelines are needed

### Step 2: Build the Chain

Read the client's SOP to determine which pipelines apply:
- Does the client have AR? → include ar-collections
- Does the client have payroll? → include payroll-reconciliation
- Is this year-end? → include tax-package-prep, vendor-compliance-1099
- Is this a close? → include month-end-close as the anchor

### Step 3: Determine Execution Order

Pipelines have natural dependencies:

```
Layer 0 (Pre-Close — parallel):
  doc-ingestion
  bank-reconciliation
  payroll-reconciliation

Layer 1 (Close):
  month-end-close (reads outputs from Layer 0)

Layer 2 (Analysis — parallel):
  pl-quick-compare
  bs-quick-compare
  scf-quick-compare

Layer 3 (Deep Analysis — parallel, depends on Layer 2 flags):
  pl-deep-analysis (only if PL flags > 0)
  bs-deep-analysis (only if BS flags > 0)
  scf-deep-analysis (only if SCF flags > 0)

Layer 4 (Cross-Statement):
  financial-ratios
  cash-flow-forecast

Layer 5 (Delivery):
  client-dashboard
  financial-package
```

### Step 4: Execute

For each layer:
1. Run all pipelines in that layer (parallel where possible via sub-agents)
2. Check exit codes — if any pipeline fails, log the error and continue (don't block the chain)
3. Pass shared arguments (slug, dates, output dir) to each pipeline
4. Collect outputs (Excel files, JSON caches, manifests)

### Step 5: Report

After all layers complete, produce a summary:
- Which pipelines ran ✅
- Which failed ❌ (with error)
- Which were skipped ⏭️ (not applicable per SOP)
- Output file locations
- Total execution time

---

## Pre-Built Templates

### Template: Full Monthly Close
```
Layers: 0 → 1 → 2 → 3 → 4 → 5
Pipelines: bank-rec → close → PL/BS/SCF quick → deep (if flagged) → ratios → dashboard
Trigger: "full close for [client]", "complete close [month]"
```

### Template: Quick Analysis Package  
```
Layers: 2 → 4 → 5
Pipelines: PL/BS/SCF quick compare → ratios → dashboard
Trigger: "quick analysis for [client]", "variance package [month]"
```

### Template: Year-End Tax Package
```
Layers: 0 → 1 → 2 → tax-specific
Pipelines: bank-rec → close → PL → tax-package-prep → vendor-1099
Trigger: "tax package for [client]", "year-end prep [year]"
```

### Template: Deep Dive (Single Statement)
```
Layers: quick → deep
Pipelines: [statement]-quick-compare → [statement]-deep-analysis
Trigger: "deep dive P&L", "analyze balance sheet in detail"
```

### Template: Financial Package (TTM)
```
Layers: single
Pipelines: financial-package.py (self-contained TTM generator)
Trigger: "financial package", "TTM statements"
```

---

## Example Usage

- "Run the full monthly close and analysis package for Acme for March 2026."
- "Chain PL, BS, and SCF quick compare, then build the dashboard."
- "Create a reusable year-end tax workflow for this client."

## Execution Commands

```bash
# Common pattern for all pipelines
SCRIPTS=~/.openclaw/workspace/scripts/pipelines
SLUG="my-client"
MONTH_START="2026-03-01"
MONTH_END="2026-03-31"
OUT=~/Desktop/close-$SLUG-$(date +%Y%m)

# Layer 0 (parallel)
python3 $SCRIPTS/bank-reconciliation.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT &
python3 $SCRIPTS/payroll-reconciliation.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT &
wait

# Layer 1
python3 $SCRIPTS/month-end-close.py --slug $SLUG --month ${MONTH_START:0:7} --out $OUT

# Layer 2 (parallel)
python3 $SCRIPTS/pl-quick-compare.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT &
python3 $SCRIPTS/bs-quick-compare.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT &
python3 $SCRIPTS/scf-quick-compare.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT &
wait

# Layer 3 (conditional)
# Only run deep analysis if quick compare flagged material items
python3 $SCRIPTS/pl-deep-analysis.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT
python3 $SCRIPTS/bs-deep-analysis.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT
python3 $SCRIPTS/scf-deep-analysis.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT

# Layer 4
python3 $SCRIPTS/financial-ratios.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT
python3 $SCRIPTS/cash-flow-forecast.py --slug $SLUG --out $OUT

# Layer 5
python3 $SCRIPTS/client-dashboard.py --slug $SLUG --start $MONTH_START --end $MONTH_END --out $OUT
```

---

## Client SOP Integration

Before running any chain, read `clients/{slug}/sop.md` to check:

1. **Which reports are relevant** — not every client needs AR aging or payroll rec
2. **Special instructions** — some clients have non-standard periods or reporting requirements
3. **Key financial characteristics** — informs which deep dives to prioritize
4. **Schedule** — when the client expects deliverables

The SOP is the authority. If the SOP says "no AR aging" (like SB Paulson — POS collection), skip ar-collections even in a full close chain.

---

## Error Handling

- **Pipeline fails:** Log error, mark as ❌, continue chain. Don't block subsequent layers unless the failed pipeline is a hard dependency.
- **QBO token expired:** Run `node integrations/qbo-client/bin/qbo connect <slug>` to refresh. Auto-detected by 401 response.
- **Missing data:** Some pipelines produce empty results for new clients. That's OK — the dashboard handles nulls gracefully.
- **Timeout:** Each pipeline has a 5-minute max. If exceeded, kill and mark as timed out.

---

## Output Convention

All chain outputs go to a single directory:
```
~/Desktop/close-{slug}-{YYYYMM}/
├── PLCompare_{slug}_*.xlsx
├── BSCompare_{slug}_*.xlsx
├── SCFCompare_{slug}_*.xlsx
├── PLDeep_{slug}_*.xlsx
├── BSDeep_{slug}_*.xlsx
├── SCFDeep_{slug}_*.xlsx
├── FinancialRatios_{slug}_*.xlsx
├── BankRec_{slug}_*.xlsx
├── PayrollRec_{slug}_*.xlsx
├── ClientDashboard_{slug}_*.xlsx
├── CashFlow_{slug}_*.xlsx
├── chain-summary.json          ← workflow metadata
└── chain-log.txt               ← execution log
```
