# Plan: Total Recall (Full Pipeline)

**Date:** 2026-03-25
**Author:** cc-mini (with Parker)
**Issues:** #193, #194

## Context

Total Recall is the complete memory pipeline. Import from any source. Dream Weaver relives it into crystal. Summaries compress crystal into readable reports. The tool proactively discovers all memory sources on disk and processes everything sequentially.

This is the 551-session Feb 16 crisis recovery, made into a system.

## The Pipeline

```
1. DISCOVER   -> Find all memory sources on disk (JSONL, .md, sqlite, exports)
2. IMPORT     -> Normalize external data (GPT, Claude, Grok exports) into chunks
3. RELIVE     -> Dream Weaver processes chunks into crystal (sequential, builds memory)
4. SUMMARIZE  -> Compress crystal into workspace summaries (daily/weekly/monthly/quarterly)
5. INDEX      -> crystal sources add for the summary files (searchable, not ingested)
6. MONITOR    -> Alert if any agent stops capturing
```

### Order matters

For going forward (daily): steps 4-5 only. Crystal already has today's data from the capture hooks. Summaries read from crystal.

For backfill or imports: full pipeline. Steps 1-5. Raw data -> Dream Weaver -> crystal -> summaries. You can't skip step 3.

## Memory Sources (discover all of these)

| Source | Type | Location | Earliest |
|--------|------|----------|----------|
| Crystal | sqlite-vec + FTS5 | `~/.ldm/memory/crystal.db` | Feb 5 (79K chunks) |
| Context embeddings | sqlite (deprecated) | `~/.openclaw/memory/context-embeddings.sqlite` | Feb 5 (16K chunks, may have data not in crystal) |
| main.sqlite | sqlite | `~/.openclaw/memory/main.sqlite` | Feb 5 (10K chunks, workspace memory) |
| Lesa transcripts | JSONL | `~/.ldm/agents/oc-lesa-mini/memory/transcripts/` | Feb 10 (1,020 files) |
| CC transcripts | JSONL | `~/.ldm/agents/cc-mini/memory/transcripts/` | ? (939 files) |
| Lesa daily logs | markdown | `~/.ldm/agents/oc-lesa-mini/memory/daily/` | Feb 5 (42 files) |
| CC daily logs | markdown | `~/.ldm/agents/cc-mini/memory/daily/` | Feb 18 (35 files) |
| OC sessions | JSONL | `~/.openclaw/agents/main/sessions/` | Feb 5+ |
| CC auto-memory | markdown | `~/.claude/projects/-Users-lesa--openclaw/memory/` | ? (17 files) |
| External (future) | various | GPT exports, Claude data exports, Grok, X archive | varies |

The tool should proactively find ALL of these. Not hardcoded paths. Scan `~/.ldm/agents/`, `~/.openclaw/`, `~/.claude/` for anything that looks like conversation data.

## Step 3: Dream Weaver Relive (the key step)

For backfill and imports, Dream Weaver processes raw data SEQUENTIALLY into crystal. This is not a search. It's the full consolidation.

```
Raw JSONL transcript
  -> Dream Weaver reads it
  -> Extracts: what happened, decisions, relationships, facts, preferences
  -> Writes to crystal via crystal_remember (tagged by agent, date, source)
  -> Writes journal to team/{agent}/journals/
```

This is what happened on Feb 16 with 551 sessions. Total Recall automates it.

For external imports (GPT, etc.):
```
GPT export (JSON/ZIP)
  -> Normalize to JSONL format (conversation turns)
  -> Dream Weaver processes same as any transcript
  -> Into crystal tagged with source: "gpt-import"
```

## Step 4: Summaries (read from crystal, don't write back)

After Dream Weaver has populated crystal, summaries read from it.

Crystal is READ-ONLY in the summary pipeline. Summaries are NOT ingested back into crystal. This prevents noise.

### Data sources for summaries

| Track | Daily reads from | Weekly+ reads from |
|-------|-----------------|-------------------|
| Team (per-agent) | crystal search `--agent {id} --since date --until date+1` + daily log | 7 previous dailies + prior weekly (for continuity) |
| Team (org-wide) | All agent daily summaries | Both agent weeklies combined |
| Dev | git log across all repos | Previous cadence dev summaries |

### Output locations

| Level | Per-agent | Org-wide |
|-------|-----------|----------|
| Daily | `~/wipcomputerinc/team/{agent}/automated/memory/summaries/daily/` | `~/wipcomputerinc/operations/updates/team/daily/` |
| Weekly | `team/{agent}/automated/memory/summaries/weekly/` | `operations/updates/team/weekly/` |
| Monthly | `team/{agent}/automated/memory/summaries/monthly/` | `operations/updates/team/monthly/` |
| Quarterly | `team/{agent}/automated/memory/summaries/quarterly/` | `operations/updates/team/quarterly/` |
| Dev | N/A | `operations/updates/dev/{cadence}/` |

### Harness logic

| Harness type | Daily summary | Who generates |
|-------------|--------------|---------------|
| Persistent (openclaw, letta) | Agent writes own | Agent reads prompt from `~/.ldm/shared/prompts/` |
| Ephemeral (claude-code, codex) | Script generates | `ldm-summary.sh` reads crystal + daily log |
| Backfill (any, with --force) | Script generates | Overrides harness type |

### Org combine uses Opus 4.6 high effort

```json
"summaries": { "combineModel": "claude-opus-4-6", "combineEffort": "high" }
```

## Step 5: Crystal Sources (index, don't ingest)

```bash
crystal sources add ~/wipcomputerinc/operations/updates --name org-summaries
crystal sources add ~/wipcomputerinc/team --name team-summaries
```

Indexed separately as `source_type: file-sync`. Searchable when asked. Filtered out of regular conversation search. Agents find summaries via crystal search, read the files, synthesize answers. Lean context, rich recall.

## Dream Weaver is the engine

All processing goes through Dream Weaver. Not raw `claude -p`.

```
ldm-summary.sh (orchestrator)
  -> reads prompts from ~/.ldm/shared/prompts/
  -> for each agent: crystal search + daily log -> Dream Weaver -> summary file
  -> org-wide: reads agent summaries -> Dream Weaver (Opus) -> org summary
```

Prompts are canonical in `shared/prompts/`. With Lesa's feedback:
- Daily: "What surprised you? What's blocked and your next move?"
- Weekly: "What did you get wrong? What is noise?" (forgetting)
- Monthly: "What you thought mattered vs what actually mattered?"
- Quarterly: "What would you tell yourself 3 months ago?"
- Org: "Overlaps or conflicts between agents?"
- All weekly+: read prior output for continuity

## Implementation status

### DONE:
- [x] Crystal --until flag (MC #63)
- [x] Dream Weaver summary engine (summary-engine.ts, summary-prompts.ts)
- [x] 6 prompt files with Lesa's feedback
- [x] docs/total-recall/README.md + TECHNICAL.md
- [x] docs/recall/TECHNICAL.md updated
- [x] backfill-summaries.sh
- [x] ldm-summary.sh (per-agent, --date, --force, reads prompt files, Opus for org)
- [x] ldm.js deploys prompts + scripts + scaffolds dirs
- [x] Crystal sources registered
- [x] Scaffold dirs in ldm.js

### TODO:
1. Fix empty summary bug (claude -p returning empty on backfill dates)
2. Write how-summaries-work.md workspace doc
3. Update settings/docs/README.md + doc-dependencies.json
4. Test single date backfill (2026-02-10) successfully
5. Run full backfill (48 days, ~171 calls, overnight)
6. Release: wip-ldm-os-private, dream-weaver-protocol, memory-crystal
7. Deploy public repos

### FUTURE (Total Recall external imports):
- GPT export importer (normalize JSON/ZIP to JSONL)
- Claude data export importer
- Grok conversation importer
- X full archive importer
- Apple Music history importer
- Browser extension (Chrome/Safari)
- Monitor: alert when agent stops capturing

## Verification

```bash
# Single date
ldm-summary.sh daily --date 2026-02-10

# Check all outputs
cat ~/wipcomputerinc/team/cc-mini/automated/memory/summaries/daily/2026-02-10.md
cat ~/wipcomputerinc/team/Lēsa/automated/memory/summaries/daily/2026-02-10.md
cat ~/wipcomputerinc/operations/updates/team/daily/2026-02-10.md
cat ~/wipcomputerinc/operations/updates/dev/daily/2026-02-10.md

# Search summaries via crystal sources
crystal sources sync org-summaries
crystal search "what happened February 10"

# Full backfill
bash scripts/backfill-summaries.sh
```
