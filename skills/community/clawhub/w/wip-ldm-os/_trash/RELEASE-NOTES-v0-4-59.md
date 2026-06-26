# Release Notes: wip-ldm-os v0.4.59

ldm install now deploys and manages LaunchAgents.

## What changed

- LaunchAgent plists ship in shared/launchagents/ and deploy to ~/Library/LaunchAgents/
- ldm install unloads old, writes new, loads new (automatic activation)
- Backup LaunchAgent fixed: log path from /tmp/ to ~/.ldm/logs/backup.log, PATH env var added
- Bug doc added for LaunchAgent management

## Why

LaunchAgents were manually placed files with hardcoded paths. When paths changed (migration), scripts broke (PID error), or logs went to /tmp/ (cleared on reboot), there was no way to fix them except manual editing. Now they're managed by the installer like rules, templates, and docs.

## Issues closed

- #236 (ldm install should deploy LaunchAgents)

## How to verify

```bash
npm install -g @wipcomputer/wip-ldm-os@latest
ldm init
launchctl list | grep ldm-backup
cat ~/Library/LaunchAgents/ai.openclaw.ldm-backup.plist | grep backup.log
```
