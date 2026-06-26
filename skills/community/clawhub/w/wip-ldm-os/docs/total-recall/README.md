###### WIP Computer

# Total Recall

## Connect your AI accounts. Bring every memory home. Never lose a conversation again.

Total Recall is LDM OS's memory import and consolidation system. It connects to AI platforms, imports conversation history, and uses Dream Weaver to consolidate raw data into searchable, structured memories in Memory Crystal.

It also generates multi-cadence summaries (daily, weekly, monthly, quarterly) for every agent.

## The Pipeline

```
1. CONNECT    -> Sign into your AI accounts (Anthropic, OpenAI, xAI, etc.)
2. IMPORT     -> Pull every conversation (API, data export, or automation)
3. RELIVE     -> Dream Weaver processes raw conversations into memories
4. CRYSTAL    -> Consolidated memories stored in Memory Crystal
5. SUMMARIZE  -> Multi-cadence summaries (daily/weekly/monthly/quarterly)
6. MONITOR    -> System check alerts when any agent stops capturing
```

## Two Modes

### Going Forward (daily)

Each agent writes its own daily summary. Persistent agents (OpenClaw, Letta) write from their own context. Ephemeral agents (Claude Code, Codex) get script-generated summaries from crystal + daily logs. Org-wide summaries combine all agents.

```bash
~/.ldm/bin/ldm-summary.sh daily              # today
~/.ldm/bin/ldm-summary.sh daily --team-only  # team track only
~/.ldm/bin/ldm-summary.sh daily --dev-only   # dev track only
```

### Backfill (historical)

Import and summarize everything from day 1. Uses `--force` to generate for all agents regardless of harness type.

```bash
~/.ldm/bin/ldm-summary.sh daily --date 2026-02-10 --force   # one day
bash scripts/backfill-summaries.sh                            # all days
```

## Output Locations

### Per-agent
```
~/wipcomputerinc/team/{agent}/automated/memory/summaries/
  daily/YYYY-MM-DD.md
  weekly/YYYY-MM-DD.md
  monthly/YYYY-MM.md
  quarterly/YYYY-QX.md
```

### Org-wide
```
~/wipcomputerinc/operations/updates/
  team/daily/YYYY-MM-DD.md    <- conversations, decisions, insights
  dev/daily/YYYY-MM-DD.md     <- code shipped, PRs, releases
```

## Recursive Consolidation

Each level reads the level below:

```
Transcripts + Crystal -> Daily summaries
7 dailies             -> Weekly summary
4 weeklies            -> Monthly summary
3 monthlies           -> Quarterly summary
```

This is the Dream Weaver paper's consolidation architecture applied at four cadences.

## Connection to Recall

[Recall](../recall/README.md) loads context at session start. Total Recall fills the memory that Recall serves. Without Total Recall, Recall only has what was captured going forward. With Total Recall, Recall has the complete history.

## Part of LDM OS

Total Recall is included with LDM OS. Summaries activate after `ldm init`. External imports are opt-in per platform.

---

[Technical Reference](./TECHNICAL.md)
