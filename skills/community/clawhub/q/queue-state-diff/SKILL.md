---
name: queue-state-diff
description: Compare two queue or state snapshots and explain what changed between them. Use when Codex needs to analyze drift between JSON/JSONL snapshots, detect newly stuck jobs, missing queue references, changed counters, or state regressions across two points in time.
---

# Queue State Diff

Use this skill to answer: what changed, what disappeared, and what got worse?

## Workflow

1. Gather two comparable snapshots: before/after JSON, report JSON, or JSONL-derived exports.
2. Normalize them before reasoning; prefer deterministic diff over freehand comparison.
3. Run `scripts/queue_state_diff.js` for raw comparison.
4. Interpret the diff in terms of operational meaning: regressions, recoveries, or noise.

## Script

```bash
node skills/queue-state-diff/scripts/queue_state_diff.js \
  --before out/report-before.json \
  --after out/report-after.json \
  --out out/queue-state-diff.md
```

## Guardrails

- Compare like with like; do not diff unrelated report formats.
- Separate numeric drift from referential drift.
- Call out missing keys explicitly instead of treating them as zero.
