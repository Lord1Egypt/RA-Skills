# Scheduled Tasks

cc-use can register local recurring tasks for long-running project supervision.
The schedule feature has two modes:

- `heartbeat`: periodically checks that a persistent inner tmux session is
  healthy and responsive.
- `cron`: runs a scheduled prompt or executable script at a calendar time.

Use schedules only when the user explicitly asks to keep a recurring local task
running. Schedules are host-local state. They are not portable by themselves and
should be migrated deliberately per machine.

## Storage And Registration

cc-use stores schedule records under:

```text
~/.cc-use/schedules.json
~/.cc-use/logs/
```

The helper also registers the task with the host scheduler:

- macOS: launchd plist files under `~/Library/LaunchAgents/`.
- Linux: user crontab entries marked with `#cc-use:<id>`.

The registered command calls back into the installed helper:

```bash
<skill_dir>/scripts/cc-use schedule-run <id>
```

This means the schedule behavior follows the installed cc-use skill code. If
the helper path changes during migration, update the launchd or crontab entry.

## Agent Selection

Schedules are agent-neutral. By default, `--agent auto` uses the same agent
family as the outer session that creates the schedule. You may also pass an
explicit supported agent family when the user asks for one.

For scheduled tasks, the default execution policy is intentionally broad:

```text
sandbox = danger-full-access
approval = never
```

This avoids recurring tasks getting stuck on routine filesystem or network
access. Use narrower settings only when the user asks for that tradeoff.

For Codex schedules, `--profile NAME` is supported and stored in the schedule
record. Scheduled Codex `exec` runs include `--skip-git-repo-check` so tasks can
run from ordinary project or script directories that are not git repositories.

## Heartbeat

Create or reuse a heartbeat schedule:

```bash
<skill_dir>/scripts/cc-use schedule-add heartbeat NAME \
  --project "$PWD" \
  --interval-minutes 15 \
  --agent auto \
  --session ccu-my-project
```

Important options:

- `NAME`: human-readable schedule name.
- `--project DIR`: project root for state and tmux session derivation.
- `--interval-minutes N`: run interval. Default is `15`.
- `--agent auto`: use the same agent family as the creator.
- `--profile NAME`: Codex profile, when the user explicitly asks for one.
- `--session NAME`: explicit tmux session name.

On first creation, cc-use creates this project-local file if missing:

```text
<project>/.cc-use/heartbeat.md
```

The heartbeat runner delegates the heartbeat text to the persistent inner tmux
session and records the latest state under:

```text
<project>/.cc-use/heartbeat-state.json
```

The heartbeat should be small and cheap. It should ask the inner session to
report whether it is healthy, blocked, or needs attention.

## Cron

Create a cron-style scheduled task:

```bash
<skill_dir>/scripts/cc-use schedule-add cron NAME \
  --project "$PWD" \
  --cron-expr "30 22 * * *" \
  --prompt "Read ./daily-report.md and follow the instructions." \
  --agent auto
```

For a script-backed task, pass the executable script path as the prompt:

```bash
<skill_dir>/scripts/cc-use schedule-add cron NAME \
  --project "$PWD" \
  --cron-expr "30 22 * * *" \
  --prompt "$PWD/.cc-use/daily-report.sh" \
  --agent auto
```

If the prompt is an executable file path, `schedule-run` executes the script
directly. Otherwise, it sends the prompt to the selected non-interactive agent
runner.

Use `--search` when the scheduled Codex task should enable web search:

```bash
<skill_dir>/scripts/cc-use schedule-add cron NAME \
  --project "$PWD" \
  --cron-expr "30 9 * * 5" \
  --prompt "Read ./weekly-report-prompt.md and follow the instructions." \
  --agent codex \
  --profile zilliz \
  --search
```

## Inspecting And Operating Schedules

List schedules:

```bash
<skill_dir>/scripts/cc-use schedule-list
```

Show all schedules or one schedule with its latest log tail:

```bash
<skill_dir>/scripts/cc-use schedule-status
<skill_dir>/scripts/cc-use schedule-status <id>
```

Manually trigger a schedule:

```bash
<skill_dir>/scripts/cc-use schedule-run <id>
```

Remove a schedule and unregister it from the host scheduler:

```bash
<skill_dir>/scripts/cc-use schedule-remove <id>
```

## Environment

Scheduled tasks run outside the user's interactive terminal. The runner loads
simple exported variables from common shell startup files without executing
arbitrary startup commands. This keeps scheduled runs from triggering unrelated
interactive shell side effects.

The temporary environment file is created with owner-only permissions and is
removed after loading. Do not hardcode user-specific secret variable names in
the skill. If a task needs a secret, the user should describe the requirement
when creating that local schedule.

## Migration

When migrating schedules from another host or another helper path:

1. Back up `~/.cc-use/schedules.json`.
2. Back up the current launchd plist files or crontab.
3. Copy or transform schedule records into the new `schedules.json`.
4. Ensure each record has the intended `agent`, `profile`, `sandbox`, and
   `approval` fields.
5. Rewrite launchd or crontab entries so they call the current
   `<skill_dir>/scripts/cc-use schedule-run <id>`.
6. Run `schedule-list`.
7. Manually run representative schedules with `schedule-run <id>`.

For migrating existing local tasks to Codex with a profile, set:

```text
agent = codex
profile = zilliz
sandbox = danger-full-access
approval = never
```

Then test at least one heartbeat and one cron task manually before relying on
the host scheduler.

## Troubleshooting

Use the schedule log first:

```bash
tail -120 ~/.cc-use/logs/cron-<id>.log
tail -120 ~/.cc-use/logs/heartbeat-<id>.log
```

Common failures:

- The helper path in launchd or crontab points to an old installation.
- The scheduled shell environment does not include a required secret.
- The project path no longer exists.
- The prompt path is not executable when a script-backed cron task is expected.
- The selected profile does not exist on that host.

After fixing the issue, rerun:

```bash
<skill_dir>/scripts/cc-use schedule-run <id>
```
