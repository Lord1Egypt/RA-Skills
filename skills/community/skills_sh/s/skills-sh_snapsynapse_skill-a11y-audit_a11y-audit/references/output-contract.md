---
skill_bundle: a11y-audit
file_role: reference
version: 1
version_date: 2026-03-03
previous_version: null
change_summary: >
  Added a dedicated reference for markdown and JSON output requirements,
  including degraded Lighthouse behavior and report section rules.
---

# Output Contract

Read this file when generating audit deliverables.

## Markdown Report

Write a markdown report with these sections in order:

1. Header
2. Executive Summary
3. Automated Scan Results
4. WCAG 2.1 AA Compliance Matrix
5. Delta from Previous Audit
6. Project-Specific Standard
7. Manual Testing Recommendations
8. Remediation Priority
9. Issues Created
10. Methodology

Rules:

- Use valid GFM tables.
- Reference WCAG criteria as `SC X.X.X`.
- Use axe `helpUrl` links when available.
- Omit sections that are truly empty.
- If Lighthouse was skipped, say why in both Executive Summary and Methodology.
- If the runtime URL differs from the expected URL, record both.
- Phrase compliance status conservatively: this is an automation-assisted audit view, not a conformance certification.

## JSON Output

When `output_mode` is `markdown+json` or `markdown+issues`, write a JSON
file alongside the markdown report. Use the schema in
`references/output-schema.json`.

## Delta Section

- Include this section only if a prior audit output exists.
- Show new violations, resolved violations, and score changes when you
  have enough evidence to compare runs.
- If comparison data is missing or non-comparable, omit the section
  rather than inventing a weak delta.

## Degraded Modes

- If Lighthouse is missing, write `lighthouse.status: "skipped"` in the
  JSON output and explain the reason.
- If browser automation is blocked entirely, do not generate a fake
  report. Summarize the blocker and produce the highest-value partial
  output the workspace supports.
