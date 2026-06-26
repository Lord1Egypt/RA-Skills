# 🔔 Task Notifier — OpenClaw Plugin

Desktop notifications when any OpenClaw agent finishes a task.
Supports macOS and WSL-on-Windows. Works for all agents and subagents.
Smart suppression, auto-language, per-run state for parallel agents, and optional agent/subagent filters.

## Install

```bash
openclaw skills install task-notifier
bash ~/.openclaw/workspace/skills/task-notifier/scripts/install-plugin.sh
```

The installer enables the bundled runtime plugin, adds `task-notifier` to
`plugins.allow`, grants lifecycle hook access, and restarts the Gateway.

Run diagnostics:

```bash
bash ~/.openclaw/extensions/task-notifier/scripts/doctor.sh
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
