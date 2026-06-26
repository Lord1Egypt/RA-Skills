---
name: pulseflow
description: Maintain a Markdown task dashboard backed by agent-written append-only AI work logs, then sync a daily AI DONE TODAY section plus a weekly usage panel via heartbeat or on-demand refresh. Use when building or operating a reusable task system where: (1) human tasks live in a single NOW.md dashboard, (2) agents automatically append work records after each completed work unit, (3) heartbeat scans logs and refreshes the AI-derived sections, (4) a new workspace or vault needs initialization with templates, paths, and sync state.
---

# PulseFlow

Build and operate a simple task system with one human-facing dashboard file and one append-only AI log flow.

## Core model

Use one current dashboard file as the source of truth for active work.

- Weekly usage lives in one top summary panel only: `AI USAGE THIS WEEK`
- Human work lives in four sections only: `FOCUS`, `TODAY`, `UP NEXT`, `DONE`
- AI work lives in one summary section only: `AI DONE TODAY`
- Agents do **not** write the dashboard directly
- Agents append one log line after each completed work unit
- Heartbeat or an explicit refresh reads usage data plus logs and rewrites the AI-derived sections

## File roles

Use these files and keep their roles strict:

- `todo/NOW.md` — current dashboard
- `todo/history/YYYY-MM.md` — monthly archive
- `todo/system/config.json` — installation-specific paths and agent list
- `todo/system/sync-state.json` — last processed offsets/checkpoints
- `reports/<agent>-ai-log-YYYY-MM-DD.jsonl` — append-only per-agent daily work logs

## Initialization workflow

When setting up a new installation:

1. Create `todo/`, `todo/history/`, and `todo/system/`
2. Create `todo/NOW.md` from the dashboard template in `references/now-template.md`
3. Create `todo/history/<current-month>.md` from `references/history-template.md` if missing
4. Create `todo/system/config.json` from `references/config-template.json`
5. Create `todo/system/sync-state.json` from `references/sync-state-template.json`
6. Fill installation-specific values:
   - dashboard path
   - history directory
   - reports directory per agent
   - optional `agentsFilePath` per agent
   - enabled agent list
   - timezone
7. If an older dashboard exists, migrate the human task sections into the new `todo/NOW.md`
8. Do not import old AI activity retroactively unless explicitly requested
9. Create today's empty AI log files for enabled agents
10. Install or refresh managed AI logging rules in configured `AGENTS.md` files
11. If the installation explicitly wants scheduled summaries, fill `notifications.summaryCrons` in config and run `scripts/install_summary_crons.js`

## Agent write contract

Each agent must append one JSON object per completed work unit to its own daily JSONL log.

Required fields:

- `ts` — ISO timestamp with timezone
- `agent` — agent name
- `task` — one-line work summary
- `tokens` — optional integer token count for that work unit; may be `0` or omitted

Example line:

```json
{"ts":"2026-04-05T14:10:00+08:00","agent":"main","task":"完成量化交易系统回测模块初版","tokens":12000}
```

Rules:

- Append only; never edit prior lines in-place
- Write after each completed work unit, not only at day end
- One line should be readable without extra context
- Do not depend on per-task token totals for daily usage accounting
- Do not write to `todo/NOW.md` directly from agents

## Heartbeat sync workflow

On heartbeat or explicit refresh:

1. Read `todo/system/config.json`
2. Read `todo/system/sync-state.json`
3. For each enabled agent, locate today's JSONL log
4. Parse all valid lines for today
5. Query OpenClaw usage summary for the current week and rebuild `AI USAGE THIS WEEK`
6. Rebuild the `AI DONE TODAY` section from the log contents for today
7. Compute today's total tokens from OpenClaw usage data, not by summing task lines
8. Rewrite only the AI-derived sections in `todo/NOW.md`
9. Update `todo/system/sync-state.json`

Important:

- Treat the dashboard AI section as a derived view, not a write-ahead log
- Rebuild from source logs for the current day instead of incrementally appending into Markdown
- Skip malformed lines; never let one bad line break the whole sync

## Dashboard format

Keep the dashboard simple and stable.

Top usage section:

- `## AI USAGE THIS WEEK`
- table columns: `Date / Total Tokens / Input / Output / Cache / Hit Rate`

Human task sections:

- `## FOCUS`
- `## TODAY`
- `## UP NEXT`
- `## DONE`

AI section:

- `## AI DONE TODAY`
- then bullet items formatted as:
  - `<agent>: <task>`

## Archive workflow

At end of day or next-day rollover:

1. Append completed human tasks and the AI section snapshot into `todo/history/YYYY-MM.md`
2. Update the month file's `AI Usage Daily Summary` block with finalized per-day usage rows
3. Group archived day entries by clipped week sections inside the month file, and keep one `AI Usage Weekly Summary` table per visible week block
4. Reset `DONE` in `todo/NOW.md`
5. Reset `AI DONE TODAY` for the new day on first sync
6. Rebuild `AI USAGE THIS WEEK` for the new current week
7. Move unfinished `FOCUS` and unfinished `TODAY` into the new day's `TODAY`
8. Keep unfinished `UP NEXT` unchanged
9. Reset `FOCUS` to an empty placeholder

## Scripts

- `scripts/append_ai_log.js` — appends one JSONL AI work record to today's per-agent log
- `scripts/install_agent_log_rules.js` — installs or updates managed AI log rule blocks in configured `AGENTS.md` files
- `scripts/install_summary_crons.js` — optionally installs or updates template-driven notification cron jobs from `notifications.summaryCrons` in config; these jobs supplement rollover and do not replace it
- `scripts/init_system.js` — creates missing dashboard, history, config, state files, today's empty AI logs, and installs managed agent log rules when configured; it does not install cron jobs by default
- `scripts/repair_system.js` — repairs missing runtime files without overwriting healthy ones
- `scripts/rollover_now.js` — daily rollover script; archives yesterday's human done + AI snapshot into a week-grouped month file, updates that week's `AI Usage Weekly Summary`, clears `DONE`, resets `AI DONE TODAY`, carries unfinished tasks forward, and updates `rollover-state.json`
- `scripts/sync_ai_done.js` — deterministic sync script for heartbeat or manual refresh; reads config, queries weekly usage, scans today's agent JSONL logs, rebuilds `AI USAGE THIS WEEK` plus `AI DONE TODAY`, and updates sync state
- `scripts/validate_system.js` — runs a local end-to-end validation covering init, sync, repair, rollover, and rollover idempotency

Run rollover with:

```bash
node <skill-dir>/scripts/rollover_now.js
```

Recommended scheduler:
- daily cron at `00:15` Asia/Shanghai

Run with:

```bash
node <skill-dir>/scripts/sync_ai_done.js
```

Optional config override:

```bash
AI_WORKLOG_CONFIG=/path/to/config.json node <skill-dir>/scripts/sync_ai_done.js
```

Validation:

```bash
node <skill-dir>/scripts/validate_system.js
```

Install or refresh agent rules:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_agent_log_rules.js
```

Optionally install or update summary cron jobs after filling `notifications.summaryCrons` in config:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js
```

Review the planned cron changes first with:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/install_summary_crons.js --dry-run
```

Recommended production invocation:

```bash
AI_WORKLOG_CONFIG=/absolute/path/to/todo/system/config.json node <skill-dir>/scripts/sync_ai_done.js
```

## Templates and references

Read these files as needed:

- `references/now-template.md` — base dashboard template
- `references/history-template.md` — monthly archive template
- `references/config-template.json` — install config shape, including optional summary-cron settings
- `references/sync-state-template.json` — sync checkpoint shape
- `references/agent-log-format.md` — log schema and examples
- `references/heartbeat-checklist.md` — heartbeat operating checklist
- `references/midday-summary-template.md` — optional 15:30 summary structure
- `references/daily-close-template.md` — optional 00:05 previous-day report structure, intended to run before rollover
- `docs/portability.md` — env overrides, installation assumptions, and optional cron-install notes

## Output standard

When asked to initialize, produce or update the installation files only.
When asked to sync, update only the AI-derived sections and sync state unless the user asks for more.
When asked to design or migrate, keep the system minimal and reusable; avoid installation-specific assumptions outside config.json.

## Runtime note

The JavaScript runtime is the only supported implementation.
