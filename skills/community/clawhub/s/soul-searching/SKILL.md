---
name: soul-searching
description: "Browse, install, switch, and manage SOUL.md personality files for OpenClaw agents from the soulsearching.ai directory. Use when a user asks to: install a soul or personality, switch souls, list installed souls, browse available souls, check current soul, uninstall a soul, or anything related to SOUL.md management. Triggers on: install soul, switch soul, change personality, browse souls, soul search, what soul, current soul, list souls, remove soul, uninstall soul, personality file."
---

# Soul Searching — SOUL.md Manager

Manage SOUL.md personality files from [soulsearching.ai](https://soulsearching.ai).

## Commands

All commands use `scripts/soul.sh` in this skill's directory.

### Browse available souls

```bash
./scripts/soul.sh browse [category]
```
Categories: `professional`, `creative`, `technical`, `funny`, `specialized`, or omit for all.

### Search souls

```bash
./scripts/soul.sh search <query>
```

### Install a soul

```bash
./scripts/soul.sh install <soul-id> [--activate]
```
Downloads from soulsearching.ai and saves to `~/.openclaw/souls/<id>.md`.
With `--activate`, also copies to the workspace `SOUL.md`.

### Switch to an installed soul

```bash
./scripts/soul.sh switch <soul-id>
```
Backs up current `SOUL.md` → `SOUL.md.bak`, then copies the installed soul into place.

### List installed souls

```bash
./scripts/soul.sh list
```

### Show current soul

```bash
./scripts/soul.sh current
```

### Uninstall a soul

```bash
./scripts/soul.sh uninstall <soul-id>
```

### Refresh catalog

```bash
./scripts/soul.sh refresh
```
Re-downloads the catalog from soulsearching.ai.

## Workflow

1. Run `browse` or `search` to find a soul
2. Run `install <id> --activate` to install and activate in one step
3. Use `switch` to swap between previously installed souls
4. Use `current` to check what's active

## Notes

- Souls are cached locally in `~/.openclaw/souls/`
- The catalog is cached at `~/.openclaw/souls/.catalog.json` (auto-refreshes if >24h old)
- `switch` always backs up the current SOUL.md before overwriting
- The workspace SOUL.md path is auto-detected (current directory or `$OPENCLAW_WORKSPACE`)
