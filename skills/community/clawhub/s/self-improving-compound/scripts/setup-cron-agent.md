# Cron setup — agent instructions

Use this guide to install the self-improving compound maintenance pipeline in OpenClaw.

## What gets installed

`scripts/setup-cron.json` defines four recommended jobs:

| Job | Default schedule | Purpose |
|---|---:|---|
| Self-Improving Light Check | every 2h, 08:00–22:00 | Scan recent main-session history for missed corrections, failures, and reusable lessons. |
| Learning Audit Heavy | 09:00 and 22:00 | Audit system/cron failures, run `learning-audit.py --log`, and maintain HOT/WARM/COLD lifecycle. |
| Daily Memory Digest | 23:50 | Write `memory/YYYY-MM-DD.md` factual continuity notes, then extract reusable lessons. |
| Daily Workspace Steward | 00:20 | Export SQLite learning memory and lightly inspect `learning/`, `skills/`, and the 7 root Markdown control-plane files. |

The last two jobs are intentionally separated: the digest writes the daily factual record; the steward checks the surrounding operating state after the digest has landed.

## Prerequisites

- This skill is installed and the agent can read `scripts/setup-cron.json`.
- The agent has access to the OpenClaw `cron` tool.
- The user explicitly confirms creation or update of persistent cron jobs.
- Bash is available for the bundled `.sh` helpers. POSIX `sh`-only hosts should run the Python CLI commands directly instead of these helpers.

## Steps for the agent

1. **Read `scripts/setup-cron.json`.**
   If installed via ClawHub, the path is usually:
   `~/.openclaw/workspace/skills/self-improving-compound/scripts/setup-cron.json`

2. **Resolve runtime paths without hard-coding local machine paths:**
   - `OPENCLAW_WORKSPACE` should point to the workspace root.
   - `SELF_IMPROVING_LEARNING_ROOT` may point to a shared learning store used by multiple workspaces.
   - `SELF_IMPROVING_SKILL_DIR` may point to the installed skill directory.
   - `SELF_IMPROVING_LEARNINGS_CLI` may point to an explicit `learnings.py`.
   - `SELF_IMPROVING_MEMORY_PIPELINE` may point to `scripts/memory-pipeline.py` for Candidate → Learning → Promotion queues and dashboard.
   - `SELF_IMPROVING_MAIN_SESSION_KEY` may disambiguate the main conversation session for incremental transcript collection.
   - `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR` may point to an optional recent-conversation collector command for Light Check.
   - `SELF_IMPROVING_DAILY_COLLECTOR` may point to an optional daily-context collector command.

3. **Configure delivery.**
   The JSON ships with `delivery.bestEffort: true`. Ask or infer the delivery channel and recipient, then set fields such as `delivery.channel` and `delivery.to`.

4. **Check idempotency first.**
   Run `cron list`. If a job with the same name already exists, update it instead of creating a duplicate.

5. **Create/update jobs.**
   Use `cron add` for new jobs or `cron update` for existing jobs. Keep schedules as wall-clock time in `schedule.tz`.

6. **Verify.**
   Run `cron list` again. Each enabled job should have `nextRunAtMs` set and delivery configured as expected.

## Timezone

Defaults use `Asia/Shanghai`. If the user operates in another timezone, adjust `schedule.tz` before creating the jobs. Do not manually convert cron expressions to UTC; cron fields are local wall-clock time in the selected timezone.

## Safety

- These jobs may write local markdown and SQLite state. Ask before installing.
- The Workspace Steward must only make small, safe, local markdown updates. It must not rewrite persona files, weaken safety/privacy rules, delete files, or change cron jobs.
- Light Check should prefer the observable memory pipeline when available: collect incrementally, add candidates, log/mark learnings, add promotion items, refresh dashboard, then commit cursor. If a configured collector fails, report `BLOCKED: collector_unavailable` instead of pretending the context was scanned.
- Daily Memory Digest should not copy raw transcripts into `learning/`; it should extract compact reusable lessons only.
