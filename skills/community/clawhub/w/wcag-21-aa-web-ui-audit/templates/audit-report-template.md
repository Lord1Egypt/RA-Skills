# WCAG 2.1 AA Web UI Audit Report

## Scope & Assumptions
- Product type:
- Audit mode: `Confirmed implementation audit` | `Readiness Review`
- Environments tested:
- Flows in scope (complete processes):
- Components in scope:
- Platforms in scope:
- Timebox and constraints:
- Evidence handling:
  - `confirmed implementation issue`
  - `design-time risk`
- Conformance statement: This report provides accessibility conformance guidance against WCAG 2.1 Level A and Level AA.

## Severity Rubric
- Blocker: prevents task completion
- High: major friction / frequent failure
- Medium: noticeable barrier with workaround
- Low: minor issue / polish

## Affected User Groups
- Screen reader
- Keyboard-only
- Low vision
- Cognitive/learning
- Motor
- Color vision

## A) Audit Summary (One Page)
- Overall conformance posture:
- Total findings:
- Findings by severity: `Blocker` / `High` / `Medium` / `Low`
- Most impacted flows:
- Most impacted components:
- Complete process risks:
- Top 3 remediation priorities:
- Immediate risk note:

## B) Findings Table

| ID | Flow/Page | Component | WCAG SC (ID • Name • Level) | Severity | Affected Users | Issue Summary | Repro Steps | Expected | Actual | Recommended Fix (Design + Dev) | Verification (Manual + Tool) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| F-001 | [flow/page] | [component] | [SC id • SC name • level] | [Blocker/High/Medium/Low] | [groups] | [summary] | [steps] | [expected] | [actual] | [design fix + dev fix] | [manual + tool] | [Open/In Progress/Done] |

## C) Per-Flow Notes

### Flow: [Flow Name]
- Flow goal:
- Complete process boundary:
- Keyboard audit notes:
- Screen reader notes:
- Zoom/reflow notes:
- Forms/errors notes:
- Dynamic updates/status message notes:
- Risk summary:

### Flow: [Flow Name]
- Flow goal:
- Complete process boundary:
- Keyboard audit notes:
- Screen reader notes:
- Zoom/reflow notes:
- Forms/errors notes:
- Dynamic updates/status message notes:
- Risk summary:

## D) Remediation Backlog

### Prioritization Rules
1. Fix all `Blocker` findings first.
2. Then fix `High` findings in highest business-critical flows first.
3. Resolve shared component root causes before isolated page-level polish.

### Backlog Snapshot
| Epic | Issue | Priority | Mapped SC | Acceptance Criteria | Test Steps | Owner | Target Sprint | Dependencies | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| [Epic] | [Issue] | [Priority] | [SCs] | [Criteria] | [Steps] | [Owner] | [Sprint] | [Deps] | [Status] |

## E) Definition of Done (Engineering + QA)
- [ ] Every finding has mapped WCAG SC ID, name, and level.
- [ ] Every implemented fix has acceptance criteria and test steps.
- [ ] Keyboard-only completion is verified for every in-scope flow.
- [ ] Screen reader announcements are verified for status updates (including SC 4.1.3 cases).
- [ ] Contrast and non-text contrast checks are verified on interactive states.
- [ ] Zoom/reflow checks pass at 200% and 320 CSS px width.
- [ ] Form error identification/suggestions are verified.
- [ ] Error prevention is verified for legal/financial/data commitments.
- [ ] Regression pass is complete on desktop and mobile.
- [ ] Final report language remains accessibility conformance guidance (no certification statements).
