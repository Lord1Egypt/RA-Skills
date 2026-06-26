# Release Notes: memory-crystal v0.7.28

**Move all log paths from /tmp/ to ~/.ldm/logs/ so logs survive reboots.**

## What changed

- Cron entry for crystal-capture now logs to `~/.ldm/logs/crystal-capture.log` instead of `/tmp/ldm-dev-tools/`
- LaunchAgent plist template for ldm-backup now logs to `~/.ldm/logs/ldm-backup.log`
- `mkdirSync` ensures `~/.ldm/logs/` exists instead of creating `/tmp/ldm-dev-tools/`
- CLI output shows the correct log path

## Why

macOS clears `/tmp/` on every reboot. All cron and LaunchAgent logs were lost after restart, making it impossible to debug issues. `~/.ldm/logs/` persists across reboots and is the correct home for LDM OS logs.

## Issues closed

- wipcomputer/wip-ldm-os#120

## How to verify

```bash
# After install, check that cron entry points to ~/.ldm/logs/
crystal init --dry-run 2>&1 | grep crystal-capture

# Check backup setup points to ~/.ldm/logs/
crystal backup setup --dry-run 2>&1 | grep ldm-backup

# Verify logs land in the right place
ls ~/.ldm/logs/
```
