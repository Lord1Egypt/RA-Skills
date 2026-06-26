---
name: windows-notifier
description: Send native Windows desktop notifications for local reminders, alerts, and background-attention events. Use when the user wants a Windows popup, a local toast notification, or when reminder/alert messages should prefer local desktop notification instead of only chat delivery.
---

# Windows Notifier

Send a local **Windows desktop notification** on this machine.

This skill is a Windows-focused alias/wrapper around the shared desktop notification flow so agents can trigger a popup consistently when the user asks for a Windows reminder or when a reminder/alert should not rely only on chat visibility.

## Use this skill for

- Local reminder popups
- Timer / study / schedule alerts
- Attention-needed notifications when chat may be in the background
- Windows-specific notification tests

## Command

Run this from PowerShell with `exec`:

```powershell
node "$env:USERPROFILE\.openclaw\workspace\skills\windows-notifier\scripts\send-notification.js" --title "<TITLE>" --message "<MESSAGE>" --timeout 10
```

Modern card / persistent dialog mode also goes through the same JS entry:

```powershell
node "$env:USERPROFILE\.openclaw\workspace\skills\windows-notifier\scripts\send-notification.js" --title "<TITLE>" --message "<MESSAGE>" --mode modern --appName "OpenClaw"
```

Behavior summary:
- **Windows + WPF available** → prefer the built-in WPF modern card path in `send-notification.js`
- **Windows fallback** → if WPF is unavailable or launch fails, automatically fall back to `node-notifier`
- **Linux / macOS** → use the existing `node-notifier` path
- Current modern card behavior: auto-close after about 60 seconds; click the card itself to dismiss

Optional flags:

- `--wait true|false`
- `--timeout <seconds|false|permanent>`
- `--sound true|false` (default: `true`)
- `--mode modern|card|dialog`
- `--appName <name>`

## Notes

- Keep the title short and the message concise.
- On Windows, `--mode modern|card|dialog` prefers the built-in WPF modern card path when available, and otherwise falls back to `node-notifier` automatically.
- `--timeout false|permanent|sticky|0` is treated as a persistent request intent, but final behavior depends on the active backend (built-in WPF on capable Windows, otherwise `node-notifier`).
- Prefer this over chat-only reminders when the request is for a local popup.
- If a reminder or alert may be missed because OpenClaw is running in the background, prefer triggering this notifier in addition to or instead of chat delivery, depending on user intent.
- `node-notifier` remains the default non-Windows path and the cross-platform fallback mechanism.
- On first run after install, the script auto-installs dependencies in this skill directory if needed, so users do not need to run npm manually.
