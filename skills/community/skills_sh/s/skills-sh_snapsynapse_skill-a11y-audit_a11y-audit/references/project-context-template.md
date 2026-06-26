---
skill_bundle: a11y-audit
file_role: reference
version: 1
version_date: 2026-03-03
previous_version: null
change_summary: >
  Added a canonical workspace-local PROJECT_CONTEXT template with
  minimal and issue-tracker examples for audit configuration.
---

# Project Context Template

Use this file as the canonical shape for
`.a11y-audit/PROJECT_CONTEXT.md` in the audited workspace.

## Rules

- Keep mutable project preferences here, not in the installed skill.
- Omit sections that are not needed for the current project.
- Prefer concrete route lists over prose when the audit scope is known.
- If the project already has accessibility planning docs, link to them
  here instead of duplicating their content.
- If first-run setup is straightforward, prefer
  `scripts/bootstrap-context.js` to generate the initial file.
- If the live app binds to a different local URL than expected, update
  `base_url` to the working value after verification.

## Canonical Structure

```markdown
# Accessibility Audit Project Context

## Project

- name: Example App
- base_url: http://localhost:5173
- repo_root: .
- app_root: frontend

## Audit Scope

- standards: WCAG 2.1 AA
- additional_standards: CAN-ASC-6.2
- scan_mode: full
- include_routes:
  - /
  - /about
  - /contact
- priority_routes:
  - /
  - /checkout
- exclude_routes:
  - /admin
  - /debug

## Output Configuration

- output_mode: markdown
- report_path: docs/accessibility/audits/audit-YYYY-MM-DD.md
- json_path: docs/accessibility/audits/audit-YYYY-MM-DD.json

## Issue Tracker

- issue_tracker: github
- issue_severity_threshold: P1
- issue_labels_priority: accessibility-p0-critical, accessibility-p1-high, accessibility-p2-medium, accessibility-p3-low
- issue_labels_status: accessibility-new
- issue_labels_wcag: wcag-perceivable, wcag-operable, wcag-understandable, wcag-robust

## References

- conformance_docs: docs/accessibility/conformance-plan.md
- manual_testing_guide: docs/accessibility/manual-testing.md
- design_tokens: docs/design/tokens.md
```

## Field Guidance

- `name`: Human-readable project name for report headers.
- `base_url`: Preferred audit target for local or preview runs.
- `repo_root`: Workspace-relative root when the audited app is in a monorepo.
- `app_root`: Workspace-relative app directory containing frontend dependencies.
- `standards`: Primary compliance target. Default to `WCAG 2.1 AA`.
- `additional_standards`: Optional secondary standards to map in the report.
- `scan_mode`: Suggested values are `quick`, `full`, or `issues`.
- `include_routes`: Explicit routes to scan.
- `priority_routes`: Routes to prefer when the user asks for a limited audit.
- `exclude_routes`: Routes to omit from automated scanning.
- `output_mode`: `markdown`, `markdown+json`, or `markdown+issues`.
- `report_path`: Workspace-relative markdown report path.
- `json_path`: Workspace-relative JSON output path when JSON is enabled.
- `issue_tracker`: `github`, `gitlab`, `linear`, or `jira`.
- `issue_severity_threshold`: Lowest priority that should create tickets.
- `issue_labels_priority`: Priority labels in P0-P3 order.
- `issue_labels_status`: Default status label for new issues.
- `issue_labels_wcag`: Optional labels used to classify issues by WCAG principle.
- `conformance_docs`: Existing compliance or conformance documentation.
- `manual_testing_guide`: Existing testing procedures to cross-link in the report.
- `design_tokens`: Existing color, typography, or spacing documentation.

## Minimal Example

Use this when the project only needs a straightforward markdown audit.

```markdown
# Accessibility Audit Project Context

## Project

- name: Marketing Site
- base_url: http://localhost:3000

## Audit Scope

- standards: WCAG 2.1 AA
- scan_mode: quick
- include_routes:
  - /
  - /pricing
  - /contact

## Output Configuration

- output_mode: markdown
- report_path: docs/accessibility/audits/audit-YYYY-MM-DD.md
```

## `markdown+issues` Example

Use this when the audit should create tickets after explicit approval.

```markdown
# Accessibility Audit Project Context

## Project

- name: Checkout App
- base_url: http://localhost:4173
- app_root: apps/web

## Audit Scope

- standards: WCAG 2.1 AA
- additional_standards: EN 301 549
- scan_mode: issues
- priority_routes:
  - /
  - /cart
  - /checkout
  - /confirmation

## Output Configuration

- output_mode: markdown+issues
- report_path: docs/accessibility/audits/audit-YYYY-MM-DD.md
- json_path: docs/accessibility/audits/audit-YYYY-MM-DD.json

## Issue Tracker

- issue_tracker: github
- issue_severity_threshold: P1
- issue_labels_priority: accessibility-p0-critical, accessibility-p1-high, accessibility-p2-medium, accessibility-p3-low
- issue_labels_status: accessibility-new
- issue_labels_wcag: wcag-perceivable, wcag-operable, wcag-understandable, wcag-robust

## References

- conformance_docs: docs/accessibility/conformance-plan.md
- manual_testing_guide: docs/accessibility/manual-testing.md
```
