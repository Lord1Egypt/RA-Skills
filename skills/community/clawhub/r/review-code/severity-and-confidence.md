# Severity and Confidence Guide

Use this matrix to keep triage consistent across reviews.

## Priority Levels

| Priority | Meaning | Merge Impact |
|----------|---------|--------------|
| P0 | Security breach, data loss, or outage risk | Block merge |
| P1 | High-probability functional defect | Block merge |
| P2 | Maintainability or medium-term reliability risk | Advisory |
| P3 | Style or low-impact improvement | Advisory |

## Confidence Levels

| Confidence | Use When | Reviewer Behavior |
|------------|----------|-------------------|
| High | Reproducible or directly provable from code | State as finding |
| Medium | Strong signal but partial context missing | State with assumptions |
| Low | Suspicion without sufficient evidence | Ask as targeted question |

## Escalation Rules

- P0/P1 with high confidence -> explicit blocker.
- P0/P1 with medium confidence -> blocker plus required verification steps.
- P2/P3 with low confidence -> convert to question, not mandate.

## Finding Format

Use one line summary first:
`[P1][High] file:line - short issue title`

Then include:
- What fails
- Why it matters
- Minimal fix path
- Validation step

## Anti-Noise Rules

- Never up-rank a finding to force action.
- Never bury blockers inside long advisory lists.
- Never call something “critical” without user-impact explanation.

## Tie-Breaker

If uncertain between two severities:
- choose lower severity
- raise confidence notes
- request the missing evidence needed to upgrade
