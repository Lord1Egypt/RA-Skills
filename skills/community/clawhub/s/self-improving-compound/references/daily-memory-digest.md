# Daily Memory Digest Integration

This reference describes the optional daily factual-memory loop that pairs with the SQLite self-improvement store.

## Purpose

`learning/` captures reusable execution lessons. A daily memory digest captures factual continuity: what happened, what changed, what was decided, and what needs follow-up.

Use both loops together:

- `memory/YYYY-MM-DD.md` — factual timeline, decisions, paths, job IDs, links, risks, follow-ups.
- `learning/memory_tree/chunks.db` — compact reusable prevention rules: corrections, tool/API gotchas, workflow conventions, recurring failures.

Do not duplicate an entire daily note into `learning/`. Extract only lessons that should alter future behavior.

## Suggested daily note quality bar

When the day had meaningful activity, prefer a detailed note that can reconstruct the day without rereading raw chat logs.

Recommended sections:

1. Overview
2. Key workflows and actions
3. Important decisions
4. System/configuration changes
5. Files/projects changed
6. External integrations and automations
7. Problems, risks, and unfinished work
8. Items to promote into long-term memory/rules
9. Next-step suggestions
10. Source notes

## Integration options

### Option A — bring your own collector

If your runtime has a transcript/session collector, call it first and write its output to a context file. Then have the agent synthesize `memory/YYYY-MM-DD.md` from that context.

`scripts/daily-memory.sh` supports:

```bash
SELF_IMPROVING_DAILY_COLLECTOR="python3 /path/to/collector.py" \
  bash scripts/daily-memory.sh --root /path/to/workspace --date YYYY-MM-DD
```

The collector may print a context path or summary. The agent should inspect that output before writing the final note.

### Option B — no collector

If no collector exists, use `scripts/daily-memory.sh` as a contract printer. It validates the date/root and prints the target file plus the required quality bar. The agent must gather context using available runtime tools.

## Self-improvement pass

After writing the daily note, run the capture gate:

- User correction / changed preference → `log-correction`
- Non-obvious failure or API/tool/schema quirk → `log-error`
- Workflow convention or successful reusable workaround → `log-learning`
- Missing capability or repeated friction → `log-feature`

Keep learning entries short, searchable, and prevention-oriented.
