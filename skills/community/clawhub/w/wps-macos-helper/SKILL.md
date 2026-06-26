---
name: wps-macos-helper
description: Help macOS users work with WPS Office more reliably when WPS is explicitly part of the document workflow. Use for preparing, converting, reviewing, exporting, or troubleshooting files that will be opened or checked in WPS on macOS, especially for Word/docx, PDF, Markdown, PowerPoint, and Excel workflows. Useful for: (1) preparing content before opening in WPS, (2) reducing WPS/Word compatibility issues, (3) choosing safe conversion workflows, (4) export and formatting guidance on macOS, and (5) troubleshooting layout, fonts, tables, page breaks, headers/footers, and PDF output.
---

# WPS macOS Helper

Default goal: improve document workflow quality on macOS when WPS is part of the path.

## Core workflow
1. Identify the source format and final goal.
2. Prefer content pre-processing before opening in WPS.
3. Reduce compatibility risk before export or layout polishing.
4. Keep original files untouched unless the user explicitly wants in-place edits.

## Read references as needed
- Read `references/workflow.md` for standard document workflows.
- Read `references/case-studies.md` for real task patterns and recommended routes.
- Read `references/compatibility.md` for WPS/Word compatibility issues.
- Read `references/export-and-format.md` for export, PDF, and formatting guidance.
- Read `references/troubleshooting.md` when a document opens incorrectly or exports badly.
- Read `references/release-checklist.md` before packaging or publishing the skill.

## Use scripts as needed
- Use `scripts/prepare_doc_workflow.sh` for low-risk preprocessing suggestions and Markdown conversion entry points.

## Operating rules
- Prefer producing new output files over overwriting originals.
- Prefer Markdown/docx/PDF workflows over GUI automation.
- Treat GUI automation as a later-stage option, not the default path.
- When exact WPS behavior is uncertain, give the user the safest compatible route first.
