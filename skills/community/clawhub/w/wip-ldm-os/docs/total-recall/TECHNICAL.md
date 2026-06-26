# Total Recall ... Technical Reference

## Architecture

```
~/.ldm/agents/{agentId}/memory/    <- SOURCE (raw data per agent)
  daily/                            <- daily logs
  journals/                         <- Dream Weaver journals
  sessions/                         <- session exports (.md)
  transcripts/                      <- raw JSONL
       |
       v
Dream Weaver (prompts at ~/.ldm/shared/prompts/)
       |
       v
~/wipcomputerinc/team/{agent}/automated/memory/summaries/
  daily/ weekly/ monthly/ quarterly/     <- per-agent summaries
       |
       v (combine all agents)
~/wipcomputerinc/operations/updates/
  team/ daily/ weekly/ monthly/ quarterly/  <- org-wide team
  dev/  daily/ weekly/ monthly/ quarterly/  <- org-wide dev (from git)
```

## Harness Logic

Each agent in `~/.ldm/config.json` has a harness type:

| Harness | Behavior | Examples |
|---------|----------|---------|
| Persistent (openclaw, letta, hermes) | Agent writes own summaries via prompt | Lesa |
| Ephemeral (claude-code, codex) | Script generates from crystal + daily logs | CC |

```
for each agent:
  if persistent AND summary file exists: skip (agent wrote it)
  if persistent AND file missing AND --force: generate via script
  if ephemeral: always generate via script
```

## Key Files

| File | What |
|------|------|
| `scripts/ldm-summary.sh` | Orchestrator. Per-agent search, org-wide combine. |
| `scripts/backfill-summaries.sh` | Loop: dailies -> weeklies -> monthlies -> quarterly |
| `shared/prompts/daily-agent-summary.md` | Prompt for daily per-agent summary |
| `shared/prompts/weekly-agent-summary.md` | Prompt for weekly (reads 7 dailies) |
| `shared/prompts/monthly-agent-summary.md` | Prompt for monthly (reads 4 weeklies) |
| `shared/prompts/quarterly-agent-summary.md` | Prompt for quarterly (reads 3 monthlies) |
| `shared/prompts/org-daily-team.md` | Prompt for combining agent summaries |
| `shared/prompts/daily-dev.md` | Prompt for git log summary |
| `bin/ldm.js` | Installer. Deploys scripts + prompts. Scaffolds dirs. |

## Data Sources

### Team track (conversations, decisions)

- `~/.ldm/agents/{agentId}/memory/daily/{date}.md` ... raw daily log
- `crystal search --agent {id} --since {date} --until {date+1}` ... crystal chunks for that day
- Both fed to Dream Weaver prompt to produce the summary

### Dev track (code shipped)

- `git log --since={date} --until={date+1} --oneline --all` across all repos in workspace
- Fed to prompt to produce factual dev summary

## Config

`~/wipcomputerinc/settings/config.json`:

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
  "perAgent": "team/{agent}/automated/memory/summaries/",
  "orgWide": "operations/updates/"
}
```

`~/.ldm/config.json`:

```json
"agents": ["cc-mini", "oc-lesa-mini"]
```

## Schedule

Cron via LDM Dev Tools.app:

```
0 6 * * *         ldm-summary.sh daily
0 7 * * 1         ldm-summary.sh weekly      (Monday)
0 8 1 * *         ldm-summary.sh monthly     (1st of month)
0 9 1 1,4,7,10 *  ldm-summary.sh quarterly   (1st of quarter)
```

## External Imports (Future)

Total Recall will also import from external platforms:

| Platform | Method | Status |
|----------|--------|--------|
| Anthropic (Claude) | API / data export | Planned |
| OpenAI (ChatGPT) | API / data export | Planned |
| xAI (Grok) | API | Planned |
| X (Twitter) | Full archive import | Planned |
| Apple Music | Listening history | Planned |
| Browser | Chrome/Safari extension | Planned |

Each import follows the same pipeline: CONNECT -> IMPORT -> RELIVE -> CRYSTAL.

## Connection to Other Components

- **[Recall](../recall/TECHNICAL.md)** ... loads context at session start. Total Recall fills what Recall serves.
- **[Bridge](../bridge/TECHNICAL.md)** ... agent-to-agent communication. Summaries are shared via the workspace, not Bridge.
- **[Memory Crystal](https://github.com/wipcomputer/memory-crystal)** ... storage + search. Total Recall writes to Crystal. Crystal search provides data for summaries.
- **[Dream Weaver](https://github.com/wipcomputer/dream-weaver-protocol)** ... consolidation engine. Prompts invoke Dream Weaver via `claude -p`.
