# Self-Improving Compound

[中文说明 / Chinese README](README_zh.md)

A portable AgentSkill that turns agent memory from scattered markdown notes into a structured self-improvement system: real-time capture, observable Candidate → Learning → Promotion queues, SQLite-backed learning, cron audits with explicit context collection, daily factual memory, and lightweight workspace stewardship.

## What it does

- **Captures durable lessons** before the final reply after non-trivial work: user corrections, tool/API gotchas, non-obvious failures, workarounds, and missing capabilities.
- **Stores execution learnings in SQLite** under `learning/memory_tree/chunks.db`, with FTS5 search, deterministic entity indexing, dedupe, lifecycle status, exports, and human-readable snapshots.
- **Keeps facts separate from lessons**: factual continuity goes to `memory/YYYY-MM-DD.md`; reusable prevention rules go to `learning/`.
- **Audits itself with cron**: light checks, heavy audits, daily factual memory, and post-digest workspace stewardship. Conversation-aware cron jobs should use deterministic context collectors when available instead of relying on implicit chat visibility.
- **Makes memory observable** with `Candidate → Learning → Promotion → Done`: candidates, promotion backlog, cursor coverage, and dashboard health are visible under `learning/pipeline/`.
- **Promotes stable rules** into the right layer: `skills/`, `AGENTS.md`, `TOOLS.md`, `MEMORY.md`, or other root agent state files.

## 3+7 co-evolution model

This system keeps three durable state directories and seven root Markdown control-plane files aligned:

**3 state directories**

- `memory/` — factual daily continuity: what happened, what changed, decisions, links, follow-ups.
- `learning/` — SQLite-backed execution lessons: corrections, tool/API gotchas, workflow rules.
- `skills/` — hardened reusable procedures that future agents can load on demand.

**7 root Markdown files**

- `AGENTS.md` — workspace contract, routing, execution policy, safety boundaries.
- `HEARTBEAT.md` — lightweight check-in surface; often intentionally empty when cron owns timing.
- `IDENTITY.md` — compatibility pointer or short identity bridge.
- `MEMORY.md` — pinned long-term hot context.
- `SOUL.md` — agent identity/persona.
- `TOOLS.md` — concrete local environment/tool facts.
- `USER.md` — durable user profile and collaboration preferences.

The steward loop should make only small, safe consistency updates across these files. It should not rewrite persona, weaken safety rules, or turn daily facts into root-level bloat.

## Architecture

```text
Observable Memory Pipeline
  -> collect incremental visible context
  -> add candidates
  -> log confirmed SQLite learnings
  -> queue durable promotions
  -> refresh dashboard

Real-time capture gate
  -> search existing SQLite learnings
  -> log compact correction/error/learning/feature entries
  -> enqueue async memory jobs

Memory job worker
  -> process chunk extraction jobs
  -> update scores, entity index, tree buffers, and tree summaries
  -> run HOT/WARM/COLD lifecycle maintenance

Daily factual memory
  -> write memory/YYYY-MM-DD.md
  -> extract only reusable lessons into learning/

Workspace stewardship
  -> export learning memory
  -> inspect learning/, skills/, and the 7 root Markdown control-plane files
  -> make only small safe consistency updates
```

## Install: files are only step 1

`clawhub install` only installs the skill files. A useful setup requires activation.

```bash
clawhub install self-improving-compound
export OPENCLAW_WORKSPACE="/path/to/workspace"
# Optional: share one learning store across multiple workspace roots.
# export SELF_IMPROVING_LEARNING_ROOT="$HOME/.openclaw/shared-learning"
export SELF_IMPROVING_SKILL_DIR="$OPENCLAW_WORKSPACE/skills/self-improving-compound"
export SELF_IMPROVING_LEARNINGS_CLI="$SELF_IMPROVING_SKILL_DIR/scripts/learnings.py"
chmod +x "$SELF_IMPROVING_SKILL_DIR"/scripts/*.py "$SELF_IMPROVING_SKILL_DIR"/scripts/*.sh "$SELF_IMPROVING_SKILL_DIR"/hooks/*.sh 2>/dev/null || true
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" init
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" status
```

Full activation checklist:

1. Install files with ClawHub or copy the skill directory.
2. Set `OPENCLAW_WORKSPACE`, `SELF_IMPROVING_SKILL_DIR`, and optionally `SELF_IMPROVING_LEARNINGS_CLI`.
   Set `SELF_IMPROVING_LEARNING_ROOT` only when multiple workspaces should share the same lesson store.
3. Initialize `learning/` with `learnings.py init`.
4. Add the capture gate to `AGENTS.md` or equivalent agent instructions.
5. Install/update cron jobs from `scripts/setup-cron.json` and configure delivery.
6. Optionally wire `hooks/activator.sh` and `hooks/error-detector.sh`.
7. Optionally enable `scripts/memory-pipeline.py` for Candidate → Learning → Promotion visibility.
8. Optionally configure `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR` for reliable Light Check context and `SELF_IMPROVING_DAILY_COLLECTOR` for high-quality daily memory.
9. Run smoke tests: search/log/export/daily-memory helper + `cron list`.

See `SKILL.md` for the detailed installation and activation flow.

Requirements:

- Python 3.8+
- bash. The bundled `.sh` helpers intentionally use bash features; POSIX `sh`-only environments are unsupported unless you call the Python CLI directly.
- No network access required for the local CLI

## Quick start

```bash
# Initialize learning storage in a workspace
python3 scripts/learnings.py --root /path/to/workspace init

# Search before logging
python3 scripts/learnings.py --root /path/to/workspace search "telegram format" --limit 5

# Log a correction
python3 scripts/learnings.py --root /path/to/workspace log-correction \
  --summary "Telegram replies should avoid wide tables" \
  --correct "Use compact lists for mobile chat" \
  --pattern chat:telegram-format

# Log a reusable learning
python3 scripts/learnings.py --root /path/to/workspace log-learning \
  --summary "Cron jobs that need conversation context should collect it explicitly" \
  --details "Isolated cron sessions do not automatically inherit main chat context; prefer a deterministic transcript/context collector, with sessions_history only as a verified fallback." \
  --pattern cron:explicit-context

# Review and maintain lifecycle
python3 scripts/learnings.py --root /path/to/workspace status
python3 scripts/learnings.py --root /path/to/workspace maintain --apply
# Optional automation: promote high-recurrence lessons into workspace memory files.
python3 scripts/learnings.py --root /path/to/workspace maintain --apply --auto-promote

# Process async memory jobs once, or keep a local daemon running
python3 scripts/learnings.py --root /path/to/workspace process-jobs
python3 scripts/learnings.py --root /path/to/workspace process-jobs --daemon --max-jobs 0

# Export for review
bash scripts/learning-export.sh
```

## Optional cron pipeline

The skill ships with OpenClaw cron templates in `scripts/setup-cron.json` and an agent setup guide in `scripts/setup-cron-agent.md`.

Recommended jobs:

| Job | Default schedule | Purpose |
|---|---:|---|
| Self-Improving Light Check | every 2h, 08:00–22:00 | Catch obvious missed corrections and blockers. |
| Learning Audit Heavy | 09:00 and 22:00 | Audit failures, log missed lessons, maintain lifecycle. |
| Daily Memory Digest | 23:50 | Write `memory/YYYY-MM-DD.md`, then extract reusable lessons. |
| Daily Workspace Steward | 00:20 | Export learning memory and lightly inspect `learning/`, `skills/`, and the 7 root Markdown control-plane files. |

For reliable Light Check context, set an optional collector when your runtime can export recent visible conversation from its local session/transcript store:

```bash
export SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR="python3 /path/to/recent-context-collector.py --limit 60"
```

Collector rule: exit 0 only after writing a readable Markdown/JSON context file; exit non-zero when the target transcript is unavailable so cron can report `BLOCKED: collector_unavailable` instead of a false success.

For an observable queue and health dashboard, use the bundled pipeline helper:

```bash
export SELF_IMPROVING_MEMORY_PIPELINE="$SELF_IMPROVING_SKILL_DIR/scripts/memory-pipeline.py"
python3 "$SELF_IMPROVING_MEMORY_PIPELINE" --base "$OPENCLAW_WORKSPACE/learning/pipeline" dashboard
```

The helper writes `candidates.jsonl`, `promotion-queue.json`, `cursor.json`, `status.json`, and `dashboard.md` under `learning/pipeline/`; it also writes a convenience `learning/dashboard.md`.

Cron installation is not automatic. Ask your OpenClaw agent:

> Install the self-improving compound cron jobs using `scripts/setup-cron.json` as reference. Check existing cron jobs first and update instead of duplicating.

## Path Model

There are two roots:

1. **Skill root** — this package: `scripts/`, `hooks/`, `references/`, `evals/`.
2. **Workspace root** — your active agent/project state:
   - `learning/memory_tree/chunks.db`
   - `learning/index.md`
   - `memory/YYYY-MM-DD.md` if daily factual memory is enabled
   - root agent files such as `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, `SOUL.md`, `HEARTBEAT.md`, `IDENTITY.md`

The learning store can be split from the workspace root with `--learning-root` or `SELF_IMPROVING_LEARNING_ROOT`. In that mode, SQLite, `index.md`, `heartbeat-state.md`, and `promotion-queue.json` live in the shared learning root, while `promote` and `maintain --auto-promote` still write only under the active workspace root.

Never write durable learnings into the installed skill directory. Always pass `--root /path/to/workspace`; add `--learning-root /path/to/shared-learning` only when sharing lessons across projects.

## Architecture Boundary

This is a selective OpenHuman memory-tree port for agent lesson management, not a full content-management clone. Implemented pieces include SQLite storage, FTS search with fallback, deterministic entity extraction, scoring, entity hotness, async jobs, lifecycle maintenance, deterministic tree buffers, and a promotion queue. LLM topic routing and full OpenHuman-style content workflows are intentionally out of scope for this Python layer.

## Key commands

```bash
python3 scripts/learnings.py --root /path/to/workspace init
python3 scripts/learnings.py --root /path/to/workspace status --format json
python3 scripts/learnings.py --root /path/to/workspace search "keyword" --limit 10
python3 scripts/learnings.py --root /path/to/workspace search "pk:tooling:api-client-gen"
python3 scripts/learnings.py --root /path/to/workspace search "entity:path:/repo/openapi.yaml"
python3 scripts/learnings.py --root /path/to/workspace search "keyword" --touch
python3 scripts/learnings.py --root /path/to/workspace log-error --summary "..." --details "..." --pattern area:stable-key
python3 scripts/learnings.py --root /path/to/workspace log-feature --summary "..." --details "..." --pattern feature:stable-key
python3 scripts/learnings.py --root /path/to/workspace process-jobs --format json
python3 scripts/learnings.py --root /path/to/workspace maintain --apply
python3 scripts/learnings.py --root /path/to/workspace maintain --apply --auto-promote
python3 scripts/learnings.py --root /path/to/workspace promote LRN-YYYYMMDD-001 --to AGENTS.md
bash scripts/daily-memory.sh --root /path/to/workspace
bash scripts/extract-skill.sh my-new-skill /path/to/workspace
```

## Guardrails

- Search before logging to avoid duplicates.
- Keep entries compact, searchable, and prevention-oriented.
- Do not log secrets, tokens, raw private transcripts, or volatile state.
- Treat cron audit candidates as review prompts, not automatic truth.
- Daily Workspace Steward may make small safe markdown updates only; it must not rewrite persona, weaken safety/privacy rules, delete files, or change cron jobs.

## Included references

- `references/entry-formats.md` — schemas and manual templates
- `references/promotion-and-extraction.md` — promotion thresholds and extraction criteria
- `references/platform-setup.md` — setup guidance for multiple agent runtimes
- `references/heartbeat-guidance.md` — when to use heartbeat vs cron
- `references/daily-memory-digest.md` — daily factual memory quality bar
- `references/hermes-integration.md` — architecture concepts absorbed from Hermes-style agents

## Credits

Hybrid adaptation from actual-self-improvement, self-improving-compound, OpenHuman memory-tree, local self-improving-agent patterns, GenericAgent memory hygiene axioms, and Hermes-style agent architecture.

Author/maintainer: Rockway Chen · <rockwaychen@gmail.com> · <https://github.com/LingmaFuture>
