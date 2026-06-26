---
name: self-improving-compound
description: "Agent memory and self-improvement system. Replaces naive file-based agent memory with a structured SQLite learning engine: capture corrections, errors, and reusable lessons during active work, audit recent conversation context via isolated cron jobs with deterministic collectors when available, and promote proven rules into skills and agent instructions. 3+7 co-evolution model — 3 state directories (`memory/`, `learning/`, `skills/`) plus 7 root Markdown control-plane files (`AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`) improve together. Adds daily factual memory and workspace stewardship loops. Python 3.8+ CLI with bash hooks. Use for: logging non-obvious failures, user corrections, tool/API gotchas, or missing capabilities before the final reply. Use for: setting up automated cron-based audit pipelines that catch what real-time capture misses. Do not use for trivial typos or routine noise."
compatibility: "Portable Agent Skills format. Core workflow is agent-agnostic. Bundled helpers require Python 3.8+; hook helpers require bash. No network access is required."
metadata:
  version: "6.2.5"
  original_slug: "self-improving-compound"
  category: "memory-system"
  author: "Hybrid adaptation from actual-self-improvement, self-improving-compound, OpenHuman memory-tree, and Hermes Agent architecture | Contact: rockwaychen@gmail.com | GitHub: LingmaFuture"
---

# Self-Improving Compound

An agent memory and learning system that replaces naive file-based memory with a structured pipeline: real-time capture, observable Candidate → Learning → Promotion queues, automated cron-based audit, and continuous promotion of lessons into skills and agent instructions.

The system runs as four layers:
- **Layer 0 — Observable memory pipeline**: ambiguous or high-value experience moves through `Candidate → Learning → Promotion → Done` using `scripts/memory-pipeline.py`, with `learning/pipeline/candidates.jsonl`, `promotion-queue.json`, `status.json`, and `dashboard.md` making backlog and coverage visible.
- **Layer 1 — Real-time capture**: AGENTS.md final-before-reply gate logs corrections, errors, and workarounds to SQLite as they happen.
- **Layer 2 — Cron audit**: Isolated background jobs scan recent conversation context. Prefer a deterministic local transcript/context collector; use `sessions_history` only when it is verified in the runtime. The jobs detect missed lessons and maintain lifecycle (HOT → WARM → COLD).
- **Layer 3 — Daily factual memory**: a nightly `memory/YYYY-MM-DD.md` digest records decisions, paths, risks, links, and follow-ups; only reusable lessons are extracted into SQLite.
- **Layer 4 — Promotion + stewardship**: proven rules flow from `learning/` SQLite → `skills/` SKILL.md → the 7 root Markdown control-plane files (`AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`). The full 3+7 system co-evolves.

**Author:** Rockway Chen · [rockwaychen@gmail.com](mailto:rockwaychen@gmail.com) · [GitHub: LingmaFuture](https://github.com/LingmaFuture)

## Installation and activation — `clawhub install` is only step 1

A raw ClawHub install only copies the skill files. It does **not** automatically wire the agent into a self-improving operating loop.

Use this maturity ladder:

| Level | What is configured | Result |
|---|---|---|
| 1/5 | `clawhub install self-improving-compound` | Files are present; almost no behavior changes yet. |
| 2/5 | `learning/` initialized and CLI verified | Manual logging/search works. |
| 3/5 | Capture gate added to agent instructions | The agent remembers to log lessons before final replies. |
| 4/5 | Cron jobs installed and delivery configured | Missed lessons, failures, daily memory, and steward checks run automatically. |
| 5/5 | Hooks/env/collector verified | Activation reminders, error capture, path resolution, and daily factual memory are reliable. |

### Phase 0 — Identify roots

You must distinguish two roots:

```bash
# Workspace root: where memory/, learning/, AGENTS.md, etc. live
export OPENCLAW_WORKSPACE="/path/to/workspace"

# Optional shared lesson store for multiple workspace roots
# export SELF_IMPROVING_LEARNING_ROOT="$HOME/.openclaw/shared-learning"

# Skill root: where this skill was installed
export SELF_IMPROVING_SKILL_DIR="$OPENCLAW_WORKSPACE/skills/self-improving-compound"
export SELF_IMPROVING_LEARNINGS_CLI="$SELF_IMPROVING_SKILL_DIR/scripts/learnings.py"
```

For OpenClaw's default workspace this is usually:

```bash
export OPENCLAW_WORKSPACE="$HOME/.openclaw/workspace"
export SELF_IMPROVING_SKILL_DIR="$OPENCLAW_WORKSPACE/skills/self-improving-compound"
export SELF_IMPROVING_LEARNINGS_CLI="$SELF_IMPROVING_SKILL_DIR/scripts/learnings.py"
```

Do not write durable learnings into the skill directory. By default `learning/` belongs under the workspace root; use `SELF_IMPROVING_LEARNING_ROOT` or `--learning-root` only when several workspaces should share one lesson store.

### Phase 1 — Install files

```bash
clawhub install self-improving-compound
cd "$SELF_IMPROVING_SKILL_DIR"
chmod +x scripts/*.py scripts/*.sh hooks/*.sh 2>/dev/null || true
```

If the skill is copied manually, set `SELF_IMPROVING_SKILL_DIR` to the copied directory.

The bundled shell helpers require bash. On POSIX `sh`-only hosts, use the Python CLI directly and skip the `.sh` helpers.

### Phase 2 — Initialize and verify the learning store

```bash
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" init
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" status
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" search "install smoke test" --limit 3
```

Expected result:

- `learning/memory_tree/chunks.db` exists.
- `status` exits successfully.
- `search` works even when there are no results.

### Phase 3 — Add the capture gate to agent instructions

Add a compact rule to the agent's durable instruction file, usually `AGENTS.md`:

```markdown
## Self-improvement capture gate

Before the final reply after any non-trivial task, check whether the work involved a user correction, non-obvious failure, tool/API quirk, workaround, format mismatch, missing capability, or reusable convention.

If yes:
1. Search existing learnings first:
   `python3 $SELF_IMPROVING_LEARNINGS_CLI --root $OPENCLAW_WORKSPACE search "<keywords>" --limit 5`
2. If no suitable entry exists, log the durable lesson with `log-correction`, `log-error`, `log-learning`, or `log-feature`.
3. Keep entries compact, prevention-oriented, and secret-free.
```

Without this phase the skill remains mostly passive; the agent will not consistently capture lessons in real time.

### Phase 4 — Install the cron pipeline

Cron installation is not automatic. The templates live in `scripts/setup-cron.json`; agent-facing instructions live in `scripts/setup-cron-agent.md`.

Recommended OpenClaw flow:

1. Ask the agent: "Install the self-improving compound cron jobs using `scripts/setup-cron.json`. Check existing jobs first and update instead of duplicating."
2. Configure delivery for your channel, e.g. Telegram or Feishu.
3. Verify with `cron list`.

The pipeline normally includes:

| Job | Purpose |
|---|---|
| Self-Improving Light Check | Frequent lightweight scan for missed corrections, errors, and blockers. |
| Learning Audit Heavy | System/cron failure audit, `learning-audit.py --log`, lifecycle maintenance. |
| Daily Memory Digest | Writes `memory/YYYY-MM-DD.md` factual continuity notes and extracts reusable lessons. |
| Daily Workspace Steward | Exports `learning/`, checks `skills/`, and inspects the 7 root Markdown control-plane files. |

Important cron requirements:

- Set `schedule.tz` to the user's actual timezone.
- Set or infer `delivery.channel` and `delivery.to`; otherwise reports may not reach the user.
- Use `cron update` for existing jobs; do not create duplicates.
- Isolated cron sessions do not inherit main chat context. Jobs that need conversation context should prefer an explicit collector that exports recent visible conversation to a file. Use `sessions_list` / `sessions_history` only after verifying those tools can access the target session from isolated cron.

### Phase 5 — Configure optional hooks

Hooks are optional but improve activation. They are runtime-specific.

Dry-run the bundled hooks first:

```bash
"$SELF_IMPROVING_SKILL_DIR/hooks/activator.sh" "install smoke test" || true
"$SELF_IMPROVING_SKILL_DIR/hooks/error-detector.sh" "install" "smoke test" || true
```

If your client supports command hooks, wire:

- `hooks/activator.sh` as a pre-prompt / prompt-start reminder.
- `hooks/error-detector.sh` as a post-error / failed-command reminder.

If your runtime has no hook system, skip this phase and rely on the capture gate plus cron. Do not invent config keys; use your runtime's documented hook mechanism.

### Phase 6 — Configure the observable memory pipeline

The bundled `scripts/memory-pipeline.py` adds an explicit queue and dashboard around cron/context scanning. It is optional for tiny installs but recommended for reliable systems.

```bash
export SELF_IMPROVING_MEMORY_PIPELINE="$SELF_IMPROVING_SKILL_DIR/scripts/memory-pipeline.py"
# Optional if the OpenClaw session key is ambiguous:
# export SELF_IMPROVING_MAIN_SESSION_KEY="agent:main:<channel>:direct:<id>"
python3 "$SELF_IMPROVING_MEMORY_PIPELINE" --base "$OPENCLAW_WORKSPACE/learning/pipeline" dashboard
```

State files:

- `learning/pipeline/candidates.jsonl` — suspected lessons awaiting dedupe/logging.
- `learning/pipeline/promotion-queue.json` — logged lessons awaiting skill/root-file promotion.
- `learning/pipeline/cursor.json` — last processed transcript line for incremental cron scans.
- `learning/pipeline/dashboard.md` and `learning/dashboard.md` — human-readable health view.

Cron Light Check should prefer this flow: `collect-incremental → add/mark candidates → log learnings → add/mark promotions → dashboard → commit-cursor`. Commit the cursor only after successful processing.

### Phase 7 — Configure optional context collectors

For reliable cron audits, prefer deterministic collectors over implicit chat context. A collector is a local command that reads the runtime's session/transcript store and writes recent visible user/assistant text to a Markdown or JSON file. It should skip tool outputs, hidden thinking, secrets, and raw long transcripts.

Light Check can use a local recent-conversation collector:

```bash
export SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR="python3 /path/to/recent-context-collector.py --limit 60"
```

Collector contract:

- Exit `0` only when context was exported successfully.
- Print either the output context path or a compact JSON summary containing the path/status.
- Write a readable Markdown/JSON context file with recent user/assistant visible text.
- Exit non-zero if the transcript/session cannot be found; the cron job should report `BLOCKED: collector_unavailable` instead of claiming success.

`Daily Memory Digest` can also use a local collector if your runtime has one:

```bash
export SELF_IMPROVING_DAILY_COLLECTOR="python3 /path/to/collector.py"
bash "$SELF_IMPROVING_SKILL_DIR/scripts/daily-memory.sh" --root "$OPENCLAW_WORKSPACE"
```

If no collector is configured, the helper prints the target note contract and the agent must gather context with available runtime tools.

### Phase 8 — End-to-end smoke test

Run this checklist after installation:

```bash
python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" log-learning \
  --summary "Self-improving install smoke test" \
  --details "Temporary entry to verify logging path; mark resolved or delete if desired." \
  --pattern "install:smoke-test" \
  --area "domain:setup"

python3 "$SELF_IMPROVING_LEARNINGS_CLI" --root "$OPENCLAW_WORKSPACE" search "install smoke test" --limit 5
bash "$SELF_IMPROVING_SKILL_DIR/scripts/learning-export.sh"
bash "$SELF_IMPROVING_SKILL_DIR/scripts/daily-memory.sh" --root "$OPENCLAW_WORKSPACE" --date "$(TZ=Asia/Shanghai date +%F)"
```

Then verify:

- `learning/memory-export.md` exists.
- `learning/status.json` exists.
- `memory/YYYY-MM-DD.md` target is clear if daily memory is enabled.
- `cron list` shows the expected enabled jobs with `nextRunAtMs`.
- Delivery target is configured for cron job summaries.

### Common install failures

| Symptom | Likely cause | Fix |
|---|---|---|
| `clawhub install` succeeded but nothing changes | Capture gate and cron not configured | Complete phases 3-4. |
| Cron runs but finds no conversation context | Isolated session has no main history or `sessions_history` is restricted | Configure `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR`; use `sessions_history` only as a verified fallback. |
| Learnings appear under the skill directory | Wrong `--root` | Set `OPENCLAW_WORKSPACE`; always pass `--root`. |
| Cron summaries disappear | `delivery` missing channel/recipient | Set `delivery.channel` + `delivery.to`. |
| Daily memory is generic or empty | No collector/context source | Configure `SELF_IMPROVING_DAILY_COLLECTOR` or improve the cron prompt. |
| Duplicate cron jobs | Setup re-run without idempotency check | `cron list` first; update by job name. |

## 3+7 co-evolution model

The **3** state directories are:

- `memory/` — factual daily continuity.
- `learning/` — SQLite-backed execution lessons.
- `skills/` — hardened reusable procedures.

The **7** root Markdown control-plane files are:

- `AGENTS.md` — workspace contract, routing, execution policy, safety boundaries.
- `HEARTBEAT.md` — lightweight check-in surface; often intentionally empty when cron owns timing.
- `IDENTITY.md` — compatibility pointer or short identity bridge.
- `MEMORY.md` — pinned long-term hot context.
- `SOUL.md` — agent identity/persona.
- `TOOLS.md` — concrete local environment/tool facts.
- `USER.md` — durable user profile and collaboration preferences.

The steward loop should keep these layers aligned with small, safe edits only. It must not rewrite persona, weaken safety/privacy rules, or promote volatile daily facts into root-level bloat.

## Core idea

Use this system for **durable improvement**, not for every bump in the road.

### Mandatory capture gate

Before a final reply, run this quick check:

- Did the task include a non-obvious failure, API/tool quirk, or format mismatch?
- Did a workaround or environment-specific convention make the task succeed?
- Did the user correct a fact, preference, workflow, or expectation?
- Would repeating this lesson save time or prevent damage later?

If yes, **search existing learnings first, then log the lesson before replying**. Do not rely on a “mental note.”

A good entry usually has at least one of these properties:
- It corrected a wrong assumption.
- It revealed a project-specific convention.
- It required real debugging or investigation.
- It is likely to recur.
- It should change future workflow, memory, or tooling.

Do **not** log routine noise such as obvious typos, expected validation failures, or errors that were solved immediately with no transferable lesson.

### Capture gate output routing

Not all lessons go to the same place. Route based on type:

| Lesson type | Destination | Example |
|---|---|---|
| User facts, preferences, system state | `MEMORY.md` / `memory/YYYY-MM-DD.md` | "Rockway prefers newspaper theme" |
| Execution mistakes, tool gotchas, workarounds | `learning/` SQLite | "Python shadowing broke promote" |
| Stable rules, workflows, anti-patterns discovered | owning `skills/<skill>/SKILL.md` | "cron isolation means no session context" |
| Behavioral constraints | `AGENTS.md` | "Don't commit workspace root" |
| Environment-specific tool knowledge | `TOOLS.md` | "Tailscale node name" |

The full 3+7 system co-evolves: fixing one layer while leaving another stale is half-done work. When a lesson reveals a skill is stale, upgrade it immediately and bump its version.

## Hybrid architecture

This skill merges three design lineages into one portable package:

| Lineage | Role | What We Kept |
|---|---|---|
| **actual-self-improvement** | Execution core | Python CLI (`scripts/learnings.py`), structured logging, JSON evals, search-before-log dedupe |
| **OpenHuman memory-tree** | Storage core | SQLite chunks, FTS search, entity index, scores, hotness, async jobs, deterministic tree buffers, lifecycle status, idempotent ingest |
| **self-improving-compound** | Memory architecture | HOT/WARM/COLD lifecycle, workspace-scoped `learning/`, lightweight bootstrap markdown |
| **self-improving-agent-local** | Promotion & hooks | Quantified promotion thresholds, OpenClaw hook guidance, pattern-key recurrence rules |

### Directory layout under `learning/`

```
learning/
├── memory_tree/chunks.db  # SQLite source of truth for durable learnings
├── index.md               # SQLite-generated snapshot (entries, lifecycle, pattern keys)
├── promotion-queue.json   # bounded maintain queue for proven promotion candidates
├── projects/              # WARM tier (project-specific)
├── domains/               # WARM tier (domain-specific)
└── archive/               # COLD tier (inactive)
```

## Important path model

There are **two different roots** in this skill:

1. **Skill root** — where bundled resources live:
   - `scripts/...`
   - `references/...`
   - `hooks/...`

2. **Workspace root** — where the project or active workspace lives:
   - `learning/memory_tree/chunks.db`
   - `learning/index.md` (SQLite-generated snapshot)
   - `memory/YYYY-MM-DD.md` factual daily notes, when enabled
   - `learning/projects/`
   - `learning/domains/`
   - `learning/archive/`
   - root agent files such as `AGENTS.md`, `MEMORY.md`, `TOOLS.md`, `USER.md`, `SOUL.md`, `HEARTBEAT.md`, `IDENTITY.md`

When `SELF_IMPROVING_LEARNING_ROOT` or `--learning-root` is set, the `learning/*` files above live in that shared learning root instead. Promotions still target the active **workspace root**, so a shared store can feed multiple projects without writing AGENTS/TOOLS files into the wrong workspace.

Never write learnings into the installed skill directory. Always target the **workspace root** for project memory and the optional **learning root** for shared lesson storage.


## Activation hardening mechanisms

When this skill is installed in a persistent agent runtime, self-improvement must be enforced by the system rather than left to memory. The recommended architecture uses three enforcement loops:

- **Capture gate**: an agent instruction requiring `search + log` before every final reply after a non-trivial task. This catches lessons in real-time during active work.
- **Cron enforcement**: isolated background jobs that audit recent session history, scan for system failures, maintain lifecycle, and export SQLite for review. Cron runs in *isolated sessions* that do not consume the main conversation context.
- **Daily stewardship**: a factual daily digest plus a post-digest workspace steward keep `memory/`, `learning/`, `skills/`, and the 7 root Markdown control-plane files aligned without broad rewrites.

### Architecture decisions (why cron, not heartbeat)

- **Cron is isolated.** `sessionTarget: "isolated"` creates a fresh ephemeral session that does not pollute the main agent's context window or bust prompt-cache warmth.
- **Cron context must be explicit.** An isolated cron job does not automatically see the main chat. Prefer a deterministic collector that reads the runtime's local session/transcript store and exports recent user/assistant visible text to a file. `sessions_list` / `sessions_history` can be used only when you have verified they work from isolated cron; otherwise they create false confidence.
- **Heartbeat runs in the main session by default.** Its role should be limited to lightweight check-ins and urgent reminders. Do not embed audit execution commands in `HEARTBEAT.md`; keep that file minimal so heartbeat returns `HEARTBEAT_OK` quickly unless an urgent decision is needed.

### Recommended cron schedule

```text
Cron                                     Schedule (Asia/Shanghai)
──────────────────────────────────────   ──────────────────────
Self-Improving Light Check               0 8-22/2 * * *    (every 2h during waking hours)
Learning Audit (Heavy)                   0 9,22 * * *      (2x/day)
Daily Memory Digest                      50 23 * * *       (nightly factual memory)
Daily Workspace Steward                  20 0 * * *        (post-digest maintenance)
```

#### Light Check (every 2h, 08:00-22:00)

A quick in-between scan that reads recent conversation context and checks whether any user correction, non-obvious error, workaround, or tool/API quirk has been missed by the SQLite learning store. Preferred path: run `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR`, read its exported Markdown/JSON, then dedupe with `learnings.py search`. Fallback path: use `sessions_list` / `sessions_history` only if verified from isolated cron. Tools: `exec`, `read`; optionally `sessions_list`, `sessions_history` for the fallback. Timeout: 120-180s.

#### Heavy Audit (09:00, 22:00)

Full audit: system-failure check, cron-failure scan, `learning-audit.py --log`, and `learnings.py maintain --apply` for lifecycle promotion/demotion. Tools: `exec`, `read`, `cron`. Timeout: 240s.

#### Daily Memory Digest (23:50)

Run `scripts/daily-memory.sh`, gather or read the daily context, write `memory/YYYY-MM-DD.md`, then run the capture gate on the final note. Facts stay in `memory/`; compact reusable lessons go to SQLite. See `references/daily-memory-digest.md`. Timeout: 300s.

#### Daily Workspace Steward (00:20)

Run `scripts/learning-export.sh`, inspect `learning/`, `skills/*/SKILL.md`, and root agent markdown files for small safe consistency updates. It may fix verified stale facts or clear contradictions, but must not rewrite persona, weaken safety/privacy rules, delete files, or change cron jobs. Timeout: 300s.

### Cron installation (one-time setup)

**The cron jobs described above are NOT created automatically when you install this skill.** You must run the setup once to create them in your OpenClaw instance.

The production-grade cron job definitions are in `scripts/setup-cron.json`. The agent-facing setup guide is `scripts/setup-cron-agent.md`.

Quick setup (run from your OpenClaw main session):

1. **Confirm**: "I want to install the self-improving compound cron jobs. Use `scripts/setup-cron.json` as reference."

2. Your agent will:
   - Read the JSON definitions
   - Resolve placeholder paths (skill root, workspace root)
   - Ask or infer your delivery channel (Telegram / Feishu / etc.)
   - Call `cron add` / `cron update` for each job, avoiding duplicates

3. **Verify**: `cron list` should show enabled jobs with `nextRunAtMs` set.

If you already have these jobs running, this step is a no-op.

### AGENTS.md capture gate

Add the following rule to agent instructions (e.g. AGENTS.md):

> Before every final reply after a non-trivial task: if the task involved a user correction, non-obvious failure, API/tool quirk, workaround, format mismatch, missing capability, or reusable convention, search existing SQLite learning first with `scripts/learnings.py --root <workspace> search "<keywords>" --limit 5`. If no suitable entry exists, log the durable lesson before replying. Never rely on a mental note; `learning/memory_tree/chunks.db` is the execution-learning source of truth.

### System failure routing

Route watchdog, doctor, healthcheck, and cron failure signals into `log-error` with stable pattern keys and dedupe:

- Pattern keys: `cron:<job-name>`, `doctor:<check-name>`, `watchdog:<component>`, `system:openclaw-audit-failure`
- Use `scripts/log-system-failures.sh` as an OpenClaw CLI audit wrapper where available.
- Always search existing entries first to prevent repeated failures from flooding SQLite.

### Guardrails

- Keep entries compact and prevention-oriented.
- Never log secrets; the CLI redacts tokens, passwords, and API keys automatically.
- Do not paste full audit exports into chat unless explicitly asked.
- Treat audit candidates as review prompts rather than automatic truth.
- Cron runs should reply with one-line summaries or `HEARTBEAT_OK`; do not echo full command output.

## Quick decision table

| Situation | What to do |
|---|---|
| User corrects you or updates a fact | Log a **correction** |
| Non-obvious command / API / tool failure | Log an **error** |
| User asks for a missing capability | Log a **feature request** |
| You discover a reusable workaround or convention | Log a **learning** |
| A pattern keeps recurring | Search related entries, link with `See Also`, and consider promotion |
| A lesson is broadly applicable or repeated | Promote it into project memory |
| A resolved, general pattern could help other projects | Extract a new skill |

## Standard workflow

### 0) Optional nightly factual memory

If the workspace uses daily factual notes, run or schedule:

```bash
bash scripts/daily-memory.sh --root /absolute/path/to/workspace
```

Then write `memory/YYYY-MM-DD.md` from the gathered context and run the capture gate on that note. Use `references/daily-memory-digest.md` for the quality bar. Do not copy the diary into SQLite; extract only reusable prevention rules.

### 1) Find the workspace root first

Before reading or writing `learning/`, determine `WORKSPACE_ROOT`.

Good defaults:
- the repository root for the current codebase
- the OpenClaw workspace root (`OPENCLAW_WORKSPACE` env var)
- the directory containing the files being edited

If unsure, prefer the directory containing `.git`, `AGENTS.md`, `CLAUDE.md`, or the user's active project files.

### 2) Initialise `learning/` if needed

Use the helper instead of creating files manually:

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace init
```

This creates:
- `learning/memory_tree/chunks.db` (SQLite database)
- `learning/projects/`
- `learning/domains/`
- `learning/archive/`

The `learning/index.md` snapshot is generated on first write (log, promote, etc.).

### 3) Review existing learnings before risky or familiar work

Review first when:
- you are returning to an area with prior failures
- the task touches infra, CI, deployment, auth, data migration, or generated code
- the user explicitly says "remember this", "we hit this before", or similar

Use the helper:

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace status
python3 scripts/learnings.py --root /absolute/path/to/workspace search "pnpm" --limit 5
python3 scripts/learnings.py --root /absolute/path/to/workspace search "pnpm" --touch

# --root can also be placed after the subcommand
python3 scripts/learnings.py status --root /absolute/path/to/workspace --format json
```

Plain `search` is read-only. Use `--touch` only when the result was actually reused and should increment recurrence metadata.

### 4) Search before logging to avoid duplicates

Always search for related entries before creating a new one.

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace search "keyword or pattern" --limit 10
```

If a similar entry already exists:
- prefer linking with `See Also`
- reuse or add a stable `Pattern-Key` for recurring issues
- bump priority only when recurrence justifies it
- prefer updating the existing pattern story over spraying near-duplicate entries

### 5) Log the right kind of entry

#### Correction
Use for user corrections and updated facts. Stored in SQLite with a human ID such as `COR-YYYYMMDD-001`.

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace log-correction \
  --summary "Used wrong format for Telegram" \
  --correct "Use lists, not tables" \
  --pattern chat:telegram-format
```

#### Learning
Use for corrections, knowledge gaps, best practices, and durable conventions. Stored in SQLite with a human ID such as `LRN-YYYYMMDD-001`.

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace log-learning \
  --summary "Project uses pnpm workspaces, not npm" \
  --details "Attempted npm install. Lockfile and workspace config showed pnpm." \
  --pattern pkg:pnpm-workspace
```

#### Error
Use for non-obvious failures, exceptions, or tool/API issues worth remembering. Stored in SQLite with a human ID such as `ERR-YYYYMMDD-001`.

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace log-error \
  --summary "Docker build failed on Apple Silicon due to platform mismatch" \
  --details "docker build -t myapp . on Apple Silicon" \
  --pattern docker:platform
```

#### Feature request
Use when the user wants a missing capability or a recurring friction point should become a feature. Stored in SQLite with a human ID such as `FTR-YYYYMMDD-001`.

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace log-feature \
  --summary "User needs report export to CSV" \
  --details "Needed for sharing weekly reports with non-technical stakeholders" \
  --pattern reports:csv-export
```

#### Backward-compatible log
The old `log` subcommand is preserved for compatibility:

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace log "Used wrong format" \
  --type COR --pattern chat:telegram-format --correct "Use lists" --force
```

To inspect or share entries, export from SQLite:

```bash
python3 scripts/learnings.py --root /absolute/path/to/workspace export
python3 scripts/learnings.py --root /absolute/path/to/workspace export --format json
```

### 6) Promote proven lessons into memory

Promote when the learning is broad, repeated, or something any future contributor should know.

Common targets:
- `CLAUDE.md` — durable project facts and conventions
- `AGENTS.md` — workflow rules and automation guidance
- `.github/copilot-instructions.md` — shared Copilot context
- `SOUL.md` — behavioural principles in OpenClaw workspaces
- `TOOLS.md` — tool-specific gotchas in OpenClaw workspaces

Write promotions as **short prevention rules**, not long incident write-ups.

Example:
- Bad promotion: "On 2026-03-12 npm failed because…"
- Good promotion: "Use `pnpm install` in this repo; it is a pnpm workspace."

When a learning is promoted, update the original entry's status to `promoted` or `promoted_to_skill` and record the destination.

`maintain` writes high-recurrence candidates to `learning/promotion-queue.json`. For fully automated deployments, `maintain --apply --auto-promote` promotes those candidates into the active workspace root while keeping the shared learning store separate when `--learning-root` is used.

### 7) Extract a reusable skill when the pattern is real

Extract a new skill when the solution is:
- resolved and working
- broadly useful beyond one file or repo
- non-obvious enough that future agents would benefit
- recurring enough to justify its own instructions

Use the helper:

```bash
bash scripts/extract-skill.sh my-skill-name /absolute/path/to/workspace
```

## Logging rules that matter most

1. **Search first.** Duplicate entries are worse than missing tags.
2. **Prefer durable lessons.** Only log what should change future behaviour.
3. **Be specific.** Name the assumption, failure, or convention clearly.
4. **Include the fix or prevention rule.** An entry without next action is weak.
5. **Use stable pattern keys for recurring problems.** This lets recurrence compound.
6. **Promote aggressively once a rule is proven.** The point is fewer repeat mistakes.
7. **Do not interrupt the user with bookkeeping.** Log silently unless the user asked to see it or you need missing details.
8. **Never log secrets.** Tokens, passwords, API keys, and private data must be redacted or omitted.

## Memory lifecycle (integrated from ivangdavila/self-improving)

Entries carry metadata (`First-Seen`, `Last-Seen`, `Recurrence-Count`, `Status`, `Area`) so the system can make deterministic lifecycle decisions without guessing.

| Tier | Location | Size guidance | Behavior |
|------|----------|---------------|----------|
| HOT | SQLite lifecycle `admitted` | Active working set | Shown by `status`, `search`, and hooks |
| WARM | SQLite lifecycle `buffered` | 30+ days unused | Retained for context-specific search |
| COLD | SQLite lifecycle `sealed` | archived/promoted/resolved | Retained for explicit query/export |

### Automatic promotion/demotion

Use `python3 scripts/learnings.py --root <workspace> maintain` to review:

| Condition | Threshold | Action |
|---|---|---|
| HOT -> WARM | 30 days unused | Set lifecycle to `buffered` |
| WARM -> COLD | 90 days unused | Set lifecycle to `sealed` |
| Frequent reuse | `Recurrence-Count >= 3` from explicit reuse (`search --touch` or `edit`) | Flag for project-memory promotion |
| Compaction/export | Human review needed | Export and manually summarize/promote without deleting the SQLite record |

`maintain` defaults to `--dry-run`. Use `--apply` to execute lifecycle status moves. It never deletes content and does not auto-summarize.

### Conflict resolution

When patterns contradict:
1. **More specific wins**: `project` > `domain` > `global`
2. **More recent wins** at the same specificity level
3. **Ambiguous conflicts** → ask the user instead of guessing

## Promotion thresholds (from legacy)

| Condition | Threshold | Action |
|---|---|---|
| HOT -> WARM | 30 days unused | Mark `buffered` |
| WARM -> COLD | 90 days unused | Mark `sealed` |
| Frequent reuse | 3 recorded uses within 7 days | Promote as a short prevention rule |
| To AGENTS/SOUL/TOOLS | `Recurrence-Count >= 3` + spans 2+ tasks + within 30 days | Promote as short prevention rule |
| To skill | Proven + broadly applicable | Extract as skill |

## Recommended references

Use these only when needed:
- `references/entry-formats.md` — full field schemas and manual templates
- `references/promotion-and-extraction.md` — promotion rules and skill extraction criteria
- `references/platform-setup.md` — Claude Code, Codex, Copilot, and OpenClaw setup notes

## Hooks

Hook helpers are intentionally optional and workspace-root aware.

Available hook scripts:
- `hooks/activator.sh` — lightweight reminder at prompt start
- `hooks/error-detector.sh` — lightweight error reminder after failed Bash-like commands

Hook configuration examples live in `references/platform-setup.md`.

## What "next-level" looks like for this skill

A mature use of this skill has a loop:

**capture → dedupe → promote → extract → evaluate**

That means:
- entries are created with stable human IDs, content-addressed chunk IDs, and consistent fields
- repeated issues link to each other instead of fragmenting
- proven rules move into persistent memory files
- broadly useful fixes become standalone skills
- the skill itself is tested with trigger and output evals in `evals/`
