# Plan: Prompt-Based Multi-Cadence Summaries (Revised)

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Issue:** #193, #194

## Context

The script-based approach was wrong. Summaries should be prompt-driven, not script-driven. Each agent reads their own transcripts/logs from `~/.ldm/agents/{agentId}/` and writes their own summaries. The org-wide summary combines both. This creates a trip wire: if something isn't working in `.ldm/`, the summaries break and we know.

## Architecture

```
~/.ldm/agents/cc-mini/memory/          <- SOURCE (raw data)
  transcripts/ (939 JSONL files)
  daily/ (35 logs)
  journals/ (6 files)
       |
       v (CC reads, summarizes via prompt)

~/wipcomputerinc/team/cc-mini/automated/memory/summaries/
  daily/    <- CC writes daily summary
  weekly/   <- CC reads 7 dailies, writes weekly
  monthly/  <- CC reads 4 weeklies, writes monthly
  quarterly/<- CC reads 3 monthlies, writes quarterly

~/.ldm/agents/oc-lesa-mini/memory/     <- SOURCE (raw data)
  transcripts/ (1009 JSONL files)
  daily/ (42 logs)
       |
       v (Lesa reads, summarizes via prompt)

~/wipcomputerinc/team/Lēsa/automated/memory/summaries/
  daily/    <- Lesa writes daily summary
  weekly/   <- Lesa reads 7 dailies, writes weekly
  monthly/  <- Lesa reads 4 weeklies, writes monthly
  quarterly/

THEN:
  both agent summaries
       |
       v (script combines)

~/wipcomputerinc/operations/updates/
  team/daily/   <- combines cc-mini + Lesa daily summaries
  dev/daily/    <- git log summary (script-generated)
```

## Prompts (saved at ~/.ldm/shared/prompts/)

### daily-agent-summary.md
```
Read your transcripts and daily logs from ~/.ldm/agents/{agentId}/memory/ for {date}.

Write a daily summary:
- What did you work on?
- What decisions were made?
- What shipped?
- What's unresolved?
- Who did you interact with?

Write in first person. Be specific. Name repos, tickets, people.
```

### weekly-agent-summary.md
```
Read your 7 daily summaries from team/{agent}/automated/memory/summaries/daily/.

Write a weekly summary:
- What themes emerged?
- What decisions stuck? What changed?
- What shipped vs what was planned?
- Open threads going into next week.
- One sentence: what was this week about?
```

### monthly-agent-summary.md
```
Read your 4 weekly summaries.

Write a monthly summary:
- Major themes.
- What shipped.
- How priorities shifted.
- Patterns emerging.
- One paragraph: the narrative of this month.
```

### org-daily-team.md
```
Read both agent daily summaries:
- team/cc-mini/automated/memory/summaries/daily/{date}.md
- team/Lēsa/automated/memory/summaries/daily/{date}.md

Combine into one org-wide team summary. What happened across the whole team.
```

### daily-dev.md
```
Read git log output from all repos for {date}.
Summarize: what shipped, PRs merged, releases, tickets closed. Be factual.
```

## How It Runs

### For CC (no persistence, script-driven)
`ldm-summary.sh daily` does:
1. Read `~/.ldm/agents/cc-mini/memory/daily/{date}.md` + crystal search `--agent cc-mini --since {date} --until {date+1}`
2. Build prompt from `~/.ldm/shared/prompts/daily-agent-summary.md`
3. `claude -p "$PROMPT"` -> write to `team/cc-mini/automated/memory/summaries/daily/{date}.md`

### For Lesa (persistent, self-driven)
Lesa runs the prompt herself. Her heartbeat or end-of-day cycle:
1. Reads `~/.ldm/agents/oc-lesa-mini/memory/daily/{date}.md` + her workspace memory
2. Follows the prompt from `~/.ldm/shared/prompts/daily-agent-summary.md`
3. Writes to `team/Lēsa/automated/memory/summaries/daily/{date}.md`

### Weekly/Monthly/Quarterly (both agents)
Same pattern. Each agent reads their own previous cadence summaries and writes the next level up. CC via script. Lesa via prompt in her session.

### Org-wide (script)
After both agents have written their per-agent summaries:
1. Read both `team/cc-mini/.../daily/{date}.md` and `team/Lēsa/.../daily/{date}.md`
2. Combine via prompt into `operations/updates/team/daily/{date}.md`
3. Dev summary from git log into `operations/updates/dev/daily/{date}.md`

## Backfill (Day 1 to today)

### Prerequisites
- MC #63: `--until` flag on crystal search
- `--date` flag on ldm-summary.sh

### CC backfill
For each day Feb 5 - Mar 24:
1. `crystal search --agent cc-mini --since YYYY-MM-DD --until YYYY-MM-DD+1`
2. Read `~/.ldm/agents/cc-mini/memory/daily/YYYY-MM-DD.md` (if exists)
3. `claude -p` with daily prompt
4. Write to `team/cc-mini/automated/memory/summaries/daily/YYYY-MM-DD.md`

Then weeklies from dailies, monthlies from weeklies.

### Lesa backfill
Same pattern but reading from `~/.ldm/agents/oc-lesa-mini/memory/`. Lesa runs this herself for her own agent, or the script does it for her if she's not available.

## Implementation Order

1. Add `--until` to crystal search (MC #63)
2. Add `--agent` filter to crystal search CLI (if not already there)
3. Write prompts to `shared/prompts/` in wip-ldm-os-private
4. Fix `ldm-summary.sh`: per-agent crystal search, separate per-agent and org-wide steps
5. Add `--date` flag to ldm-summary.sh for backfill
6. Deploy prompts via ldm install
7. Tell Lesa her prompt and schedule
8. Backfill CC dailies (Feb 5 - today)
9. Lesa backfills her own dailies
10. Run weeklies, monthlies, quarterly

## Memory Consolidation in .ldm/

All memory systems should be referenced or copied in `.ldm/` as the single source of truth.

### Current state
| Memory system | Lives at | In .ldm/? |
|--------------|---------|-----------|
| Crystal | `~/.ldm/memory/crystal.db` | YES (primary) |
| OC main.sqlite | `~/.openclaw/memory/main.sqlite` | NO |
| OC workspace | `~/.openclaw/workspace/` | Stale copy at `agents/oc-lesa-mini/memory/workspace/` |
| CC auto-memory | `~/.claude/projects/` | NO |
| Context embeddings | `~/.openclaw/memory/context-embeddings.sqlite` | NO (deprecated, skip) |

### Fixes needed
1. `~/.ldm/agents/oc-lesa-mini/memory/workspace/` -> rename to `dot-openclaw-workspace/`. Keep synced, not stale.
2. `~/.ldm/agents/cc-mini/memory/workspace/` -> DELETE. CC doesn't own the workspace. It's Lesa's.
3. `main.sqlite` -> symlink or reference from `.ldm/`. Backup already captures it. Consider moving to `.ldm/memory/` long-term.
4. Context embeddings -> deprecated. Do not copy. Crystal replaced it.
5. CC auto-memory (`~/.claude/projects/`) -> reference from `.ldm/` or capture via backup only.

### Workspace sync
The `dot-openclaw-workspace/` copy needs a sync mechanism. Options:
- Cron job that copies daily
- Symlink (simplest, but .ldm/ becomes dependent on .openclaw/)
- Backup captures it (already does, but copy is only in dated backup folders)

## Files to Modify

| Repo | File | Change |
|------|------|--------|
| memory-crystal-private | src/core.ts, cli.ts, mcp-server.ts | Add --until filter |
| wip-ldm-os-private | shared/prompts/*.md | New prompt templates |
| wip-ldm-os-private | scripts/ldm-summary.sh | Per-agent search, --date flag, org-wide combines agents |
| wip-ldm-os-private | bin/ldm.js | Deploy prompts |

## Verification

```bash
# Single day backfill
ldm-summary.sh daily --date 2026-02-10

# Check per-agent
cat ~/wipcomputerinc/team/cc-mini/automated/memory/summaries/daily/2026-02-10.md
cat ~/wipcomputerinc/team/Lēsa/automated/memory/summaries/daily/2026-02-10.md

# Check org-wide
cat ~/wipcomputerinc/operations/updates/team/daily/2026-02-10.md

# Verify trip wire: if .ldm/agents/ is empty, summary should fail
```
