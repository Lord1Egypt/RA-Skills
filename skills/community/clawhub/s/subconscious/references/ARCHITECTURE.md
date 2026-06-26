# Architecture Reference

## Design Principles

1. **Bounded** — Hard limits on everything: 50 core, 100 live, 500 pending items
2. **Governed** — Every mutation typed, bounded, logged. No unbounded changes
3. **Metabolism not daemon** — One-shot cron jobs, not persistent process
4. **Immutable core** — Values/guiding principles never change without human OK
5. **Session-isolated** — Bias injected ephemeral, session can't bloat from it

## Item Lifecycle

```
Source → pending.jsonl (candidate_queued)
  ↓ tick (reinforce once per item)
pending.jsonl (candidate_reinforced)
  ↓ rotate --enable-promotion (if confidence>=0.75, reinforcement>=3, freshness>=0.3)
live.json (active)
  ↓ flush (daily snapshot)
snapshots/*.json
```

## Governance Rules

| Protection Class | Mutation | Bounds |
|-----------------|---------|--------|
| CORE | Any | BLOCKED (manual only) |
| ACTIVE | WEIGHT_UPDATE, FRESHNESS_DECAY, CONFIDENCE_UPDATE | ±0.1/step, decay→0.1 |
| STALE | REINFORCEMENT, FRESHNESS_DECAY, ARCHIVAL | Max 50 stale items |
| GATED | PROMOTION_TO_LIVE | confidence≥0.75, reinforce≥3, freshness≥0.3 |

## Learnings Bridge Flow

```
Self-improving agent writes to .learnings/
  ↓ scan every tick (via learnings_bridge.py)
New entries queued to pending.jsonl (type=candidate_queued)
  ↓ tick reinforcement (1x per item per tick)
type becomes candidate_reinforced
  ↓ rotate with --enable-promotion
If eligible: promoted to live.json
If not eligible: stays in pending, reinforced again next tick
```

## Bias Injection

- Max 5 items per session turn (enforced by `build_bias`)
- Content: 200 chars max per item (enforced by `_compact_text`)
- Max 1200 chars total bias block (enforced by MAX_BIAS_CHARS)
- All from live store only (core items injected separately as identity)

## Snapshot Rotation

- Daily at midnight (or on `flush` call)
- Maximum 10 snapshots
- Oldest deleted when limit exceeded
- Snapshot = JSON dump of live items + metrics + timestamp

## Key Safety Rules

1. NEVER promote if governance check fails
2. NEVER allow mutations on CORE items
3. NEVER skip duplicate check before queuing
4. NEVER promote an item already in live (dedup by ID on write)
5. Reinforcement is one-shot per item per tick (track state to prevent double-reinforce)
