---
name: workflow-guardian-soul
description: Soul-layer persistent context for workflow-guardian. Tracks active workflows, compliance trends, violation patterns, and rule registry across sessions.
---

# Workflow Guardian — Soul Context

## [WORKSPACE OWNER]
- Owner:        [soul.owner.name]
- Initialized:  YYYY-MM-DD
- Soul version: 1.0.0

---

## [ACTIVE WORKFLOWS]
<!-- All workflows currently defined. Upsert by workflow-id. -->
<!-- Format: ID | TASK_TYPE | STATE | COMPLIANCE_RATE% | LAST_RUN -->

---

## [BLOCKED GATES]
<!-- Workflows currently stopped at a gate. Remove when resolved. -->
<!-- Format: YYYY-MM-DD | WORKFLOW_ID | GATE_NAME | REASON | DAYS_BLOCKED -->

---

## [VIOLATION PATTERNS]
<!-- Same rule broken 3+ times. Upsert by pattern-id. -->
<!-- Format: PATTERN_ID | RULE | WORKFLOW_ID | COUNT | FIRST_SEEN | LAST_SEEN -->

---

## [GLOBAL RULES SUMMARY]
<!-- Current active global rules. Update when rules change. -->
<!-- Format: RULE_ID | TYPE | ENFORCEMENT | SUMMARY -->

---

## [COMPLIANCE TREND]
<!-- Updated after every execution. Last 4 weeks. -->
<!-- Format: WEEK | EXECUTIONS | VIOLATIONS | COMPLIANCE_RATE% -->

---

## [POST-FIX PENDING]
<!-- Workflows in post-fix state awaiting resolution. -->
<!-- Format: YYYY-MM-DD | WORKFLOW_ID | VIOLATION_SLUG | STATUS -->

---

## [RECENT VIOLATIONS]
<!-- Rolling 20. Drop oldest when >20. -->
<!-- Format: YYYY-MM-DD | SLUG | WORKFLOW_ID | RULE | SEVERITY | STATUS -->

---

## [SESSION LOG]
<!-- Append-only. One entry per session. -->
<!-- Format: YYYY-MM-DD | workflows_run:N | violations:N | gates_blocked:N | compliance:N% -->

---

## Write Protocol

| Section | Trigger | Operation |
|---|---|---|
| [ACTIVE WORKFLOWS] | Workflow created/updated | Upsert by ID |
| [BLOCKED GATES] | Gate blocked | Append; remove when cleared |
| [VIOLATION PATTERNS] | Pattern detected (3+) | Upsert by pattern-id |
| [GLOBAL RULES SUMMARY] | Rules change | Upsert by rule-id |
| [COMPLIANCE TREND] | Every workflow execution | Update last 4 weeks |
| [POST-FIX PENDING] | Post-fix state set | Append; remove when done |
| [RECENT VIOLATIONS] | Any violation | Append; drop oldest >20 |
| [SESSION LOG] | Session end | Append |
