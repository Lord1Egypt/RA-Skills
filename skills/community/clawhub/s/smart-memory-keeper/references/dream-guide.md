# Dream Consolidation — 定期记忆整理（< OpenClaw 2026.4.8）

> **Note**: OpenClaw 2026.4.8+ has native Dreaming (`/dreaming on`). This guide is only for older versions.
> See SKILL.md Part 4 for version-aware logic.

> Inspired by Claude Code's AutoDream — a periodic reflective pass over memory files to fix drift and keep memories accurate.

## Trigger conditions

Run during heartbeat when both are true:
- `lastDream` was more than 7 days ago
- `sessionsSinceLastDream` >= 3

## Four phases

**① Orient**: scan `memory/tasks.md` and last 7 days of journals — understand current state

**② Collect**: find content worth long-term retention:
- Repeated lessons → distill and write to `MEMORY.md`
- Repeatedly validated methods → update "Notes" in project entries
- Tasks completed 30+ days ago → remove from "Completed" in tasks.md

**③ Integrate**:
- Write collected content to the right files
- **Check for memory drift**: if new content contradicts old memory, rewrite the old — don't keep both
- Replace relative time references ("last time", "before") with absolute dates

**④ Prune**:
- `MEMORY.md` over 200 lines → merge similar entries, remove outdated content
- Journals older than 30 days → move to `memory/archive/` (full content preserved)

## Drift correction principle

> A memory was accurate when written, but circumstances changed — that's memory drift.

When drift is found:
- **Rewrite**: replace old with accurate info — don't keep two conflicting entries
- **Date it**: add "updated YYYY-MM-DD" after corrections
- **No stacking**: don't append "(update: xxx)" to old entries — rewriting is cleaner

## Dream state file

```json
// memory/dream-state.json
{
  "lastDream": "YYYY-MM-DD",
  "sessionsSinceLastDream": 0
}
```

### Init (auto-create if missing)

```bash
echo '{"lastDream": "2000-01-01", "sessionsSinceLastDream": 0}' > ~/.openclaw/workspace/memory/dream-state.json
```

Setting `lastDream` to `2000-01-01` ensures the first check triggers consolidation immediately.

### Counting rule (once per day only)

- Today's journal was just created this heartbeat → increment `sessionsSinceLastDream`
- Today's journal already existed → skip (prevents overcounting from multiple daily heartbeats)

### After Dream completes

- Set `lastDream` = today (`YYYY-MM-DD`)
- Reset `sessionsSinceLastDream` = 0
- Write back to `dream-state.json`
