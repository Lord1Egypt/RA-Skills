# Subconscious — Bounded Self-Improving Agent

**Published at: https://clawhub.ai/skills/subconscious** ⭐

A persistent, self-evolving bias layer for AI agents. Survives session resets. Shapes behavior quietly with strict guardrails. Designed for OpenClaw agents.

**Version 1.6** — Production ready

## Bundled Integration

Includes a wired connection to the **self-improving-agent** skill (v3.0.10) by **[@pskoett](https://clawhub.ai/u/pskoett)** — a separate skill that produces learnings from experience. The subconscious consumes those learnings and evolves them into persistent behavioral biases.

```
self-improving-agent (by @pskoett)  →  .learnings/  →  subconscious  →  live/bias
(produces lessons from errors,              (consumes +
 corrections, and insights)                   evolves)
```

The self-improving-agent skill files are included in this package under `self-improving-agent/` for convenience. Full credit to [@pskoett](https://clawhub.ai/u/pskoett) for the original skill.

## What It Does

```
Learnings Bridge          Pending Queue           Live Store           Session Context
.self-improving/ ────────► tick ───────────────► rotate ───────────► bias inject
                           (reinforce,           (promote eligible,
                            dedupe)               archive stale)
```

- **Learnings bridge**: Feeds lessons from the self-improving agent into the subconscious every 5 minutes
- **Bounded promotion**: Items must earn their way to live (confidence≥0.75, reinforcement≥3)
- **Governed mutations**: Every change is typed, bounded, and logged
- **Immutable core**: Identity/values are untouchable without human override
- **Ephemeral bias**: Max 5 items per session turn, never bloats context

## Quick Start

```bash
# Install (auto-detects your OpenClaw workspace)
git clone <repo> ~/.openclaw/skills/subconscious
cd ~/.openclaw/skills/subconscious/scripts
chmod +x install.sh
./install.sh

# Check status
SUBCONSCIOUS_WORKSPACE=~/.openclaw/workspace-alfred python3 subconscious_metabolism.py status
python3 subconscious_cli.py verify
python3 subconscious_cli.py bias
```

## Architecture

| Layer | Purpose | Governance |
|-------|---------|------------|
| `core/` | Immutable identity | BLOCKED — manual only |
| `live/` | Active learnings | Bounded mutations only |
| `pending/` | Queue for new items | Reinforcement → promotion |

**Item kinds**: `VALUE`, `LESSON`, `PRIORITY`, `PATTERN`, `CONSTRAINT`

## Metabolism Cycles

| Cycle | Cadence | Purpose |
|-------|---------|---------|
| `tick` | Every 5 min | Scan learnings, reinforce pending |
| `rotate` | Hourly | Full maintenance, promote eligible items |
| `review` | Daily 6am | Health check, snapshot integrity |
| `benchmark` | Weekly Mon 9am | Compare to baseline, track improvement |

## Files

```
subconscious/
├── SKILL.md                          # OpenClaw skill definition
├── scripts/
│   ├── install.sh                    # One-time installer
│   ├── subconscious_metabolism.py   # Metabolism CLI (tick/rotate/review)
│   └── subconscious_cli.py          # Admin CLI (status/bias/intake/verify)
├── subconscious/                     # Core package
│   ├── schema.py                    # Item dataclasses
│   ├── store.py                     # JSON file ops
│   ├── retrieve.py                  # Relevance scoring, dedup
│   ├── influence.py                 # Bias formatting
│   ├── governance.py                # Mutation rules
│   ├── evolution.py                 # Promotion pipeline
│   ├── maintenance.py               # Housekeeping
│   ├── intake.py                    # Turn extraction
│   ├── flush.py                     # Snapshot continuity
│   └── learnings_bridge.py          # Self-improving agent bridge
└── references/
    ├── ARCHITECTURE.md              # Design reference
    ├── INSTALL.md                   # Detailed install guide
    └── WIRING.md                  # How to wire to self-improving-agent
```

## Requirements

- Python 3.8+
- OpenClaw workspace

**Includes the self-improving-agent skill** (v3.0.10 by @pskoett) — bundled as a separate but paired skill.

**How they work together:**
```
self-improving-agent (by @pskoett)  →  .learnings/  →  subconscious  →  live/bias
(produces lessons from errors,               (consumes +
 corrections, and insights)                   evolves)
```

- `self-improving-agent/` files are bundled in this package — no separate install needed
- Hooks from self-improving-agent (`sessions_history`, `sessions_send`, `sessions_spawn`) are **DISABLED by default** — they require explicit manual enable in your OpenClaw hooks directory
- Both skills remain independent — the learnings bridge is a one-way read-only connection from `.learnings/` into subconscious

## Design Principles

1. **Bounded** — Hard limits: 50 core / 100 live / 500 pending
2. **Governed** — Typed mutations, no unbounded changes
3. **Metabolism not daemon** — One-shot cron jobs, no persistent process
4. **Immutable core** — Values never change without human OK
5. **Session-isolated** — Bias ephemeral, can't bloat context

## Custom Workspace

```bash
# Override where the skill looks for workspace memory
export SUBCONSCIOUS_WORKSPACE=/path/to/workspace

# Or per-command:
SUBCONSCIOUS_WORKSPACE=/path/to/workspace python3 scripts/subconscious_metabolism.py status
```

Works with any OpenClaw workspace regardless of directory name.

## License

For use within the Alfred/OpenClaw agent system.
