# Plan: Multi-Cadence Summaries (Dream Weaver + Memory Crystal)

**Date:** 2026-03-24
**Author:** cc-mini (with Parker)
**Issue:** #193

## Context

Dream Weaver currently runs in two modes: full (crisis recovery) and incremental (maintenance). It reads transcripts, produces journals + memories. We need four cadence levels (daily, weekly, monthly, quarterly) that produce summaries. Each level consolidates the level below. Two tracks: team (from crystal/conversations) and dev (from git).

## Output Locations

### Per-agent (one combined summary per cadence)
```
~/wipcomputerinc/staff/{agent}/
  journals/                                <- human-requested (manual + Dream Weaver)
  automated/memory/summaries/
    daily/YYYY-MM-DD.md                    <- everything this agent did that day
    weekly/YYYY-WXX.md                     <- week in review for this agent
    monthly/YYYY-MM.md
    quarterly/YYYY-QX.md
```

### Org-wide
```
~/wipcomputerinc/operations/updates/
  team/                                    <- conversations, decisions, insights (from crystal)
    daily/YYYY-MM-DD.md
    weekly/YYYY-WXX.md
    monthly/YYYY-MM.md
    quarterly/YYYY-QX.md
  dev/                                     <- code shipped (from git)
    daily/YYYY-MM-DD.md
    weekly/YYYY-WXX.md
    monthly/YYYY-MM.md
    quarterly/YYYY-QX.md
```

### Runtime (backed up, not published)
```
~/.ldm/agents/{agentId}/memory/
  daily/          <- raw daily logs (cc-hook, already exists)
  journals/       <- Dream Weaver journals (already exists for cc-mini)
  sessions/       <- session exports
  transcripts/    <- raw JSONL
```

## Repos to Modify

### 1. dream-weaver-protocol-private

**Files:**
- `src/types.ts` ... add `'daily' | 'weekly' | 'monthly' | 'quarterly'` to mode type. Add summary output fields.
- `src/prompts.ts` ... add 4 new prompt builders (one per cadence). Daily reads crystal search results. Weekly reads 7 daily summaries. Monthly reads 4 weeklies. Quarterly reads 3 monthlies.
- `src/engine.ts` ... add `runSummary()` function alongside existing `runDreamWeaver()`. Summary mode reads different inputs (crystal results or previous summaries instead of transcripts).
- `src/parser.ts` ... add `===SUMMARY===` section parsing.

**New type:**
```typescript
export interface SummaryOptions {
  agentId: string;
  cadence: 'daily' | 'weekly' | 'monthly' | 'quarterly';
  track: 'team' | 'dev';
  workspacePath: string;        // ~/wipcomputerinc
  crystalSearchResults?: string; // for daily team: crystal search output
  gitLogOutput?: string;         // for daily dev: git log output
  previousSummaries?: string[];  // for weekly+: paths to previous cadence files
  dryRun?: boolean;
}
```

**Prompts per cadence:**
- Daily team: "Here are crystal search results from the last 24 hours. Summarize: what was discussed, decided, discovered. Who worked on what."
- Daily dev: "Here is git log output from the last 24 hours across all repos. Summarize: what shipped, PRs merged, releases, tickets closed."
- Weekly team: "Here are 7 daily team summaries. What themes emerged? What decisions stuck? Open threads?"
- Weekly dev: "Here are 7 daily dev summaries. What shipped this week? Release highlights?"
- Monthly/quarterly: same pattern, consolidating the level below.

### 2. memory-crystal-private

**Files:**
- `src/dream-weaver.ts` ... add `runSummary()` wrapper that provides crystal search results to the engine. Hook to store summaries in crystal.
- `src/mcp-server.ts` ... optionally expose `crystal_summarize` tool.

**Flow for daily team summary:**
1. `crystal_search --since 24h --quality deep --limit 30` across all agents
2. Pass results to Dream Weaver `runSummary({ cadence: 'daily', track: 'team' })`
3. Engine builds prompt, invokes Claude, parses output
4. Write to per-agent `automated/memory/summaries/daily/` AND org-wide `operations/updates/team/daily/`
5. Store summary in crystal via `crystal_remember`

### 3. wip-ldm-os-private

**Files:**
- `bin/ldm.js` ... deploy summary prompts and cron job during `ldm install`
- `scripts/ldm-summary.sh` ... new script that runs the daily/weekly/monthly/quarterly jobs
- `shared/prompts/` ... prompt templates for each cadence (deployed to ~/.ldm/shared/prompts/)

**ldm-summary.sh:**
```bash
#!/bin/bash
# Usage: ldm-summary.sh daily|weekly|monthly|quarterly
CADENCE=$1
# Reads workspace from ~/.ldm/config.json
# For team: calls crystal search, pipes to Dream Weaver
# For dev: runs git log across repos, pipes to Dream Weaver
# Writes output to workspace paths
```

**Cron (via LDM Dev Tools.app):**
```
0 6 * * *     ldm-summary.sh daily       # 6 AM daily
0 7 * * 1     ldm-summary.sh weekly      # Monday 7 AM
0 8 1 * *     ldm-summary.sh monthly     # 1st of month 8 AM
0 9 1 1,4,7,10 * ldm-summary.sh quarterly # 1st of quarter 9 AM
```

**New job in LDM Dev Tools.app:**
```bash
# jobs/summary.sh
exec ~/.ldm/bin/ldm-summary.sh "$1"
```

### 4. wip-ai-devops-toolbox-private

**Files:**
- `tools/wip-repos/git-summary.mjs` ... new file. Runs `git log` across all repos in the workspace, formats for Dream Weaver input.

**Used by:** `ldm-summary.sh daily dev` calls this to get the git activity.

### 5. wipcomputerinc home repo (settings/config.json)

**Add:**
```json
"summaries": {
  "cadences": ["daily", "weekly", "monthly", "quarterly"],
  "tracks": ["team", "dev"],
  "schedule": {
    "daily": "06:00",
    "weekly": "Monday 07:00",
    "monthly": "1st 08:00",
    "quarterly": "1st of Q 09:00"
  },
  "perAgent": "staff/{agent}/automated/memory/summaries/",
  "orgWide": "operations/updates/"
}
```

## Implementation Order

1. **Config:** Add summaries section to config.json
2. **Prompts:** Write the 8 prompt templates (4 cadences x 2 tracks) in dream-weaver-protocol
3. **Engine:** Add `runSummary()` to dream-weaver-protocol (types, engine, parser, prompts)
4. **Crystal integration:** Add summary wrapper to memory-crystal (crystal search as input)
5. **Git summary:** Add git-summary.mjs to devops toolbox
6. **Orchestrator:** Write ldm-summary.sh (reads config, runs the right cadence/track)
7. **Installer:** ldm install deploys ldm-summary.sh + prompts + cron
8. **LDM Dev Tools.app:** Add summary.sh job
9. **Test:** Run `ldm-summary.sh daily --dry-run` then real daily for both tracks
10. **Release:** All 4 repos get releases

## Verification

```bash
# Dry run
~/.ldm/bin/ldm-summary.sh daily --dry-run

# Real daily
~/.ldm/bin/ldm-summary.sh daily

# Check per-agent output
cat ~/wipcomputerinc/staff/cc-mini/automated/memory/summaries/daily/2026-03-25.md

# Check org-wide output
cat ~/wipcomputerinc/operations/updates/team/daily/2026-03-25.md
cat ~/wipcomputerinc/operations/updates/dev/daily/2026-03-25.md

# Check crystal stored it
crystal_search "daily summary March 25"
```
