# Report Eval Failure Map

Use this map when a case fails. The goal is to point directly to the layer that should be fixed, not to argue about vibes after the fact.

## 1. Compression

- Typical failures:
  - `report_class` missing or inconsistent with the source.
  - `audience` / `decision_goal` missing, so the report has no explicit async-reading target.
  - `must_include` / `must_avoid` absent, so later review cannot tell what drifted.
- Fix here:
  - [SKILL.md](/D:/projects/kai-report-creator/SKILL.md)
  - [README.md](/D:/projects/kai-report-creator/README.md)
  - [README.zh-CN.md](/D:/projects/kai-report-creator/README.zh-CN.md)

## 2. IR Contract

- Typical failures:
  - `timeline` is not real time.
  - `kpi` values are sentences.
  - `chart` / `diagram` bodies invent undocumented schema.
- Fix here:
  - [SKILL.md](/D:/projects/kai-report-creator/SKILL.md)
  - [references/rendering-rules.md](/D:/projects/kai-report-creator/references/rendering-rules.md)
  - [evals/contract_checks.py](/D:/projects/kai-report-creator/evals/contract_checks.py)
  - [tests/test_ir_contract_validation.py](/D:/projects/kai-report-creator/tests/test_ir_contract_validation.py)

## 3. Async Readability

- Typical failures:
  - The opening never states the judgment.
  - Heading stack reads like a template instead of a scan path.
  - Data blocks appear without a takeaway or next action.
- Fix here:
  - [references/review-checklist.md](/D:/projects/kai-report-creator/references/review-checklist.md)
  - [evals/rubric.schema.json](/D:/projects/kai-report-creator/evals/rubric.schema.json)
  - Case artifacts under [evals/cases](/D:/projects/kai-report-creator/evals/cases)

## 4. Render Integrity

- Typical failures:
  - HTML shell IDs are missing.
  - `report-summary` JSON is absent or incomplete.
  - Raw `:::` blocks leak into final HTML.
- Fix here:
  - [references/html-shell-template.md](/D:/projects/kai-report-creator/references/html-shell-template.md)
  - [tests/test_html_shell_contract.py](/D:/projects/kai-report-creator/tests/test_html_shell_contract.py)
  - [scripts/run-report-evals.py](/D:/projects/kai-report-creator/scripts/run-report-evals.py)

## Operating Rule

Every real production failure should become one new case in [evals/report-cases.csv](/D:/projects/kai-report-creator/evals/report-cases.csv), plus the smallest artifact set needed to reproduce it.
