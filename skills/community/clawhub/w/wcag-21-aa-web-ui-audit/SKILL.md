---
name: wcag-21-aa-web-ui-audit
description: Audit web UI for WCAG 2.1 Level AA and produce a remediation backlog. Use when users ask for WCAG 2.1 AA audits, accessibility reviews, conformance reports, remediation plans, keyboard/focus/contrast/reflow/forms/ARIA/status-message checks.
---

# WCAG 2.1 AA Web UI Audit

## Skill Version
- 1.0.0

## Trigger Phrases
Use this skill when the request includes any of the following:
- WCAG 2.1 AA audit
- Accessibility audit or UI accessibility review
- A11y checklist or conformance report
- Remediation plan for accessibility issues
- Keyboard navigation or focus issues
- Contrast issues
- Zoom/reflow issues
- ARIA or name/role/value issues
- Status message or toast announcement issues
- Forms and accessibility issues

## Scope & Assumptions (Required First Output)
When invoked, first output a `## Scope & Assumptions` section before any findings. Include:
- Product type
- Key flows and complete processes in scope
- Platforms in scope
- Components in scope
- Access constraints (timebox, environments, auth constraints)
- Evidence type boundaries:
  - `confirmed implementation issue`: verified on running UI or artifact with reproducible behavior
  - `design-time risk`: predicted from design artifacts/spec without runtime confirmation
- Conformance note: "This report provides accessibility conformance guidance against WCAG 2.1 Level A and AA."

## Inputs and Best-Effort Defaults
Collect these inputs. If missing, proceed with defaults and state assumptions explicitly.

- Product type
  - Preferred input: `SaaS`, `ecommerce`, `content`
  - Default: `SaaS` (switch to `ecommerce` if cart/checkout is in scope)
- Key flows to test
  - Preferred input: explicit flows
  - Default: `sign-in`, `onboarding`, `search/filter`, `forms`, `checkout (if applicable)`
- Target platforms
  - Preferred input: desktop, mobile, or both
  - Default: `desktop + mobile`
- Known UI components
  - Preferred input: explicit component list
  - Default: `navigation`, `modal`, `drawer`, `toast/status`, `carousel`, `date picker`, `table`, `forms`
- Access constraints
  - Preferred input: timebox, environments, authentication access
  - Default: `single-pass audit on available environment within stated timebox`
- Evidence artifacts
  - Preferred input: URLs and/or design files/specs
  - Default behavior: if no URLs/artifacts are provided, run a clearly labeled `Readiness Review` only

## Deterministic Workflow
Run these steps in order.

1. Scope
- Define flows, pages, components, and complete processes.
- Identify highest-risk areas: forms, checkout, auth, navigation, modals, dynamic updates.

2. Baseline automated checks (optional)
- Run axe and lighthouse on key pages when runtime URLs are available.
- Capture and deduplicate issues.
- If automation dependencies are missing, continue with manual workflow and mark automation as skipped.

3. Manual keyboard audit
- Validate tab order, focus visibility, keyboard traps, skip links, modals, menus, and custom controls.

4. Visual audit
- Validate text contrast, non-text contrast, focus indicator visibility/contrast, non-color error cues, and hover/focus content behavior.

5. Zoom and reflow audit
- Validate at 200% zoom, 320 CSS px width, text-spacing overrides, and orientation behavior.

6. Forms and errors audit
- Validate labels, instructions, error identification, error suggestions, and error prevention for legal/financial/data commitments.

7. Semantics and ARIA audit
- Validate name/role/value, label-in-name, autocomplete/input purpose semantics, and parsing robustness.

8. Status messages audit (AA)
- Validate that toasts and inline status updates are announced without forced focus moves when appropriate.

9. Synthesis
- Map each finding to WCAG SC.
- Assign severity.
- Propose design and engineering fixes.
- Add acceptance criteria and verification steps.

## Output Contract (Always Deterministic)
Always render output with these sections in this exact order using templates:
- `A) Audit Summary (One Page)`
- `B) Findings Table`
- `C) Per-Flow Notes`
- `D) Remediation Backlog`
- `E) Definition of Done (Engineering + QA)`

Use these files directly:
- `templates/audit-report-template.md`
- `templates/finding-template.md`
- `templates/remediation-backlog-template.md`

## Findings Quality Bar
Every finding must include:
- WCAG SC ID, name, and level
- Severity: `Blocker`, `High`, `Medium`, `Low`
- Affected user groups
- Repro steps
- Expected vs actual behavior
- Suggested fix split into design and engineering actions
- Verification steps (manual and tool-based where relevant)
- Evidence type: `confirmed implementation issue` or `design-time risk`

## Severity Rubric
- `Blocker`: Prevents task completion for one or more user groups.
- `High`: Causes major friction or frequent failure.
- `Medium`: Noticeable barrier with workaround.
- `Low`: Minor barrier or polish issue.

## Component Fix Recipes
Use `docs/ui-component-checklists.md` for fix-oriented component recipes covering:
- Buttons/links
- Inputs/selects/forms
- Modal/dialog
- Tooltip/popover
- Carousel
- Toast/status
- Tabs
- Accordion
- Table
- Date picker

## Optional Automation Script
Use the optional script only when runtime URLs are provided:

```bash
node scripts/run_axe_playwright.js --url https://example.com
node scripts/run_axe_playwright.js --urls-file ./urls.txt
```

Behavior expectations:
- Writes `outputs/axe-results.json` and `outputs/axe-summary.md`.
- Deduplicates by `(rule id + target selector + page)`.
- Continues on per-URL failures.
- If `playwright` or `@axe-core/playwright` is missing, prints install guidance and exits without failing.

## "All Requirements" Requests
If the user asks for all WCAG requirements, point to and include or excerpt:
- `docs/wcag21-aa-success-criteria.md`

## Conformance Language Guardrail
Do not issue legal determinations or certification statements. Use conformance phrasing such as:
- "accessibility conformance guidance"
- "conformance risk"
- "current conformance gaps"

## Source Notes
Use WCAG terminology and SC names from:
- WCAG 2.1 Recommendation
- WAI How to Meet WCAG (Quick Reference) filtered to Level A and AA
- Understanding WCAG, including 4.1.3 Status Messages
