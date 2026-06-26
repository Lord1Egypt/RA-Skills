# Changelog

## 6.2.5 - 2026-05-19

- Added bundled `scripts/memory-pipeline.py` for an observable `Candidate → Learning → Promotion → Done` flow.
- Added candidate queue, promotion queue, cursor-based incremental transcript processing, machine-readable status, and Markdown dashboard support.
- Updated Light Check cron template to use candidate-first scanning and commit cursor only after successful processing.
- Updated SKILL.md and README docs with the memory pipeline setup, dashboard paths, and promotion backlog workflow.

## 6.2.4 - 2026-05-19

- Documented the deterministic Light Check context collector pattern: isolated cron must not rely on implicit main-chat visibility.
- Added `SELF_IMPROVING_LIGHT_CONTEXT_COLLECTOR` as the portable environment contract for exporting recent visible user/assistant conversation to Markdown/JSON.
- Updated `scripts/setup-cron.json` so Light Check runs the collector first, reports `BLOCKED: collector_unavailable` on collector failure, and uses `sessions_history` only as a verified fallback.
- Updated English/Chinese README and cron setup guide with the collector contract and false-success guardrail.

## 6.2.3 - 2026-05-18

- Release packaging hygiene update: preserve local research/reference artifacts in the canonical working directory while excluding them from Git and ClawHub packages via ignore files.
- Verified ClawHub publish file collection excludes `.reference/` and `.clawhubignore`.


## 6.4.0 - 2026-05-18

- Added `--learning-root` / `SELF_IMPROVING_LEARNING_ROOT` so multiple workspaces can share one SQLite lesson store while promotions still target the active workspace.
- Made job claiming cross-process safer with an atomic SQLite `BEGIN IMMEDIATE` claim path and row-count guard.
- Added `promotion-queue.json` plus `maintain --apply --auto-promote` to turn high-recurrence promotion candidates into an explicit, bounded automation queue.
- Tightened the legacy `log` command so `--type COR` now follows `log-correction` validation and requires `--correct`.
- Documented the selective OpenHuman boundary, bash requirement, shared-learning path model, and supported capabilities.
- Added regression coverage for shared learning roots, promotion queue auto-promotion, and cross-store job claiming.

## 6.3.0 - 2026-05-18

- Added a portable Phase 2 memory upgrade: standalone SQLite FTS5 chunk index with LIKE fallback for robust full-text search.
- Added deterministic lightweight entity extraction for Pattern-Keys, areas, entry IDs, namespaced tokens, email addresses, and durable paths.
- Added unique entity-index upserts and active job dedupe keys to suppress duplicate extraction/maintenance work.
- Updated `search` to combine retrieval relevance with memory score and support exact `pk:` / `entity:` lookups.
- Added regression coverage for FTS search, entity extraction, entity-index dedupe, and job dedupe.

## 6.2.2 - 2026-05-18

- Expanded `SKILL.md` with a full installation and activation flow: root/env setup, learning-store initialization, capture gate, cron pipeline, hooks, optional daily collector, smoke tests, and common failure fixes.
- Clarified that `clawhub install` only copies files and is not a complete self-improving-system installation.
- Added concise install checklists to English and Chinese READMEs.


## 6.2.1 - 2026-05-18

- Clarified the 3+7 co-evolution model: 3 state directories (`memory/`, `learning/`, `skills/`) plus 7 root Markdown control-plane files (`AGENTS.md`, `HEARTBEAT.md`, `IDENTITY.md`, `MEMORY.md`, `SOUL.md`, `TOOLS.md`, `USER.md`).
- Added README language links between `README.md` and `README_zh.md`.
- Tightened Workspace Steward wording to explicitly inspect the 7 root Markdown files.


## 6.2.0 - 2026-05-18

- Added portable Daily Memory Digest integration guidance: facts stay in `memory/YYYY-MM-DD.md`; reusable lessons are extracted into SQLite.
- Upgraded the cron template from a three-job audit pipeline to a four-job maintenance pipeline with `Daily Workspace Steward`.
- Generalized `scripts/daily-memory.sh` so public installs can use an optional collector instead of Rockway-local absolute paths.
- Refreshed README / README_zh and SKILL.md to document 7+3 co-evolution, daily memory, and workspace stewardship guardrails.
- Synced local helper scripts, hooks, evals, and references from the hardened OpenClaw installation.
- Cleaned generated/private research artifacts from the public package before publishing.

## 6.1.7 - 2026-05-17

- Added cron installation infrastructure (scripts/setup-cron.json, scripts/setup-cron-agent.md).
- SKILL.md now has dedicated Cron installation section with one-time setup instructions.
- README / README_zh updated with cron setup table and quick-start instructions.
- Closes the cron audit architecture gap where scripts existed but scheduling was undocumented.

## 6.1.6 - 2026-05-17

- Added author contact: rockwaychen@gmail.com / GitHub LingmaFuture.

## 6.1.5 - 2026-05-17

- Optimized description and SKILL.md to clearly position as an agent memory and learning system, not just a task skill.
- Improved intro: three-layer architecture summary (real-time capture → cron audit → promotion).
- README now includes system positioning section explaining the SQLite/cron/co-evolution pipeline.
- Category changed from workflow to memory-system.

## 6.1.4 - 2026-05-17

- Synced public staging copy from ClawHub 6.1.3 series.
- Includes full 6.1.x stack: SQLite memory-tree backend, activation hardening mechanisms, cron enforcement architecture, session-history aware audit, capture gate output routing, 7+3 co-evolution model.

## 6.1.3 - 2026-05-17

- Added capture gate output routing table: lessons flow to memory/learning/skills/AGENTS/TOOLS based on type.
- Formalized the 7+3 continuous-improvement model: the full system (memory + learning + skills + AGENTS + TOOLS + MEMORY + HEARTBEAT) co-evolves; fixing one layer while leaving another stale is half-done work.

## 6.1.2 - 2026-05-17

- Replaced heartbeat-based audit with cron-isolated enforcement architecture: Self-Improving Light Check (2h via sessions_history), Learning Audit Heavy (2x/day), and Daily Export.
- Documented architecture rationale: cron isolation keeps main session context clean; sessions_list + sessions_history gives cron full conversation visibility without running inside the main session.
- Clarified heartbeat role: lightweight check-ins only; audit execution belongs in isolated cron, not in HEARTBEAT.md.


## 6.1.1 - 2026-05-17

- Added activation hardening norms: final-before-reply capture gate, heartbeat learning audit, watchdog/doctor/cron failure `log-error` routing, and daily SQLite export.
- Added helper scripts: `learning-audit.py`, `log-system-failures.sh`, and `learning-export.sh`.


All notable changes to this project will be documented in this file.

## [6.1.0] - 2026-05-17

### Changed
- Made SQLite (`learning/memory_tree/chunks.db`) the source of truth for durable learnings.
- Preserved human entry IDs (`TYPE-YYYYMMDD-XXX`) while keeping content-addressed chunk IDs internally.
- Updated docs, evals, hooks, and extraction guidance to match SQLite-first behavior.

### Fixed
- Distinct same-day entries no longer dedupe incorrectly by `TYPE/date`.
- `promote` and `edit` now operate on SQLite-backed entries instead of only scanning markdown files.
- `maintain --apply --format json` now applies lifecycle updates before emitting JSON.
- Hooks now route through `scripts/learnings.py` when available.

## [6.0.0] - 2026-05-12

### Added
- **`.learnings/` directory renamed to `learnings/`** (no dot prefix) — all paths updated across scripts, hooks, docs, and evals.
- **`--area` parameter** for all `log-*` commands — supports `project:name` and `domain:name` routing for proper tier placement.
- **Auto-increment Recurrence-Count** — search command now touches matched HOT entries, updating `Last-Seen` and incrementing `Recurrence-Count`.
- **WARM→HOT reverse promotion** — `maintain` now detects entries with `Recurrence-Count >= 3` within 7 days and promotes them back to HOT tier.
- **`promote` command** (`promote ID --to FILE`) — moves entries to promotion targets (AGENTS.md, CLAUDE.md, etc.) with traceable pointers.
- **`edit` command** (`edit ID --status STATUS --last-seen DATE --recurrence N`) — updates entry metadata in-place.
- **`scripts/daily-memory.sh`** — comprehensive daily memory template generator with structured sections for sessions, decisions, errors, learnings, and self-improvement audits.
- **`references/hermes-integration.md`** — documents selectively absorbed Hermes Agent architecture concepts kept lean for this system.
- **`index.md` now includes Skill Registry** — Pattern-Key index doubles as lightweight skill discovery inspired by Hermes's Skills Hub.

### Changed
- **Dedup improved** — `_do_dedup_check()` now uses `difflib.SequenceMatcher` for semantic similarity detection (>70% threshold).
- **SKILL.md metadata** updated to reflect Hermes Agent architecture influence.
- **All paths** migrated from `.learnings/` to `learnings/` (87 references across 10 files).

### Fixed
- Recurrence-Count now auto-increments on search — no longer a static dead value.
- Promotion lifecycle is now closed-loop — WARM entries can return to HOT when frequently used.
- Missing `--area` routing fixed — WARM tier placement is now deterministic.

## [5.0.0] - 2026-05-09

### Added
- `SKILL.md` with OpenClaw/portable AgentSkill frontmatter.
- Hybrid architecture: actual-self-improvement execution core + self-improving-compound HOT/WARM/COLD memory tiers + legacy promotion/hook guidance.
- `--root PATH` global option for all CLI commands.
- `OPENCLAW_WORKSPACE` environment variable support as default root.
- New specific logging commands: `log-correction`, `log-learning`, `log-error`, `log-feature`.
- Best-effort secret redaction in logging text.
- `references/entry-formats.md`, `references/promotion-and-extraction.md`, `references/platform-setup.md`.
- Machine-readable JSON evals: `evals/trigger-validation.json` and `evals/output-evals.json`.
- `CHANGELOG.md`.

### Changed
- `scripts/learnings.py` no longer hard-codes `~/self-improving`. All data now lives under `<root>/learning/`.
- `hooks/activator.sh` and `hooks/error-detector.sh` are now workspace-root aware and use `OPENCLAW_WORKSPACE`.
- `index.md` now includes tier statistics and Pattern-Key index.

### Deprecated
- Backward-compatible `log CONTENT --type ...` command is preserved but specific `log-*` commands are preferred.

### Removed
- Hard-coded `BASE_DIR = Path.home() / "self-improving"` from `scripts/learnings.py`.
- Markdown eval checklists replaced with JSON evals.
