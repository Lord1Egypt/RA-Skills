---
name: signal-dreaming
description: Signal-driven memory consolidation for OpenClaw agents. Automatically consolidates recent session logs into long-term memory using recall frequency signals from memory/.dreams/short-term-recall.json — content that has been searched more often gets prioritized. Runs in three safe phases (Sense/Consolidate/Settle) with a human-readable dream diary. Use when setting up automated memory maintenance, running a manual "dream" consolidation pass, or upgrading from date-ordered log processing to signal-aware prioritization.
---

# Memory Dreaming

Signal-aware memory consolidation in three phases. Instead of processing logs by date order, this skill reads `memory/.dreams/short-term-recall.json` (maintained automatically by OpenClaw's memory-core) to find what's been most frequently recalled — then prioritizes consolidating those entries into long-term topic files.

## Memory Architecture Assumed

This skill expects a two-layer memory layout:

- **Daily logs** (`memory/YYYY-MM-DD*.md`) — raw session notes, never deleted
- **L2 topic files** (`memory/<topic>.md`) — curated, durable knowledge on a specific subject (e.g. `memory/clash-verge.md`, `memory/business.md`). Created manually or by the dream agent when new topics emerge.
- **Index** (`MEMORY.md`) — high-level status overview with pointers to L2 files

If you are starting fresh, create at least `MEMORY.md` and `memory/dream-log.md` before the first dream run. L2 files are created on demand.

## Quick Start

### Manual dream (run once)

Tell your agent:
> "Run a memory dream consolidation. Follow the protocol in `<SKILL_PATH>/references/dream-protocol.md`. Workspace root: `<YOUR_WORKSPACE_PATH>`."

Or simply: *"爆爆做个梦"* / *"run a dream consolidation"* — if this skill is loaded, the agent will know what to do.

### Automated daily dream (cron)

Set up an isolated agentTurn cron that runs while your human is asleep:

```json
{
  "name": "daily-dream",
  "schedule": { "kind": "cron", "expr": "0 7 * * *", "tz": "<YOUR_TIMEZONE>" },
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "timeoutSeconds": 900,
    "message": "Run a memory dream consolidation. Find and read references/dream-protocol.md inside the signal-dreaming skill (check your skillDirs; common locations: skills/signal-dreaming/ or ~/.openclaw/skills/signal-dreaming/). Workspace root: <YOUR_WORKSPACE_PATH>. End your final response with a one-line dream summary — the cron delivery mechanism will auto-announce it."
  },
  "delivery": { "mode": "announce", "channel": "<CHANNEL_TYPE>", "to": "<CHANNEL_ID>" }
}
```

Adjust `expr` and `tz` to match when your human sleeps.

## How the Signal Works

OpenClaw's `memory-core` maintains `memory/.dreams/short-term-recall.json` automatically. Every `memory_search` call updates this file with:

- `recallCount` — how many times a snippet was returned in results
- `totalScore` — weighted composite (relevance × frequency × query diversity × recency)
- `queryHashes` — distinct queries that surfaced this snippet (diversity signal)
- `recallDays` — days the snippet was active

The dream protocol reads `totalScore` to rank candidates. Snippets with `totalScore > 0.8` from multiple distinct queries are strong promotion candidates.

## Three-Phase Safety Model

| Phase | Writes | Purpose |
|-------|--------|---------|
| **Sense** | ❌ None | Read recall signals + scan recent logs |
| **Consolidate** | ✅ L2 files only | Promote high-value content to topic files |
| **Settle** | ✅ MEMORY.md + dream-log.md | Trim index, write diary entry |

Phase 1 is always read-only. An error in Sense never corrupts files.

## Quality Gates

The full protocol includes a read-only planning checkpoint before writes:

- **Topic identity guard** — do not merge legacy/current projects just because names are similar; split active, legacy, and index files when durable IDs, hosts, owners, or lifecycle differ.
- **Lifecycle guard** — classify candidates as active / waiting / done / archived / closed / snowed; closed or snowed work must not reappear as active TODOs unless the human reopens it.
- **Secret propagation guard** — never promote API keys, tokens, passwords, private keys, signed URLs, or credential-bearing command lines from daily logs into L2, MEMORY.md, or dream-log.md.
- **Backup guard** — existing L2 files are copied outside `memory/` to `<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/` with a `.bak` suffix before modification; `MEMORY.md` is backed up there too before rewrite.
- **Post-write audit** — check size, Markdown structure, current-vs-legacy separation, and obvious credential patterns before finalizing. Use `references/dream-audit.sh` for the common lightweight sanity checks; it is not full DLP.


## Compatibility with OpenClaw 2026.4.15+

OpenClaw 2026.4.15 changed the built-in **memory-core Dreaming** default from `inline` to `separate` mode. This is a **different system** from this skill:

| | memory-core built-in Dreaming | signal-dreaming (this skill) |
|---|---|---|
| Trigger | Heartbeat (automated) | Cron agentTurn |
| Output | `DREAMS.md` / `memory/dreaming/{phase}/` | `memory/dream-log.md` + L2 files |
| Signal source | Internal | `memory/.dreams/short-term-recall.json` |

**These two systems are independent.** You can use this skill whether or not built-in Dreaming is enabled.

If you use **both**:
- Keep built-in Dreaming in `separate` mode (default in 2026.4.15+). This keeps `memory/YYYY-MM-DD*.md` clean so this skill sees only real session notes.
- If you're on an older version with `inline` mode, the protocol will skip `## Light Sleep` / `## REM Sleep` phase blocks when scanning daily logs.

## Key Rules

- **Never move or delete daily logs** (`memory/YYYY-MM-DD*.md`) — archiving breaks memory_search indexing
- **dream-log.md is Markdown** — append text directly, do not write JSON
- **Never copy secrets into curated memory** — omit/redact and alert instead
- **Keep lifecycle state sticky** — closed/archived/snowed lines stay non-active unless explicitly reopened
- **Back up MEMORY.md** to `<WORKSPACE_ROOT>/.backup/memory-dreams/YYYYMMDD-HHMM/MEMORY.md.bak` before rewriting it
- **Back up touched L2 files** outside `memory/`, with `.bak` suffix, before editing existing topic files
- **MEMORY.md target**: ≤ 8KB

## Full Protocol

See `references/dream-protocol.md` for the complete three-phase workflow, scoring thresholds, dream-log format, and safety mechanisms.
