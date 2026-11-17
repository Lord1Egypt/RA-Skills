---
name: "Task Notifier"
description: "Tighten Task Notifier README consent and rollback docs."
---

# Task Notifier

Task Notifier is an OpenClaw notification helper. When the runtime plugin is installed, it sends a native desktop notification after an OpenClaw agent finishes a user-initiated task, unless OpenClaw is currently the active foreground window.

> For the AI agent: this skill is documentation and operating guidance. The actual desktop notification behavior requires the separate runtime plugin package.

## When to use this skill

Use this skill when the user explicitly asks to install, set up, configure, verify, debug, update, or uninstall Task Notifier, or explicitly asks for desktop notifications when OpenClaw agents finish work.

Do not treat generic mentions of notifications, alerts, reminders, desktop settings, or operating-system notification behavior as permission to install or configure Task Notifier. In those cases, answer the user's actual question first and only discuss Task Notifier if it is clearly relevant.

## Safe setup workflow

If the user asks to set up or check Task Notifier, first check whether the runtime plugin is installed:

```bash
test -f ~/.openclaw/extensions/task-notifier/src/index.js && echo installed || echo missing
```

If it is missing, explain plainly:

> Task Notifier needs its runtime plugin to send desktop notifications. The skill only documents the workflow; the plugin is the code that registers OpenClaw lifecycle hooks and calls local OS notification commands.

Before installing, get explicit user confirmation. Tell the user what the install changes:

- downloads the runtime plugin to `~/.openclaw/extensions/task-notifier/`;
- enables `task-notifier` in OpenClaw plugin config;
- adds it to `plugins.allow`;
- grants lifecycle hook access with `allowConversationAccess`;
- requires `--dangerously-force-unsafe-install` because the plugin intentionally runs local notification commands.

The flag is a real security decision, not a cosmetic warning. The runtime plugin is designed to use local OS notification tools (`osascript` on macOS, PowerShell on WSL-on-Windows, and `notify-send` on Linux fallback), inspect the active foreground window title for suppression, and write small per-run state files under the active workspace's `.openclaw-task/` directory. The runtime itself does not need network access for notifications, but installing or updating from ClawHub uses network access.

Privacy note: `allowConversationAccess` lets the runtime receive OpenClaw lifecycle hook context for conversations and agent turns. Task Notifier uses that context only to decide when a user-initiated agent run started/ended, identify the agent name, and avoid heartbeat/cron/system-event noise. Do not install it unless the user explicitly accepts persistent lifecycle hook access across agents.

After explicit approval, install the runtime plugin:

```bash
openclaw plugins install clawhub:task-notifier --dangerously-force-unsafe-install --force
```

Then restart the gateway and run the doctor:

```bash
openclaw gateway restart
bash ~/.openclaw/extensions/task-notifier/scripts/doctor.sh
```

To revert the runtime install later:

```bash
openclaw plugins disable task-notifier || true
openclaw plugins uninstall task-notifier || true
openclaw gateway restart
```

## How it works

The runtime plugin registers OpenClaw lifecycle hooks:

1. `before_prompt_build` detects a new user-initiated turn, filters out heartbeat, cron, and system-event turns, applies agent filters, and writes a per-run marker to `<agent-workspace>/.openclaw-task/runs/<runId>.env`.

2. `agent_end` reads that run marker, checks whether OpenClaw is the active foreground window, sends a native desktop notification when OpenClaw is not active, and then cleans up the marker.

The plugin tracks runs separately by run/session key so parallel agents do not overwrite each other. It works for the main agent and subagents unless filtered by environment variables.

## Smart suppression

If OpenClaw's web interface is the active foreground window, the runtime suppresses the notification. If the user has switched away, it sends the notification.

Probe the current foreground-window detection:

```bash
~/.openclaw/extensions/task-notifier/src/task-notify.sh probe
```

If notifications fire while the user is looking at OpenClaw, configure a distinctive active-window title fragment:

```bash
export TASK_NOTIFIER_ACTIVE_MATCH="openclaw|localhost:18789|127.0.0.1:18789|my openclaw window title"
```

## Verification

Run the doctor:

```bash
bash ~/.openclaw/extensions/task-notifier/scripts/doctor.sh
```

Send a manual test notification:

```bash
AGENT_NAME="Test" STATE_DIR=/tmp/task-notifier-test STATE_FILE=/tmp/task-notifier-test/runs/manual.env \
  ~/.openclaw/extensions/task-notifier/src/task-notify.sh start

AGENT_NAME="Test" STATE_DIR=/tmp/task-notifier-test STATE_FILE=/tmp/task-notifier-test/runs/manual.env \
  ~/.openclaw/extensions/task-notifier/src/task-notify.sh done "Task Notifier test"
```

If OpenClaw is active, the `done` command may report `notification suppressed: OpenClaw is active`. To test the notification path deliberately, set a non-matching active-window expression for that one command:

```bash
TASK_NOTIFIER_ACTIVE_MATCH="__never_match_openclaw__" \
AGENT_NAME="Test" STATE_DIR=/tmp/task-notifier-test STATE_FILE=/tmp/task-notifier-test/runs/manual.env \
  ~/.openclaw/extensions/task-notifier/src/task-notify.sh done "Task Notifier test"
```

## WSL-on-Windows notes

This mode is for setups where OpenClaw Gateway runs inside WSL, but the browser and desktop are native Windows apps.

Requirements:

- Windows PowerShell must be reachable from WSL. The script checks `powershell.exe`, `pwsh.exe`, and `/mnt/c/Windows/System32/WindowsPowerShell/v1.0/powershell.exe`.
- WSL must have access to `/mnt/c`.
- Windows notifications must not be blocked by Focus Assist or Do Not Disturb.

The active-window check uses the real Windows foreground window via Win32 API, not Linux-only tools like `xdotool`.

## Language support

Auto-detects the system language:

- macOS: `defaults read -g AppleLocale`
- WSL-on-Windows: Windows UI culture via PowerShell
- fallback: `LC_ALL` / `LANG`

Supported notification languages:

- Russian: `Задача выполнена`
- Ukrainian: `Завдання виконано`
- German: `Aufgabe erledigt`
- English: `Task completed`

Override language detection with:

```bash
export LANG_CODE=en
```

## Configuration

| What | How |
|------|-----|
| Language override | `export LANG_CODE=en` |
| Active-window matching | `export TASK_NOTIFIER_ACTIVE_MATCH="openclaw|localhost:18789|my title"` |
| Disable main agent notifications | `export TASK_NOTIFIER_NOTIFY_MAIN=false` |
| Disable subagent notifications | `export TASK_NOTIFIER_NOTIFY_SUBAGENTS=false` |
| Notify only selected agents | `export TASK_NOTIFIER_INCLUDE_AGENTS="main,forgemaster"` |
| Exclude selected agents | `export TASK_NOTIFIER_EXCLUDE_AGENTS="noisy-agent,avito"` |
| Hide agent name in notification body | `export TASK_NOTIFIER_AGENT_IN_BODY=false` |
| Stale state cleanup | `export TASK_NOTIFIER_STATE_TTL_HOURS=24`; set `0` to disable |

Agent filters match raw agent id or display name after simple normalization.

## Use cases

- Step away from the desk while OpenClaw handles a long task.
- Get notified when subagents finish background work.
- Monitor batch processing or multi-agent workflows without staring at the web UI.
- Reduce notification spam by suppressing alerts while OpenClaw is already active.

## Technical details

- OS support: macOS, WSL-on-Windows, and basic Linux fallback.
- macOS notifications use `osascript` and `afplay`.
- WSL-on-Windows notifications use Windows PowerShell to inspect the foreground window and send a tray notification.
- Linux fallback uses `notify-send` when available.
- Runtime state lives in `<workspace>/.openclaw-task/runs/<run-or-session-key>.env` and is cleaned up after completion.
- Agent name/id resolution uses session metadata, agent id, workspace path, and `IDENTITY.md` fallback for the main agent.
- Trigger filter ignores heartbeat, cron, and system events.
- Completion hook: `agent_end`.

## Files in the runtime package

| File | Purpose |
|------|---------|
| `src/index.js` | Runtime plugin entry and lifecycle hooks |
| `src/index.ts` | TypeScript source for the runtime plugin |
| `src/task-notify.sh` | Cross-platform notification dispatcher |
| `scripts/install-plugin.sh` | Installer/configurator helper |
| `scripts/doctor.sh` | Platform, config, hook, and focus diagnostic helper |
| `openclaw.plugin.json` | Plugin manifest for OpenClaw |
| `package.json` | npm package metadata |
| `SKILL.md` | Agent-facing documentation |
| `README.md` | Human-facing readme |
| `LICENSE` | MIT-0 |

## Keywords

task notification, agent completion, macOS alerts, desktop notification, OpenClaw plugin, background monitoring, task done alert, work complete, AI agent notifier, productivity tool, multi-agent support, subagent notifications, sound alert, smart suppression, hands-free workflow, auto-language, Russian notifications, German notifications
