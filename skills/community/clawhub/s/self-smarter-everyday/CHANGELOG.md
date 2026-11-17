# Changelog

All notable changes to the **self-smarter-everyday** skill are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.0.0] — 2026-08-10

### Initial Release

First stable release of the self-smarter-everyday skill — a comprehensive autonomous self-improvement system for AI agents. This release provides the full infrastructure for nightly reflection, self-auditing, memory lifecycle management, prompt evolution, skill gap analysis, and improvement planning.

### Added

#### Core Scripts (`scripts/`)

- **`nightly_routine.py`** — Main orchestrator that runs 6 improvement phases in sequence:
  1. **Reflection** — Generates daily reflection journal entries with task performance tracking, goal alignment assessment, and knowledge gap identification.
  2. **Audit** — Invokes `self_audit.py` to collect quality metrics, error patterns, and token efficiency data.
  3. **Memory Compaction** — Invokes `memory_compact.py` to manage the HOT/WARM/COLD/ARCHIVE memory tier lifecycle.
  4. **Prompt Evolution** — Invokes `prompt_evolve.py` to mutate, evaluate, and select prompt variants.
  5. **Skill Gap Analysis** — Analyzes audit data to identify areas where performance falls below targets.
  6. **Improvement Planning** — Generates prioritized improvement plans based on identified gaps.
  - Supports `--dry-run` mode for testing without writing state.
  - Supports `--phase` flag to run individual phases in isolation.
  - File-based state persistence with JSON serialization.
  - Comprehensive logging to both file and stdout.
  - Error handling with graceful degradation (one phase failure doesn't abort others).

- **`self_audit.py`** — Self-audit metrics collector:
  - Memory metrics: directory sizes, file counts, per-directory breakdown.
  - Error metrics: error rate, error categories (timeout, missing resource, general), trend tracking.
  - Performance metrics: run count, success rate, phase execution tracking.
  - Token efficiency: reflection entry analysis, lesson capture rate.
  - Health score calculation (0-100) based on weighted combination of all metrics.
  - Outputs JSON report and human-readable summary.

- **`memory_compact.py`** — Memory tier lifecycle manager:
  - Four-tier system: HOT → WARM → COLD → ARCHIVE.
  - Promotion rules: entries accessed within 1 day are promoted to HOT.
  - Demotion rules: HOT→WARM after 3 days, WARM→COLD after 7 days, COLD→ARCHIVE after 30 days.
  - Similarity-based merging: entries with >80% word overlap in the same tier are merged.
  - Preserves most recent access timestamp when merging.
  - Dry-run mode for previewing transitions without executing.
  - Per-tier processing with `--tier` flag.

- **`prompt_evolve.py`** — Prompt evolution engine:
  - Five mutation strategies: clone, rephrase, constrain, relax, combine.
  - Fitness evaluation based on success rate, constraint structure, and generation depth.
  - Elite selection: top-performing variants are preserved across generations.
  - Variant cap (MAX_VARIANTS = 10) to prevent state bloat.
  - Version control: each variant tracks parent_id, generation, mutation type, and creation timestamp.
  - Supports multi-generation evolution in a single run.

- **`setup.sh`** — Installation and setup script:
  - Creates `~/self-smarter/` directory structure (state, logs, memory tiers, reflections, prompts).
  - Initializes config files: `routine_state.json`, baseline prompt variant, sample memory entry.
  - Sets up cron job for 2:00 AM daily execution.
  - Idempotent: safe to run multiple times without side effects.
  - Verification step: checks Python3, script existence, directory structure, and runs dry-run test.
  - Supports `--skip-cron` flag for environments without cron.

#### Templates (`templates/`)

- **`daily-reflection.md`** — Comprehensive daily reflection template with sections for:
  - Task performance summary (table format with complexity, outcome, time tracking).
  - Goal alignment check (weekly goals progress, monthly objectives).
  - Knowledge gap identification (context, what was missing, impact, action items).
  - Improvement opportunities (immediate, short-term, long-term).
  - Lessons learned (context, lesson, confidence level, related lessons).
  - Tomorrow's focus (prioritized task list with stretch goals).
  - Daily metrics dashboard (7-day trend comparison).
  - Includes example filled-in content for reference.

- **`weekly-evaluation.md`** — Detailed weekly evaluation template with sections for:
  - Week summary (narrative overview of accomplishments and challenges).
  - Key metrics dashboard (start/end comparison with targets and status indicators).
  - 4-week trend visualization (ASCII charts for error rate, token efficiency, budget).
  - Skill evolution status (prompt generation history, skills acquired, gaps remaining).
  - Memory health report (tier distribution, compaction results, quality assessment).
  - Prompt performance (variant testing results, fitness comparison, next evolution direction).
  - Improvement plan progress (previous plan status, blockers encountered).
  - Next week priorities (prioritized action items with stretch goals).
  - Appendix with raw daily breakdown data.
  - Includes example filled-in content for reference.

- **`improvement-plan.md`** — Structured improvement plan template with sections for:
  - Current state assessment (performance baseline, strengths, weaknesses).
  - Identified gaps (description, root cause, impact, evidence for each gap).
  - Proposed improvements (detailed description, expected impact, risk assessment).
  - Priority ranking (impact/effort/risk scoring matrix).
  - Resource requirements (time investment, infrastructure, token budget impact).
  - Success criteria (quantitative targets at 4 and 8 weeks, qualitative indicators, acceptance tests).
  - Timeline (week-by-week implementation plan with checkboxes).
  - Rollback plan (per-improvement and global rollback procedures).
  - Notes and dependencies (prerequisites, unmitigated risks, future considerations).
  - Includes example filled-in content for reference.

#### Documentation (Root)

- **`CHANGELOG.md`** — This file. Detailed version history following Keep a Changelog format.
- **`CONTRIBUTING.md`** — Contribution guidelines for extending the skill.
- **`SECURITY.md`** — Security policy and threat model.

### Design Decisions

#### Why File-Based State?
The system uses JSON files in `~/self-smarter/state/` rather than a database. This decision was made for several reasons:
1. **Simplicity** — No external dependencies (no SQLite, no Redis). Just files.
2. **Transparency** — State is human-readable and editable. Easy to debug.
3. **Portability** — State can be backed up, copied, or version-controlled.
4. **Sufficiency** — The data volume is small (kilobytes, not gigabytes). A database would be overkill.

#### Why Python Scripts Instead of Shell?
The core scripts are written in Python rather than bash for:
1. **JSON handling** — Native `json` module makes state management clean.
2. **Date arithmetic** — `datetime` module handles timestamp comparisons reliably.
3. **Extensibility** — Python's module system makes it easy to add new phases or metrics.
4. **Error handling** — Try/except blocks provide graceful degradation.

#### Why 4 Memory Tiers?
The HOT/WARM/COLD/ARCHIVE tier system was chosen over simpler approaches because:
1. **Access patterns vary** — Not all memories are equal. Frequently accessed patterns should be fast to retrieve.
2. **Natural lifecycle** — Information naturally becomes less relevant over time. Tiers model this decay.
3. **Compaction pressure** — Without lifecycle management, memory grows unbounded. Tiers provide natural archival.
4. **Inspired by OS page caching** — The tier system mirrors how operating systems manage memory pages.

#### Why Evolutionary Prompt Optimization?
Rather than manually tuning prompts, the system uses evolutionary algorithms because:
1. **Objective fitness** — Success rate and token efficiency provide measurable fitness signals.
2. **Exploration** — Mutation strategies explore prompt space that humans might not consider.
3. **Adaptation** — As task distributions change, prompts adapt automatically.
4. **Version control** — Every variant is tracked, enabling rollback to any previous generation.

#### Why 2 AM for Nightly Routine?
The 2 AM cron schedule was chosen because:
1. **Low activity** — Minimal user interaction at 2 AM WIB (Indonesia Western Time).
2. **Day boundary** — After midnight but before early morning, capturing the full previous day.
3. **Resource availability** — VPS load is lowest at night, ensuring consistent execution time.
4. **Recovery window** — If the routine fails at 2 AM, there's time to detect and fix before morning activity.

### Migration Notes

#### From Manual Reflection
If you were previously doing manual daily reflections (writing to `memory/YYYY-MM-DD.md`):
- The nightly routine's reflection phase creates entries in `~/self-smarter/state/reflections/` as JSON.
- To migrate existing reflections, convert markdown files to JSON format and place in the reflections directory.
- The `nightly_routine.py` script doesn't replace manual memory files — it complements them.

#### From Ad-Hoc Self-Auditing
If you were manually checking error rates or token usage:
- The `self_audit.py` script automates this collection.
- Audit data is stored in `~/self-smarter/state/audit_latest.json`.
- Historical audit data can be built by running the script daily (via the nightly routine).

#### From Manual Memory Management
If you were manually organizing memory files:
- The `memory_compact.py` script automates tier transitions.
- Existing memory files in `~/self-smarter/state/memory/` will be processed according to tier rules.
- Run with `--dry-run` first to preview transitions before executing.

---

## [Unreleased]

### Planned for v1.1.0
- Task-category-specific prompt evolution (separate variant pools per category).
- Hour-granularity memory access tracking.
- Nightly routine catch-up mechanism for missed executions.
- A/B testing framework for prompt variants.

### Planned for v1.2.0
- Cross-session learning (share lessons between agent instances).
- Real-time metric dashboard (web-based visualization).
- Sentiment analysis in reflection logs.
- Predictive error detection from historical patterns.

---

[1.0.0]: https://github.com/akdira/self-smarter-everyday/releases/tag/v1.0.0
