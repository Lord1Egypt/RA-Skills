# Business Entry Examples

Concrete examples of well-formatted business entries.

## 1) Approval Bottleneck (BUS)

```markdown
## [BUS-20260413-001] decision_latency

**Logged**: 2026-04-13T09:10:00Z
**Priority**: high
**Status**: pending
**Area**: governance
**Severity**: high

### Summary
Quarter-end procurement approvals remained pending for 5 business days, blocking delivery.

### Issue Details
Three purchase requests above policy threshold had no backup approver configured.
Primary approver was out of office and no automatic escalation was active.

### Impact Assessment
- Affected functions: procurement, operations, finance
- KPI/SLA impact: on-time onboarding at risk
- Cost impact: expedited shipping likely if delayed further

### Recommended Action
- Configure backup approver for all threshold-based approvals
- Escalate pending approvals after 48h
- Add control to governance checklist
```

## 2) KPI Definition Mismatch (LRN)

```markdown
## [LRN-20260413-002] kpi_misalignment

**Logged**: 2026-04-13T10:20:00Z
**Priority**: high
**Status**: pending
**Area**: reporting

### Summary
"On-time delivery" was calculated from two different dates across operations and finance dashboards.

### Details
Operations measured against promised ship date; finance measured against invoice date.
Monthly executive report showed conflicting performance without annotation.

### Recommended Action
Create canonical KPI definition in registry with owner, formula, and source system.
```

## 3) Vendor Handoff Failure (BUS)

```markdown
## [BUS-20260413-003] handoff_failure

**Logged**: 2026-04-13T11:15:00Z
**Priority**: high
**Status**: in_progress
**Area**: vendor_management
**Severity**: high

### Summary
Vendor onboarding handoff failed due to missing acceptance checklist and owner acknowledgment.

### Issue Details
Procurement marked onboarding complete, but operations had not received configuration
credentials or SLA contacts. Service launch slipped by 4 days.

### Recommended Action
Introduce signed handoff artifact with required fields and accountable owner.
```

## 4) Budget Variance Review (BUS)

```markdown
## [BUS-20260413-004] process_breakdown

**Logged**: 2026-04-13T12:00:00Z
**Priority**: medium
**Status**: pending
**Area**: budgeting
**Severity**: medium

### Summary
Budget variance exceeded threshold for two consecutive months without documented mitigation.

### Issue Details
Spend tracker flagged >8% variance, but review meeting notes lacked action owner and due date.

### Recommended Action
Require variance action plan template in monthly budget review cadence.
```

## 5) Policy Gap (LRN)

```markdown
## [LRN-20260413-005] policy_gap

**Logged**: 2026-04-13T13:05:00Z
**Priority**: medium
**Status**: pending
**Area**: procurement

### Summary
No explicit policy existed for emergency vendor renewals under 10-day deadlines.

### Details
Teams used ad hoc exception paths, resulting in inconsistent approvals and missing evidence.

### Recommended Action
Add emergency-renewal policy section with threshold, approver, and evidence requirements.
```

## 6) Cross-Team Misalignment (BUS)

```markdown
## [BUS-20260413-006] stakeholder_misalignment

**Logged**: 2026-04-13T14:00:00Z
**Priority**: high
**Status**: pending
**Area**: communication
**Severity**: high

### Summary
Operations prioritized SLA stability while sales prioritized launch speed, causing decision deadlock.

### Issue Details
No shared decision memo defined tie-break criteria; escalation path was unclear.

### Recommended Action
Adopt decision memo template with owner, criteria, and escalation deadline.
```

## 7) Promoted Playbook (LRN -> promoted)

```markdown
## [LRN-20260413-007] process_breakdown

**Logged**: 2026-04-13T15:00:00Z
**Priority**: high
**Status**: promoted
**Promoted**: process_playbook
**Area**: operations

### Summary
Recurring intake triage failures required a standard operating playbook.

### Details
Five incidents showed inconsistent routing and missing dependency checks.

### Recommended Action
Published "Intake-to-Execution Triage Playbook" with 24h triage SLA and owner rules.
```

## 8) Promoted Skill (LRN -> promoted_to_skill)

```markdown
## [LRN-20260413-008] decision_latency

**Logged**: 2026-04-13T15:30:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/approval-escalation-cadence
**Area**: governance

### Summary
Approval queue escalation logic became reusable across planning and procurement workflows.

### Details
Pattern repeated across four teams with similar root cause: missing escalation SLA.

### Recommended Action
Extracted reusable skill for escalation design and governance cadence setup.
```

---
