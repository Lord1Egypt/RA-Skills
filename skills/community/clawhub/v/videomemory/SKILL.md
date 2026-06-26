---
name: videomemory
description: Start VideoMemory from OpenClaw and return the local UI link.
homepage: https://github.com/Clamepending/videomemory
metadata: {"openclaw":{"emoji":"camera"}}
---

# VideoMemory Setup

Use this skill when the user wants OpenClaw to install, start, relaunch, or check VideoMemory.

For requests like "install videomemory please", "set up videomemory", or "Install the VideoMemory skill from ClawHub and send me the UI", prefer installing the OpenClaw plugin package. If the plugin install path is unavailable, run the safe onboarding command and reply with the returned UI link.

## Preferred Commands

First-class plugin install:

```bash
openclaw plugins install @clamepending/videomemory@0.1.7
```

After the plugin is installed and the gateway has restarted, prefer the plugin tools:
- `videomemory_onboard`
- `videomemory_relaunch`
- `videomemory_status`

CLI fallback from the OpenClaw workspace root after `clawhub install videomemory`, inspect the onboarding plan:

```bash
npx -y @clamepending/videomemory@0.1.7 onboard --safe --repo-ref v0.1.3 --explain
```

If the plan matches the user's request, run onboarding:

```bash
npx -y @clamepending/videomemory@0.1.7 onboard --safe --repo-ref v0.1.3
```

Relaunch:

```bash
npx -y @clamepending/videomemory@0.1.7 relaunch --repo-ref v0.1.3
```

Check status:

```bash
curl -fsS http://127.0.0.1:5050/api/health
```

## What Onboarding Does

- Starts VideoMemory without Docker.
- Installs the OpenClaw bridge files used by VideoMemory.
- Returns the user-facing VideoMemory UI link.
- Runs in safe mode, avoiding network-exposure setup, chat notifications, and privileged setup paths.

## Ground Rules

- Prefer the published VideoMemory CLI command above over hand-written setup commands.
- Prefer `openclaw plugins install @clamepending/videomemory@0.1.7` when OpenClaw plugin installation is allowed.
- Run `--safe --explain` before onboarding when acting from chat.
- If onboarding or relaunch fails, report the actual stderr instead of guessing.
- After a successful onboarding or relaunch, reply with the returned UI link.
