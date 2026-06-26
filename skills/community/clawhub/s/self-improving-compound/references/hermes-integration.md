# Hermes Integration Notes

How the self-improving compound selectively incorporates Hermes Agent architecture
strengths while staying lean and SQLite-backed.

## Concepts Absorbed from Hermes Architecture

### 1. Skill Registry & Discovery

Hermes has a Skills Hub with unified search across official/builtin/community sources
and trust levels (builtin > trusted > community). We mirror this with:

- **Pattern-Key index** as lightweight skill pointers — each Pattern-Key is a
  discoverable, searchable SQLite entity that links related entries across lifecycle states
- **Trust levels**: `confirmed` > `pending` > `experimental`, tracked per-entry
  as status metadata
- **Auto-discovery** via `learnings.py maintain` scan, which surfaces
  high-recurrence patterns as promotion candidates
- **`extract-skill.sh`** parallels Hermes's skill authoring workflow — turning
  proven learnings into reusable `SKILL.md` documents

### 2. Context Engine Awareness

Hermes has pluggable context engines (compressor, etc.). We keep it explicit
with tiered lifecycle loading:

- **HOT tier** (`admitted`) — active context candidates, equivalent to Hermes's
  active context window
- **WARM tier** (`buffered`) — retained context-specific records
- **COLD tier** (`sealed`) — archived/promoted/resolved records for explicit query/export

The `activator.sh` hook mirrors Hermes's context priming by extracting top
Pattern-Keys at session start.

### 3. Achievement-Driven Self-Improvement

Hermes has `hermes-achievements` plugin for gamified progress tracking. We
adopt the concept without the gamification:

- **Recurrence-Count** tracks pattern maturity — equivalent to achievement
  progress tracking
- **Promotion thresholds** as "achievement gates": Recurrence-Count >= 3
  triggers promotion review
- **Pattern extraction** = skill creation — when a pattern proves itself
  across multiple tasks, it graduates to a reusable skill via
  `extract-skill.sh`

### 4. Provider Abstraction (Kept Lean)

Hermes has 8 pluggable memory providers. We keep a single SQLite backend
but add abstraction for portability:

- Single-file SQLite backend under `learning/memory_tree/chunks.db`
- JSON-format export option (`--format json`) for portability between systems
- `OPENCLAW_WORKSPACE` env var for backend location independence

## What We Intentionally Did NOT Absorb

### Multi-Provider Memory Backend

Hermes supports 8 memory providers (honcho, mem0, holographic, retaindb,
byterover, supermemory, openviking, hindsight). We keep a single SQLite
backend.

**Rationale**: SQLite gives reliable local indexing, scoring, and idempotent
ingest while still requiring zero external services. Markdown export preserves
human review and portability when needed.

### Multi-Platform Gateway

Hermes has 10+ platform gateways (Telegram, Discord, Slack, Google Meet,
etc.). We stay platform-agnostic.

**Rationale**: The Portable AgentSkill format (`SKILL.md` frontmatter) works
wherever the agent works — no gateway abstraction needed. The skill travels
with the agent.

### Provider-Agnostic Model Switching

Hermes has 109+ model providers with runtime switching. We don't need this.

**Rationale**: Memory management is model-agnostic. Learning capture is about
content and patterns, not about which model executes the task. The
HOT/WARM/COLD tiering works identically regardless of the underlying LLM.

## Strategic Alignment

| Hermes Concept | Our Implementation | Lean-ness |
|---|---|---|
| Skills Hub | Pattern-Key Index + `extract-skill.sh` | Lighter — SQLite-backed, no server |
| Memory Providers | Single SQLite backend with lifecycle tiers | Lighter — no external services |
| Achievement System | Recurrence-Count + Promotion thresholds | Lighter — automatic, no gamification UI |
| Context Engine | HOT/WARM/COLD tiered loading | Lighter — explicit, no compression plugin |
| Skill Authoring | `SKILL.md` frontmatter + `entry-formats.md` | Equivalent |
| Cron / Scheduling | `heartbeat-guidance.md` + hooks | Lighter — bash-only, no cron plugin |
| Plugin Discovery | Workspace directory scan | Lighter — no four-source resolution |
| Observability | `evals/` JSON quality gates | Lighter — no observability plugin |

## Key Design Philosophy

Hermes optimizes for **breadth** — many providers, many platforms, many
models. The self-improving compound optimizes for **depth** — fewer
mechanisms, but each one is fully integrated into the agent's workflow
(capture gate, tiered storage, promotion lifecycle, skill extraction).

We absorb Hermes's **structural ideas** (skill registry, context awareness,
achievement tracking) while rejecting its **infrastructure complexity**
(multi-provider backends, platform gateways, model switching). The result is
a system that learns like Hermes but deploys like a single directory of
Markdown files.
