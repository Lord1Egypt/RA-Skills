# Accessibility Audit Project Context

## Project

- name: Checkout App
- base_url: http://localhost:4173
- app_root: apps/web

## Audit Scope

- standards: WCAG 2.1 AA
- additional_standards: CAN-ASC-6.2
- scan_mode: issues
- priority_routes:
  - /
  - /checkout

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
