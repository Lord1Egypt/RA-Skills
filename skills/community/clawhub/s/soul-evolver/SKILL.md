---
name: soul-evolver
description: "soul-evolver - AI Agent Memory Evolution System. Automatically analyzes memory files and evolves SOUL.md, USER.md, IDENTITY.md, and other workspace identity files using MiniMax API. Triggers when: agent accumulates new patterns in memory/*.md or .learnings/, needs to update behavioral guidelines, discovers recurring user preferences, or evolves team workflows. Use when: you want your AI to become smarter over time automatically, need to propagate learnings across sessions, or want automatic identity file maintenance. NOT for: one-shot tasks, real-time responses, or when manual curation is preferred."
metadata:
  openclaw:
    requires:
      bins:
        - python3
    env:
      MINIMAX_API_KEY:
        description: MiniMax API key for pattern analysis
        required: true
    hooks:
      soulforge-evolve:
        description: "Scheduled memory evolution: reads memory/*.md, analyzes patterns with MiniMax, updates SOUL.md/USER.md/IDENTITY.md"
        type: agentTurn
        session: isolated
        schedule: every 120m
---

# soul-evolver Skill

soul-evolver automatically evolves your AI agent's identity files by analyzing memory sources and discovering patterns over time.

## When to Use

- After significant conversations that reveal new behavioral patterns
- When USER.md or SOUL.md needs updating based on accumulated experience
- During periodic memory reviews (scheduled or manual)
- After the user provides corrections or new preferences

## Quick Start

### Run Manual Evolution

```
exec python3 ~/.openclaw/skills/soul-forge/scripts/soulforge.py run
```

### Dry Run (Preview Changes)

```
exec python3 ~/.openclaw/skills/soul-forge/scripts/soulforge.py run --dry-run
```

### Check Status

```
exec python3 ~/.openclaw/skills/soul-forge/scripts/soulforge.py status
```

## Multi-Agent Isolation

SoulForge is designed for multi-agent environments. Each agent's data is **completely isolated**:

| Data | Isolation Strategy |
|------|-------------------|
| Backup files | `.soulforge-{agent}/backups/` — agent-specific subdirectory |
| State files | `.soulforge-{agent}/` — agent-specific directory |
| Memory sources | Read only from agent's own `memory/` and `.learnings/` |
| Target files | Update only agent's own SOUL.md, USER.md, etc. |

**Example: workspace naming**
```
~/.openclaw/workspace/         → .soulforge-main/     (main agent)
~/.openclaw/workspace-wukong/  → .soulforge-wukong/  (wukong agent)
~/.openclaw/workspace-tseng/   → .soulforge-tseng/   (tseng agent)
```

Each agent should run its own cron job pointing to its workspace:
```bash
# For main agent
python3 soulforge.py run --workspace ~/.openclaw/workspace

# For wukong agent
python3 soulforge.py run --workspace ~/.openclaw/workspace-wukong
```

## Configuration

Set your MiniMax API key:

```bash
export MINIMAX_API_KEY="your-api-key"
```

Or in OpenClaw config:

```json
{
  "env": {
    "MINIMAX_API_KEY": "your-key"
  }
}
```

## How It Works

```
memory/*.md + .learnings/ → MiniMax Analysis → Pattern Discovery → File Updates
```

### Trigger Conditions

soul-evolver updates files when:

| File | Triggers |
|------|----------|
| SOUL.md | Same behavior seen 3+ times, user corrections, new principles |
| USER.md | New user preferences, project changes, habit changes |
| IDENTITY.md | Role/responsibility changes, team structure changes |
| MEMORY.md | Important decisions, milestones, lessons learned |
| AGENTS.md | New workflow patterns, delegation rules |
| TOOLS.md | New tool usage patterns, workarounds |

## Safety

- **Incremental**: Only appends, never overwrites existing content
- **Backups**: Creates timestamped backups in `.soulforge-backups/`
- **Dry Run**: Preview changes with `--dry-run`
- **Threshold**: Patterns must appear multiple times before promoting

## Schedule (Recommended)

Set up a cron job for continuous evolution:

```bash
# Every 2 hours
openclaw cron add --name soulforge-evolve --every 120m \
  --message "exec python3 ~/.openclaw/skills/soul-forge/scripts/soulforge.py run"
```

## Files Generated

- `.soulforge-backups/*.bak` — Timestamped backups
- `.soulforge-state.json` — Last run state (optional)

## Memory Sources

| Source | Path | Priority |
|--------|------|----------|
| Daily logs | `memory/YYYY-MM-DD.md` | High |
| Learnings | `.learnings/LEARNINGS.md` | High |
| Errors | `.learnings/ERRORS.md` | Medium |
| hawk-bridge | Vector store | Medium |

## Exit Codes

- `0` — Success
- `1` — Error (check output for details)
