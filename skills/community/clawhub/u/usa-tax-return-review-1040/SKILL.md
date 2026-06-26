---
name: form-1040-review
description: Review U.S. individual income tax returns (Form 1040/1040-SR) for the most recent tax year, compare major return items against current-year tax rules, check consistency across historical returns when multiple years are provided, generate a standalone DOCX risk register, and estimate audit likelihood from return content. Use when tasks involve 1040 compliance review, multi-year consistency analysis, tax-law validation, or audit-risk assessment.
---

# Form 1040 Review

## Overview

Run a structured review of normalized Form 1040 data for the latest tax year in the provided set. Produce three artifacts: a detailed findings JSON file, a markdown summary, and a separate DOCX risk report listing major items and related risks.

## Quick Start

1. Prepare normalized input JSON using [references/input_schema.json](references/input_schema.json).
2. Confirm current-law parameters in [references/current_tax_law_2025.json](references/current_tax_law_2025.json) before use.
3. Run:

```bash
python scripts/review_1040.py --input <normalized_returns.json> --output-dir output/form-1040-review
```

4. Review outputs:
- `review_summary.md`
- `review_findings.json`
- `form-1040-risk-report.docx`

## Workflow

### 1. Identify the current return
- Select the highest `tax_year` in the input as the current return.
- Treat all prior years as historical comparison returns.

### 2. Run current-year law checks
- Validate internal arithmetic and line-to-line relationships.
- Compare major current-year items to law parameters:
- Standard deduction by filing status and age/blind additions.
- Regular-rate tax computation when no preferential income is present.
- Child Tax Credit and ACTC limits.
- Self-employment tax and Additional Medicare tax thresholds.

### 3. Run multi-year consistency checks
- Compare current return against the most recent prior year.
- Flag large year-over-year movement in wages, AGI, taxable income, credits, payments, and refund/amount owed.
- Flag filing-status and dependent-count shifts for explanation.

### 4. Produce risk outputs
- Generate a structured findings file (`review_findings.json`).
- Generate a human-readable summary (`review_summary.md`).
- Generate a standalone DOCX risk register (`form-1040-risk-report.docx`) that lists each major item, severity, observations, and recommended documentation.
- Produce an audit-likelihood estimate based on weighted findings and return complexity.

## Inputs

Use the normalized schema in [references/input_schema.json](references/input_schema.json). At minimum, include:
- `tax_year`
- `filing_status`
- `major_items` for core 1040 lines (AGI, deduction, taxable income, tax, payments, refund/amount owed)

Use [references/major_items_reference.md](references/major_items_reference.md) for canonical key mapping.

## Law Source Discipline

- Update [references/current_tax_law_2025.json](references/current_tax_law_2025.json) when the filing year changes or IRS issues revisions.
- Use only official IRS/SSA sources for numeric thresholds.
- If law data is older than the analyzed return year, flag the result as stale and require manual update before final sign-off.

## Script

`scripts/review_1040.py` performs:
- Current-year arithmetic and law checks.
- Prior-year consistency checks.
- Weighted audit-risk scoring.
- DOCX risk report generation with `python-docx`.

If `python-docx` is missing, install it:

```bash
python -m pip install --user python-docx
```

## Output Interpretation

- Treat findings as risk signals, not final legal determinations.
- Require CPA/EA review for filing decisions.
- Present audit likelihood as a heuristic estimate derived from return patterns and detected issues, not a guarantee.

## Example Command

```bash
python scripts/review_1040.py \
  --input references/example_returns.json \
  --output-dir output/form-1040-review
```