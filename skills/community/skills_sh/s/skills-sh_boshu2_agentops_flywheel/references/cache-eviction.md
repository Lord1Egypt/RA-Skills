# Cache Eviction

The knowledge flywheel includes automated cache eviction to prevent unbounded growth:

```
Passive Read tracking → Confidence decay → Maturity scan → Archive
```

**How it works:**
1. **Passive tracking** — `ao maturity --scan` records when learnings are accessed
2. **Confidence decay** — Unused learnings lose confidence at 10%/week
3. **Composite criteria** — Learnings are eviction candidates when ALL conditions met:
   - Utility < 0.3 (low MemRL score)
   - No citation in 90+ days
   - Confidence < 0.2 (decayed from disuse)
   - Not established maturity (proven knowledge is protected)
4. **Archive** — Candidates move to `.agents/archive/learnings/` (never deleted)

**Commands:**
- `ao maturity --evict` — dry-run: show eviction candidates
- `ao maturity --evict --archive` — execute: archive candidates
- `ao metrics cite-report --days 30` — cache health report

**Kill switches:**
- `AGENTOPS_EVICTION_DISABLED=1` — disable SessionEnd auto-eviction
- `AGENTOPS_PRUNE_AUTO=0` — disable SessionStart auto-pruning (default: off)
