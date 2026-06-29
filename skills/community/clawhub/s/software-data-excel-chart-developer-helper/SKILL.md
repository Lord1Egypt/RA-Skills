---
name: software-data-excel-chart-developer-helper
description: Create and troubleshoot Excel reporting workbooks with charts, dashboards, conditional formatting, print areas, PDF/image export, openpyxl or Office automation, and recurring data refresh. Use when Codex needs to build or repair XLSX reports while preserving workbook layout, formulas, and presentation-ready output.
---

# Excel Chart Report Developer

Use this skill for recurring Excel reports where the workbook is both a data artifact and a presentation artifact. Keep charts, formulas, formatting, print settings, and exports in sync.

## Workflow

1. Clarify the report target: dashboard workbook, chart pack, PDF export, image export, print-ready report, recurring refresh, or workbook template.
2. Separate data, calculations, and presentation:
   - Raw or imported data sheets.
   - Calculation/helper sheets with formulas and named ranges.
   - Output sheets with charts, summaries, conditional formatting, and print areas.
3. Choose the automation layer:
   - Use `openpyxl` for workbook structure, formulas, styles, charts, tables, print setup, and conditional formatting where supported.
   - Use Excel desktop automation only when live chart rendering, Power Query refresh, or PDF export fidelity is essential and available.
   - Preserve unsupported workbook parts by editing package contents carefully.
4. Design stable ranges. Prefer Excel Tables and named ranges over hard-coded row counts.
5. Apply visual formatting after data writes so fills, borders, number formats, widths, and conditional formatting do not drift.
6. Validate:
   - Formulas point to valid ranges.
   - Charts reference current data.
   - Print areas, page orientation, margins, headers/footers, and page breaks match the expected export.
   - Exports are reviewed for clipping, missing labels, and font substitution.

## Common Fix Patterns

- **Chart not updating**: verify series formulas, named ranges, table expansion, and cached chart data.
- **Conditional formatting drift**: inspect rule ranges and priority ordering after row insertion.
- **Bad PDF export**: check print area, scaling, margins, page breaks, and whether a desktop Excel render is required.
- **Template overwrites**: write values into known input ranges, then preserve output sheets and chart objects.
- **Data refresh**: log source file timestamps, row counts, and validation totals for each run.

## Outputs

Provide:

- A report architecture or repair diagnosis.
- Implementation steps or code for workbook generation/update.
- A validation note covering formulas, charts, formatting, and exports.

Read `references/requirement-plan.md` only when source evidence from the discovery run is needed.
