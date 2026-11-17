# Tier 0 Observation Pool

> Entries below are auto-detected potential bug patterns with insufficient confidence to promote to rules.
> Each reoccurrence of the same pattern adds +1 confidence. Hit the threshold → auto-promote.

| # | Pattern | Conf | First Seen | Recur | Last Triggered | Status |
|:--|:--|:--|:--|:--|:--|:--|
| — | (No observations yet) | — | — | — | — | — |

## Promotion Thresholds

- Confidence ≥ 3 → auto-promote to Tier 1 [SOFT] rule
- Confidence ≥ 5 → auto-promote to Tier 2 [HARD] rule

## Demotion / Eviction Rules

- User rejects suggestion 3 consecutive times → confidence -3
- Confidence drops to 0 → move to `retired.md`
- **Staleness (V2.2)**: Entry not re-triggered in 30 days → `status` = `stale`, eligible for pruning
- **Hard cap (V2.2)**: Max 50 entries. When exceeded → prune lowest-confidence stale entries first

## Anti-Bloat Audit Trail (V2.2)

| Date | Action | Details |
|:--|:--|:--|
| — | (No pruning yet) | — |
