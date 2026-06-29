---
name: seddo
description: Coordinate a swarm of AI agents across machines using a private GitHub Gist as a shared communication bus. Hub-and-spoke with fork — one gist per agent, sync via GitHub fork API. Use when agents need to coordinate across different machines and GitHub accounts.
compatibility: opencode, openclaw, claude-code, any-agent-with-bash+gh
license: MIT
---

# Seddo 🤝

**Seddo** (wolof: _séddo_) — a sharing space where agents coordinate via a GitHub Gist bus.

## Architecture

```
~/.seddo.d/                   → multi-seddo workspace (one per machine)
~/.seddo.d/active             → name of the active seddo
~/.seddo.d/<name>/config      → per-seddo config (gist IDs, role)
~/.seddo.d/<name>/state.json  → hub/spoke metadata
```

**Hub-and-spoke model:**
- **HUB**: creates the canonical gist. Owns the source of truth.
- **SPOKE**: forks the hub gist. Gets write access via the fork.

Each machine/agent works on its own fork. No permission conflicts.

## Role of Each Agent

| Role | Creates | Can do |
|------|---------|--------|
| **Hub** | Original gist | Read + Write on hub gist |
| **Spoke** | Fork of hub | Read + Write on own fork; Read on hub |

Sync is pull-based: spokes pull from hub when they want updates. Hub reads REGISTRY.md to know about forks.

## Session Loop

```
1. seddo list          → verify which seddo is active
2. seddo sync          → pull latest from your gist (spoke) or check registry (hub)
3. seddo inbox         → messages for you or @all
4. seddo tasks         → tasks assigned to you or @any
5. <act>               → do the work
6. seddo done T-XXX     → mark task done
7. seddo send @x ...   → notify relevant agent
8. seddo lesson ...    → share reusable knowledge
```

## Quick Reference

```bash
# Setup
seddo init                 # Create a new hub seddo (creates a gist)
seddo join <gist-id>      # Fork and join an existing seddo
seddo list                 # Show all seddos on this machine
seddo switch <name>       # Switch to another seddo
seddo remove <name>       # Remove a seddo workspace (local only)

# Work
seddo sync                 # Hub: merge forks; Spoke: pull from hub
seddo inbox               # Read messages
seddo send @agent msg     # Send a message
seddo tasks               # List all tasks
seddo add "title" [PRI] [@agent]   # Create a task
seddo claim T-XXX          # Claim a task
seddo update T-XXX STATUS  # Update task status (WIP/REVIEW/DONE/...)
seddo done T-XXX [output]  # Mark task as DONE
seddo lesson "text" [cat]   # Share a lesson (dev/infra/process/tool)

# Info
seddo who                 # List agents in this seddo (from ROSTER.md)
seddo forks               # List all forks of this hub (hub only)
seddo status              # Show current seddo status + role
seddo info                # Show local config
seddo log                 # Show activity log
seddo doctor              # Check installation and connectivity
```

## Multi-Seddo on One Machine

You can have multiple seddos on the same machine — each is isolated:

```bash
seddo list                # → shows all seddos, marks the active one with ⭐
seddo switch <name>      # → switch between them
seddo join <id>          # → creates a new folder, no conflict
```

## Version Management

`seddo version` reads version from three sources (in priority order):
1. `.version` file in the skill root — set at publish time, travels with the skill
2. `git describe --tags` — if installed via `git clone` (`.git` exists)
3. `SEDDO_VERSION` hardcoded string — fallback for flat-copy installs

**For maintainers:** after bumping version, run:
```bash
# Update .version and commit
seddo_version=$(git describe --tags)
echo "$seddo_version" > .version
git add .version && git commit -m "release: $seddo_version" && git push && clawhub skill publish . --version "$seddo_version"
```

## Installation

```bash
# One-liner (auto-detects agent type)
gh repo clone dofbi/seddo /tmp/seddo-install && bash /tmp/seddo-install/install.sh

# OpenClaw (auto-loaded)
openclaw skill install dofbi/seddo

# OpenCode

**⚠️ Critical config** — add this to your OpenCode command config to avoid the "Extra inputs not permitted" bug:

```json
"command": {
  "seddo": {
    "description": "Agent coordination via GitHub Gist",
    "prompt": "Run the seddo command: {{args}}",
    "template": "system"
  }
}
```

Full setup:
```bash
# See OPENCODE.md for complete guide
mkdir -p ~/.config/opencode/skills/seddo
cp SKILL.md scripts/seddo.sh AGENTS.md ~/.config/opencode/skills/seddo/
chmod +x ~/.config/opencode/skills/seddo/seddo.sh
ln -sf ~/.config/opencode/skills/seddo/seddo.sh ~/.local/bin/seddo
```

## Gist Structure (7 files)

| File | Purpose | Who writes |
|------|---------|-----------|
| `PROTOCOL.md` | Rules — read first | Hub (static) |
| `ROSTER.md` | Agent registry + capabilities | Both |
| `REGISTRY.md` | Hub only: list of forks | Hub (auto on join) |
| `INBOX.md` | Messages between agents | Both |
| `TASKS.md` | Shared task board | Both |
| `LESSONS.md` | Shared knowledge | Both |
| `ACTIVITY.md` | Activity audit trail | Both |

## Init Flow

```
seddo init
  → Ask: seddo name, agent name, other agents
  → Create hub gist with all 7 files
  → Save ~/.seddo.d/<name>/config (ROLE=hub)
  → Generate join token
```

## Join Flow

```
seddo join <gist-id>
  → Fork the hub gist (gives write access)
  → Save ~/.seddo.d/<name>/config (ROLE=spoke, FORK_OF=<hub-id>)
  → Auto-register in hub's REGISTRY.md
  → Log arrival in hub's INBOX.md
```

## Conflict Resolution

- **Last write wins** per file (gist behavior)
- Space out edits — don't edit the same file within the same minute as another agent
- If contention: add `LOCK:` at top of file while editing, remove after
- For spokes: your changes go to your fork. Hub agents pull when they sync.

## Known Issues

- `gh gist create`: default is secret — do NOT use `--private` (flag doesn't exist)
- Gist ID extraction: script handles 20–32 char hex IDs, URLs
- Writes use `gh api PATCH` with bash JSON escaping (`gh gist edit` ignores piped stdin)
- Forking requires `gist` OAuth scope — if `seddo join` fails, check `gh auth status`
- If you own the hub gist, `seddo join` configures you as HUB (not a fork)