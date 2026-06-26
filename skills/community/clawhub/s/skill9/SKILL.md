---
name: skill9
description: Cloud-synced skill vault — backup, version, and sync your AI agent skills across machines and platforms. Use when user wants to backup, sync, version-control, or migrate their skills.
compatibility: Requires curl or wget for installation
---

# skill9 — Your Skills, Everywhere

skill9 backs up, versions, and syncs your AI agent skills across machines and platforms.

## Routing

| Intent | Read |
|--------|------|
| Install, configure, reconnect, first-time setup | [`SETUP.md`](https://skill9.ai/SETUP.md) |
| Uninstall, remove, disable, roll back | [`UNINSTALL.md`](https://skill9.ai/UNINSTALL.md) |

## Commands

All commands support `--json` and `--platform <name>`.

| Command | Description |
|---------|-------------|
| `skill9 push [name] [--all]` | Push skill(s) to cloud (creates new version) |
| `skill9 push --delete <name>` | Delete a skill from cloud |
| `skill9 pull [name] [--all]` | Pull skill(s) from cloud to local |
| `skill9 list` | List local and cloud skills |
| `skill9 status` | Show sync status |
| `skill9 log <name>` | View version history |
| `skill9 diff <name> <v1> <v2>` | Compare two versions |
| `skill9 rollback <name> <ver>` | Restore a previous version |
