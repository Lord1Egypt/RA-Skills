---
name: solcal-recovery
description: OpenClaw repair toolkit — automated diagnostics, backup/restore, and guided AI-assisted recovery.
version: 1.0.0
author: TheSolAI
permissions: ["shell.exec", "file.read", "file.write"]
---

# SolCal Recovery

A beginner-friendly repair toolkit for OpenClaw AI agents. Get back online fast when things go wrong — with automated diagnostics, AI-assisted repair, and one-click restore.

## Triggers

Use when:
- OpenClaw won't start or crashes on launch
- Skills aren't loading or behaving unexpectedly
- After a system update or config change that broke things
- The agent is giving errors or behaving incorrectly
- Regular maintenance and health checks

## Actions

- **Diagnostics** — Run automated checks on: config files, skill loading, API keys, network connectivity, disk space
- **AI Repair** — Use Ollama or another LLM to diagnose the specific error and suggest fixes
- **Backup** — Snapshot all OpenClaw data: workspace, memory, config, skills
- **Restore** — Roll back to a previous backup state
- **Emergency Reset** — Nuclear option to reset to clean state while preserving workspace
- **Quick Start** — Safe launch sequence with pre-flight checks

## Scripts Included

| Script | Purpose |
|---|---|
| `SolCal-Recovery.sh` | Main diagnostic + AI repair runner |
| `start-sol.sh` | Quick safe start |
| `save-sol.sh` | Full backup |
| `restore-sol.sh` | Restore from backup |
| `emergency-repair.sh` | Reset to clean state |
| `ai-repair.sh` | Ask LLM for diagnosis |

## Requirements

- OpenClaw installed
- `gh` CLI authenticated (for GitHub workspace restore)
- Ollama (optional, for AI-assisted repair)
