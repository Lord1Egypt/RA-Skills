# Negotiation Entry Examples

Concrete examples of negotiation entries with realistic patterns.

## 1) Poor Anchor

```markdown
## [LRN-20260413-001] anchor_error

**Logged**: 2026-04-13T10:12:00Z
**Priority**: high
**Status**: pending
**Area**: framing

### Summary
Opening anchor was too close to fallback, reducing room for structured trades.

### Details
Team opened at a near-midpoint offer to appear collaborative. Counterparty immediately requested additional concessions, interpreting the anchor as soft.
```

## 2) Concession Without Reciprocity

```markdown
## [NEG-20260413-001] concession_leak

**Logged**: 2026-04-13T10:40:00Z
**Priority**: critical
**Status**: pending
**Area**: concessions

### Summary
Discount granted without reciprocal term extension or scope reduction.

### What Happened
Commercial concession was offered to keep momentum, but no matching commitment was captured.
```

## 3) BATNA Absent

```markdown
## [NEG-20260413-002] batna_weakness

**Logged**: 2026-04-13T11:05:00Z
**Priority**: high
**Status**: pending
**Area**: preparation

### Summary
No actionable BATNA defined before first pricing round.

### Root Cause
Preparation focused on target terms only; walk-away point and fallback option were not validated.
```

## 4) Stakeholder Escalation Mismatch

```markdown
## [NEG-20260413-003] escalation_misalignment

**Logged**: 2026-04-13T11:50:00Z
**Priority**: high
**Status**: pending
**Area**: escalation

### Summary
Escalation sent to executive sponsor before legal/procurement owner alignment.

### Impact
Escalation created urgency noise but did not unblock the actual approval path.
```

## 5) Contract Term Ambiguity

```markdown
## [NEG-20260413-004] agreement_risk

**Logged**: 2026-04-13T12:20:00Z
**Priority**: critical
**Status**: pending
**Area**: contract_terms

### Summary
Renewal clause had ambiguous trigger language and unresolved fallback.

### Prevention
Require explicit term definitions and final legal signoff before recommending close.
```

## 6) Value Reframing Success

```markdown
## [LRN-20260413-002] value_articulation_gap

**Logged**: 2026-04-13T13:10:00Z
**Priority**: medium
**Status**: resolved
**Area**: framing

### Summary
Shift from unit-price discussion to risk-reduction framing improved acceptance.

### Outcome
Counterparty accepted narrower concession after quantified value framing.
```

## 7) Promoted Playbook

```markdown
## [LRN-20260412-004] objection_handling_gap

**Logged**: 2026-04-12T16:30:00Z
**Priority**: high
**Status**: promoted
**Promoted**: negotiation_playbook
**Area**: bargaining

### Summary
Recurring implementation-risk objection now handled through 3-step response flow.

### Metadata
- Recurrence-Count: 5
- Pattern-Key: objection.implementation_risk
```

## 8) Promoted Skill

```markdown
## [LRN-20260410-001] framing_miss

**Logged**: 2026-04-10T09:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/value-anchor-reset
**Area**: framing

### Summary
Reusable anchor-reset method for negotiations drifting toward unilateral concessions.

### Metadata
- Recurrence-Count: 6
- Pattern-Key: framing.anchor_reset
```
