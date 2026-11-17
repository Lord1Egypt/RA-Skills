# Task Notifier - OpenClaw Plugin

Desktop notifications when any OpenClaw agent finishes a task.
Supports macOS and WSL-on-Windows. Works for all agents and subagents.
Smart suppression, auto-language, per-run state for parallel agents, and optional agent/subagent filters.

## Security and privacy notice

Task Notifier has two parts: this skill documentation and a separate runtime plugin. The runtime plugin is persistent until disabled or uninstalled.

Before installing, understand that the runtime plugin:

- installs code under `~/.openclaw/extensions/task-notifier/`;
- enables `task-notifier` in OpenClaw plugin config;
- adds `task-notifier` to `plugins.allow`;
- grants lifecycle hook access with `allowConversationAccess`;
- restarts the OpenClaw Gateway during setup;
- writes small per-run state files under each active workspace's `.openclaw-task/` directory;
- reads the active foreground app/window title to suppress notifications while OpenClaw is already active;
- runs local OS notification commands (`osascript`/`afplay` on macOS, PowerShell on WSL-on-Windows, `notify-send` on Linux fallback).

`allowConversationAccess` lets the plugin receive OpenClaw lifecycle hook context for conversations and agent turns. Task Notifier uses that context to detect user-initiated run start/end, identify the agent name, and filter heartbeat/cron/system-event turns. Install it only if you accept that persistent hook access across agents.

The notifier runtime does not need network access for sending desktop notifications. Installing or updating from ClawHub does use network access.

## Install

Review the source and the install command first. Then install only after explicit consent:

```bash
openclaw plugins install clawhub:task-notifier --dangerously-force-unsafe-install
```

The `--dangerously-force-unsafe-install` flag is required because the plugin intentionally runs local OS notification commands and registers lifecycle hooks. Treat it as a real security decision, not a cosmetic warning.

Restart and verify:

```bash
openclaw gateway restart
bash ~/.openclaw/extensions/task-notifier/scripts/doctor.sh
```

## Manual verification

Run diagnostics:

```bash
bash ~/.openclaw/extensions/task-notifier/scripts/doctor.sh
```

Send a test notification:

```bash
AGENT_NAME="Task Notifier Test" STATE_DIR=/tmp/task-notifier-test STATE_FILE=/tmp/task-notifier-test/runs/manual.env \
  ~/.openclaw/extensions/task-notifier/src/task-notify.sh done "Task Notifier test"
```

## Revert

To disable or remove the runtime plugin:

```bash
openclaw plugins disable task-notifier || true
openclaw plugins uninstall task-notifier || true
openclaw gateway restart
```

You can also delete stale per-run state from workspaces after uninstalling:

```bash
find ~/.openclaw/workspace -path '*/.openclaw-task/runs/*.env' -type f -delete
```

## Agent filters

By default Task Notifier watches the main agent and all subagents. Include/exclude entries match either the raw agent id or the display name, case-insensitively; spaces and underscores are treated like hyphens. Optional env settings:

```bash
export TASK_NOTIFIER_NOTIFY_MAIN=true
export TASK_NOTIFIER_NOTIFY_SUBAGENTS=true
export TASK_NOTIFIER_INCLUDE_AGENTS="main,forgemaster"
export TASK_NOTIFIER_EXCLUDE_AGENTS="noisy-agent,avito"
export TASK_NOTIFIER_AGENT_IN_BODY=true
export TASK_NOTIFIER_STATE_TTL_HOURS=24
```

State is stored per run/session under `.openclaw-task/runs/`, so parallel agents do not overwrite each other. The agent name is included in the title and body because Windows may display the notification source/app name as the visible header.

## Quick links

- **ClawHub:** https://clawhub.ai/skills/task-notifier
- **Install:** `clawhub install task-notifier`
- **License:** MIT-0
