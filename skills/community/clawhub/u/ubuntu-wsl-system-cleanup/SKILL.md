---
name: system-cleanup
description: Audit and safely clean Ubuntu 24.04 system junk, caches, logs, temp files, and unused local tool artifacts outside /mnt. Use when the user asks to clean the system, free disk space, remove caches, tidy packages, reclaim storage, or safely prune local Linux files on Ubuntu/WSL. Default to safe cleanup first; do not touch /mnt or destructive Docker data unless the user explicitly asks.
---

# System Cleanup

Audit disk usage first, then choose a cleanup level.

## Safety rules

- Never touch anything under `/mnt`.
- Default to **safe cleanup**.
- Do not remove user project files.
- Do not delete Docker images, containers, volumes, or builder cache unless the user explicitly asks for Docker cleanup.
- Prefer moving niche tool folders inside the workspace `_trash/` when cleanup should stay reversible.
- For package-manager caches and journals, direct deletion is acceptable after reporting what will be reclaimed.

## Cleanup levels

### 1. Safe cleanup
Use this by default.

Run these checks first:
- `df -h /`
- `du -xhd1 /root /var /usr 2>/dev/null | sort -h`
- `journalctl --disk-usage`
- `du -sh /var/cache/apt /var/lib/apt/lists ~/.npm ~/.cache ~/.local ~/.openclaw 2>/dev/null`

Then run the safe cleanup script:
- `bash /root/.openclaw/workspace/skills/system-cleanup/scripts/safe-clean.sh`

What safe cleanup does:
- `apt-get clean`
- remove old apt list cache files
- vacuum `systemd-journald`
- remove stale files from `/tmp` and `/var/tmp`
- clear npm cache
- clear user cache directories that are known caches
- report before/after sizes

### 2. Extended cleanup
Use when the user wants more aggressive cleanup but still safe for active development.

Possible targets after confirming with the user:
- old `_trash/` directories in the workspace
- stale pip caches
- obsolete `.npm/_npx`
- large tool caches under `/root/.cache`
- optional `docker system df` report

Read `references/targets.md` before extended cleanup.

### 2b. Second-round orphaned-tool cleanup
Use when the user asks to clean leftovers from tools that were already removed, or when you suspect tool dependencies, launchers, configs, caches, or generated data still remain after uninstalling a tool.

Read `references/orphaned-tool-patterns.md` before acting.

Checklist:
- find broken symlinks in `~/.local/bin`
- compare `~/.local/share/pipx/venvs` against active launchers in `~/.local/bin`
- search `~/.cache`, `~/.config`, `~/.local/share`, and workspace `_trash` for removed tool names
- search configs for stale references to removed tools

Default actions in this mode:
- delete broken symlinks
- delete caches clearly tied to removed tools
- delete stale `_trash` entries the user explicitly approved
- keep shared runtimes and shared browser/tool dependencies unless clearly orphaned

### 3. Docker cleanup
Only use when the user explicitly asks.

First inspect:
- `docker system df`
- `du -sh /var/lib/docker`

Then choose the least destructive command that matches the request, for example:
- `docker image prune -f`
- `docker builder prune -f`
- `docker system prune -f`
- `docker system prune -a --volumes -f` only with explicit user confirmation

## Reporting format

Always summarize:
- biggest directories found
- what was cleaned
- what was intentionally preserved
- estimated reclaimed space
- any follow-up recommendations

## Files to read when needed

- For cleanup targets and rationale: `references/targets.md`
- For execution: `scripts/safe-clean.sh`
