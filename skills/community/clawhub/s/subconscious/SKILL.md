---
name: subconscious
description: A bounded, governed self-improvement layer for OpenClaw agents. Consumes learnings from the self-improving-agent skill (produces .learnings/), evolves them through a typed mutation system, and surfaces emerging behavioral patterns as session biases. Triggers on: subconscious system installation, health checks, metabolism management (tick/rotate/review/benchmark), or reviewing what biases are active. Do NOT invoke proactively — only when Edward specifically asks about it or when the system health check cron reports issues.
readme: README.md
metadata:
  version: "1.6"
  compatibility:
    openclaw: ">= 1.0.0"
  tags:
    - self-improvement
    - memory
    - bias-layer
    - autonomous
    - metabolism
  category: agent-framework
  license: MIT
  author: elyasdruid
  homepage: https://clawhub.ai/skills/subconscious
  repositories:
    - type: github
      url: https://github.com/elyasdruid/subconscious
---

# Subconscious v1.5 — Bounded Self-Improving Agent

## What It Is

A persistent, self-evolving bias layer that survives session resets. Alfred's "second brain" — quiet, bounded, and strictly governed. It does NOT make decisions. It shapes how Alfred *approaches* decisions.

**Core principle**: Every mutation is typed, bounded, and logged. Core identity is untouchable without manual override.

## Architecture

```
Learnings Bridge          Pending Queue           Live Store           Session Context
.learnings/ ─────────────► tick ──────────────► rotate ──────────────► bias inject
(Self-improving agent)    (reinforce,           (promote eligible,       (5 items max,
                         dedupe,               archive stale)           ephemeral)
                         skip duplicates)

Core Store ────────────────────────────────────────────────────────────────► Identity
(Immutable values,                                                  (never changes
 values/style, guiding principles)                                   without human OK)
```

**Three layers:**
- `core/` — Immutable identity (Alfred's nature, Edward's preferences). Manual-only.
- `live/` — Active learnings from experience. Governed promotion from pending.
- `pending/` — Queue for new items. Bounded reinforcement before promotion eligibility.

**Five bias types:**
| Kind | Category | Example |
|------|----------|---------|
| `VALUE` | Identity | "Alfred is sharp, calm, direct" |
| `LESSON` | Context | "XHS MCP needs QR re-login each cycle" |
| `PRIORITY` | Active | "Verify before claiming success" |
| `PATTERN` | Interpretation | "Proof discipline failure mode" |
| `CONSTRAINT` | Attention | "Don't suggest without trying first" |

## Lifecycle Commands

All commands run from `scripts/` directory inside the skill:

```bash
cd ~/.openclaw/skills/subconscious/scripts

# Check system health
python3 subconscious_metabolism.py status
python3 subconscious_cli.py verify

# See active biases in session context
python3 subconscious_cli.py bias

# Manual metabolism cycles
python3 subconscious_metabolism.py tick        # Light tick (5 min cadence)
python3 subconscious_metabolism.py rotate       # Full rotation (hourly)
python3 subconscious_metabolism.py review       # Daily health check
```

## Metabolism Cycles

### Tick (every 5 min)
```bash
python3 subconscious_metabolism.py tick
```
- Scans `.learnings/` via learnings bridge → queues new items to pending
- Passive reinforcement: increments reinforcement count on pending items
- Skips already-reinforced items (prevents type corruption)
- Runs bounded maintenance: freshness decay, metrics, no structural changes

### Rotate (hourly)
```bash
python3 subconscious_metabolism.py rotate --enable-promotion
```
- Full maintenance: flush, decay, snapshot rotation
- **Promotion gate** (only with `--enable-promotion`):
  - `confidence >= 0.75`
  - `reinforcement >= 3`
  - `freshness >= 0.3`
  - Not a duplicate of anything in core/live/pending
  - Passes governance check
- Governance enforces typed mutation bounds on all items

### Review (daily at 6am)
```bash
python3 subconscious_metabolism.py review
```
- System health check
- Snapshot integrity
- Pending queue depth check
- Recommendations log

## Learnings Bridge

The learnings bridge connects the self-improving-agent skill to the subconscious:

- Scans `.learnings/LEARNINGS.md`, `.learnings/ERRORS.md`, `.learnings/FEATURES.md`
- Tracks seen entries per file in `learnings_bridge_last_seen.json`
- New entries → queued to `pending.jsonl` with type `candidate_queued`
- Entries already reinforced in this session → skipped (idempotent)

**Bridge to self-improving agent**: The learnings bridge should be called from the metabolism tick so that new learnings flow into the subconscious every 5 minutes automatically.

## Checking System Health

```bash
python3 subconscious_metabolism.py status
```

Expected output:
```
Core: 3/50   Live: 1/100   Pending: 0/500   Snapshots: 10/10
Status: OK
```

If `Pending: 0/500` and `Live: N` — system is healthy, items promoting correctly.
If `Status: blocked` — resource limits hit, run `rotate` to compact.

## Adding Items Manually

```bash
# Queue a lesson manually
python3 subconscious_cli.py intake --kind LESSON --text "Remember to verify before claiming success" --confidence 0.8 --source "manual"

# Check what's in pending
python3 subconscious_cli.py pending
```

## Key Files

| File | Purpose |
|------|---------|
| `subconscious/schema.py` | Item dataclasses, validation, kind enum |
| `subconscious/store.py` | JSON file ops with atomic writes |
| `subconscious/retrieve.py` | Relevance scoring, `is_duplicate` |
| `subconscious/influence.py` | Convert items to bias blocks for prompts |
| `subconscious/governance.py` | Mutation types, protection classes, bounds |
| `subconscious/evolution.py` | Promotion pipeline, reinforcement logic |
| `subconscious/maintenance.py` | Decay, snapshot rotation, housekeeping |
| `subconscious/intake.py` | Conservative item extraction from turns |
| `subconscious/flush.py` | Snapshot building/loading for session continuity |
| `subconscious/learnings_bridge.py` | Bridge to self-improving-agent `.learnings/` |

## For Claude Code Sessions

When Claude Code needs to assess or improve the subconscious system, use the `claude-cx` wrapper:

```bash
claude-cx "Run: python3 ~/.openclaw/skills/subconscious/scripts/subconscious_metabolism.py status"
claude-cx "Run: python3 ~/.openclaw/skills/subconscious/scripts/subconscious_cli.py bias"
claude-cx "Read ~/.openclaw/skills/subconscious/subconscious/evolution.py lines 450-525"
```

## Cron Setup

After running `install.sh`, four cron jobs are active:
- `*/5 * * * *` — tick (light metabolism)
- `0 * * * *` — rotate (hourly, with promotion)
- `0 6 * * *` — review (daily health check)
- `0 9 * * 1` — **weekly benchmark** (Monday 9am, compares to baseline)

### Weekly Benchmark

Compares current state to the baseline snapshot captured at install time. Reports on:
- Learnings volume change (LEARNINGS.md, ERRORS.md entries)
- New biases promoted to live
- Pending queue depth
- Error recurrence as a proxy for learning effectiveness

```bash
# Run manually
python3 scripts/subconscious_benchmark.py

# View past benchmarks
ls memory/subconscious/benchmarks/
cat memory/subconscious/benchmarks/benchmark_YYYY-MM-DD.json
```

To capture a new baseline:
```bash
python3 scripts/subconscious_benchmark.py --capture-baseline
```

To override workspace location:
```bash
export SUBCONSCIOUS_WORKSPACE=/path/to/any/workspace
```
