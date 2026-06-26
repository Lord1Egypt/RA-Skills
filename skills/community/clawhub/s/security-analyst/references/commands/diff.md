---
description: "Compare two security analysis runs to show new, resolved, and persistent findings."
model: opus
---

# Security Analyst — Delta Report

Compare two security analysis runs and produce a delta report highlighting changes.

**Arguments:**
- `[run-a]` — baseline run directory path (older run)
- `[run-b]` — current run directory path (newer run, optional — defaults to latest)

If no arguments are provided, auto-detect the two most recent runs in `docs/security/runs/`.

**Read `references/constants.md` for all directory paths, filenames, and placeholder variables.**

**Execution:**

1. Validate both run directories exist and contain `reports/final.md` and `findings/index.md`
2. Read the SBOM template: `{TEMPLATES_DIR}/delta-report.md`
3. Read both runs' findings indexes (`findings/index.md`) and match findings between runs using:
   - Finding ID exact match
   - CWE + file match (same weakness type in same file)
   - CWE + component match (same weakness in same logical area)
4. Read both runs' `reports/sbom.md` (if present) to diff dependencies
5. Categorize each finding as: New, Resolved, Persistent, or Severity Changed
6. If Run A has a `reports/fix-plan.md`, cross-reference fix plan tasks with resolved findings
7. Write the delta report to `{RUN_DIR_B}/reports/delta.md`

**Output files:**
- `{RUN_DIR_B}/reports/delta.md` (Delta report)

**STOP after presenting the delta summary. Wait for the user to ask a follow-up question.**
