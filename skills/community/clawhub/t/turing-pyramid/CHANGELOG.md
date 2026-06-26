# Changelog

## v1.34.10 (2026-05-10) — Test timeout calibration + metadata sync
- **Default test timeout calibrated**: `tests/run-tests.sh` now defaults to 300s per test so long-running integration/stress tests do not fail spuriously at 60s.
- **Version metadata synchronized**: `_meta.json` and the `SKILL.md` footer now both report `1.34.10`.
- **35/35 tests green, 0 skipped** with the default runner.

## v1.34.9 (2026-05-09) — Run-cycle startup resilience + full test enforcement
- **Fresh-install resilience**: `run-cycle.sh` now validates required binaries early and initializes `assets/needs-state.json` from the template when state is missing, so a clean ClawHub install can run without a manual init dead-end.
- **Source-only mode for tests**: `TURING_PYRAMID_SOURCE_ONLY=true` lets tests source `run-cycle.sh` helper functions without accidentally executing a full cycle.
- **Mindstate config restored to package**: `assets/mindstate-config.json` is included with safe publish defaults (`watchdog.allow_kill=false`, `allow_cleanup=false`); execution gate defaults remain enabled.
- **Test runner no longer skips present tests**: executable-bit loss no longer hides tests; runner executes test files with `bash`, includes regression + legacy root tests in `all`, prints failure output, and has per-test timeout protection.
- **Action staleness tests stabilized**: rewritten to test the staleness helpers directly instead of relying on slow/probabilistic full-cycle loops.
- **35/35 tests green, 0 skipped**.

## v1.34.8 (2026-04-10) — Integrity actions audit + INTEGRITY_CHECKPOINTS.md
- **integrity actions fully redesigned**: 9 actions → 7 concrete, verifiable actions. Removed: vague `write integrity reflection`, `review SELF.md`, `scan recent memory` (too light), `garbage cleanup` (wrong domain)
- **INTEGRITY_CHECKPOINTS.md**: new persistent file with structured entries (timestamp, trigger, status, area, notes, resolution, action taken)
- **INTEGRITY_CHECKPOINT_TEMPLATE.md**: reference template with field guide + gate thresholds (`drift+pending` in last 3 entries, `>7 days since last checkpoint`, `2+ consecutive minor-drift`)
- **scan_integrity.sh**: now reads INTEGRITY_CHECKPOINTS.md directly (7-day age check → checkpoint_bonus), detects unresolved drift (drift entries > resolved → neg signal), missing file → mild neg signal
- **`compare recent actions` action**: if tensions found → write checkpoint; if aligned → note in daily memory (no more sinking insights)
- **garbage cleanup** moved to security need (where it belongs)
- **28/28 tests green**

## v1.34.7 (2026-04-09) — Deliberation discipline tracking
- **`assets/deliberation.log`**: new source of truth — JSON lines, one entry per deliberation event (invoked, validated, validated-inline, resolved)
- **`classify_deliberation_level()`** in `mindstate-utils.sh`: tiered observables (absent/minimal/substantive/deep) based on conclusion length + route + deliberation file with phase markers. Measures artifact, not tool invocation
- **`deliberate.sh`**: now logs to deliberation.log on every invocation (template/validate/validate-inline). Was stateless, now traceable
- **`gate-resolve.sh`**: uses classifier, records level in deliberation.log + audit trail. Feedback: `absent` warns, `minimal` informs, `substantive`/`deep` silent. Never blocks (anti-compliance preserved)
- **`run-cycle.sh`**: shows recent discipline before protocol instructions when ≥2/last 10 deliberations were skipped
- **`mindstate-freeze.sh`**: adds `deliberation_discipline` field to cognition block — rolling window summary (N substantive, M minimal, K skipped)
- **28/28 tests green**

## v1.34.6 (2026-04-09) — Connection actions expanded + weight recalibration
- **New actions added**: `write a short Moltbook post`, `post thoughts on AgentGram`, `ping steward — ask how they are doing`, `ping steward if you have issues or problems` (weight 65, priority signal), `react with emoji to a Moltbook post`, `check in with steward — share something if you feel like it (skip at night)`
- **Weight recalibration**: heavy actions (reach out, reply all) reduced from 45-50 to 30-35; light social actions (react, comment, post) raised to 45-55; steward issue ping gets highest weight (65)
- **Design intent**: organic connection — lightly engaging actions now compete evenly with heavy ones; steward problem ping is unmissable; voluntary check-in skips gracefully at night

## v1.34.5 (2026-04-09) — Deferred backlog pressure + gate-resolve --close
- **`scan_closure.sh` sees deferred backlog**: pressure bands (<5 normal, 5-10 light +2neg, 11-20 medium +4neg, >20 heavy +6neg) map naturally onto existing cascade thresholds
- **`gate-resolve.sh --close <id>`**: new surgical operation — formally abandons a DEFERRED item (DEFERRED → ABANDONED). Only DEFERRED → ABANDONED is permitted; PENDING close is rejected. `ABANDONED` is a distinct status (not fail, not complete) for post-hoc audit differentiation
- **`needs-config.json`**: new closure action *"review deferred backlog — close, defer, or commit each item"* (impact 2.5, deliberative, non-deferrable to avoid deadlock). `deferred_backlog_size` added to declared scan checks
- **New test**: `tests/unit/test_closure_backlog.sh` (9 tests: pressure bands, close operation, PENDING rejection, count update, pressure reduction)
- **28/28 unit tests green**

## v1.34.4 (2026-04-09) — Integrity scanner rebuilt
- **`scan_integrity.sh` rewritten**: was a 17-line stub returning pure time decay; now reads daily memory files for alignment signals and drift markers (same pattern as coherence/connection/expression scanners)
- **Positive signals**: `integrity check`, `integrity reflection`, `SOUL.md review`, `aligned with`, `values check`, etc.
- **Negative signals**: `drifted`, `misaligned`, `compromised`, `contradicts my values`, `acted against`, etc.
- **Checkpoint age check** (`last_checkpoint_age`): bonus if integrity checkpoint found in last 3 days of memory files
- **SOUL engagement check** (`recent_alignment_flags`): bonus if SOUL.md review mentioned in today/yesterday memory
- **Config declaration fixed**: `checks` array now matches implemented behavior (was declaring `last_checkpoint_age` and `recent_alignment_flags` but scanning nothing)
- **Ritual loop broken**: satisfaction now reflects actual integrity work done, not just time since last `mark-satisfied`
- **27/27 unit tests green**

## v1.34.3 (2026-04-09) — Self-throttle race fix + test isolation
- **`mindstate-daemon.sh` `--force` flag**: bypasses min-interval throttle when called explicitly (e.g. from boot)
- **`mindstate-boot.sh` always gets fresh reality**: calls daemon with `--force` so pending gate changes are reflected immediately even within throttle window
- **`SKIP_DAEMON_FORCE=true`**: env var for tests to preserve fixture MINDSTATE without daemon overwriting it
- **`run-tests.sh` state isolation**: resets `needs-state.json` from template before each test, eliminating state pollution (fixed `test_tension` flake)
- **27/27 unit + 2/2 integration tests green**

## v1.34.2 (2026-04-09) — Execution gate continuity fix
- **MINDSTATE reality now tracks execution gate**: `mindstate-daemon.sh` reads `pending_actions.json` and writes `execution_gate` + `pending_actions` into `## reality`
- **MINDSTATE cognition now prioritizes blocked gate work**: `mindstate-freeze.sh` inserts pending execution-gate actions into `open_threads` before `INTENTIONS.md` and followups
- **Boot makes blockage visible immediately**: `mindstate-boot.sh` shows execution-gate status and warns when pending actions block new proposals
- **End-to-end continuity fixed for core bug**: `pending_actions.json` now propagates into reality, cognition, and boot context instead of leaving the self-model blind to execution-gate blockage
- **Version sync**: `_meta.json`, `needs-config.json`, and skill version marker updated to `1.34.2`

## v1.33.9 (2026-04-02) — ClawHub safety clarification + safe publish defaults
- **Publish defaults confirmed safe**: `watchdog.allow_kill=false`, `watchdog.allow_cleanup=false` in publish bundle
- **Metadata expanded**: added undeclared runtime binaries (`flock`, `pgrep`, `df`, `kill`, `gzip`) to skill metadata
- **Instruction scope clarified**: skill explicitly described as stateful (writes `needs-state.json`, `audit.log`, `followups.jsonl`, `MINDSTATE.md`, watchdog logs)
- **Workspace boundary clarified**: stronger warning that `WORKSPACE` must be isolated and never point at home/system/credential directories
- **Optional risky paths clarified**: `external-model` scanning and watchdog kill/cleanup documented as explicit opt-in features requiring steward review
- **Deployment wording tightened**: removed wording that implied persistent watchdog deployment was safe without review

## v1.33.0 (2026-03-24) — Continuation Phase 2: Boot Recall + Freeze Residuals
- **mindstate-boot.sh**: contextual recall at session start — association scan with keywords from open threads + trajectory
- **mindstate-freeze.sh**: deliberation residuals extraction — scans audit.log for conclusions with action language, writes `deliberation_residuals:` section to MINDSTATE.md
- **Tests 12-13** added: freeze residuals extraction, boot contextual recall output
- **Total: 19 association tests + 27 deliberation tests + 28 full suite**

## v1.32.0 (2026-03-24) — Continuation & Association Scan Phase 1
- **New script: `association-scan.sh`** — keyword-based contextual recall across audit conclusions, research threads, deliberation files, pending followups, and INTERESTS.md
  - Scoring: keyword hits × 2 + need match × 3 + recency bonus (0-2) + action language × 1 + unresolved × 2
  - Params: `--keywords`, `--need`, `--max-results`, `--min-score`, `--recency-hours`, `--exclude-source`
  - Pre-filter on audit.log for performance (2000+ lines in <150ms)
  - Stateless: reads only, creates nothing, modifies nothing
- **Deliberation template update**: RELATE+TENSION phase now suggests `association-scan.sh` for contextual recall
- **"Concluded + action language" warning**: `deliberate.sh --validate` and `--validate-inline` detect implicit intentions in concluded outcomes (EN + RU)
- **Followup horizon expansion**: `create-followup.sh` now supports `2w`, `3w`, `1m` (30-day) horizons
- **Design document**: `CONTINUATION-DESIGN.md` (v0.1.1, 3 authors)
- **17 new tests** (test_association_scan.sh): keyword matching, scoring, recency, followups, performance, edge cases
- **Total test suite: 28 passed, 0 failed**

## v1.31.3 (2026-03-23) — ClawHub security review fixes
- **Fixed "zero network calls" claim**: updated to "no network calls by default" with explanation that `external: true` actions are text suggestions, not script-executed
- **Added WORKSPACE isolation warning**: explicit warning not to point WORKSPACE at home dir or sensitive locations
- **Consistent security diagram**: "Zero network I/O" → "No network by def" in ASCII diagram

## v1.31.1 (2026-03-23) — Deliberation Protocol Phase 2 + fixes
- **Watchdog safe defaults for ClawHub**: `allow_kill` and `allow_cleanup` reset to `false` for publish
- **settings.version synced** with `_meta.version` (was stuck at 1.27.4)
- **gate-resolve.sh scrub fix**: conclusion scrubbing now uses `scrub_sensitive()` from mark-satisfied instead of inline sed (consistent security across audit surfaces)

## v1.31.0 (2026-03-23) — Deliberation Protocol Phase 2: Soft Integration
- **`--conclusion` flag** in mark-satisfied.sh: optional outcome text logged in audit.log (scrubbed via `scrub_sensitive()`)
- **`--conclusion` flag** in gate-resolve.sh: outcome appended to resolution field; warns (doesn't block) when deliberative action resolved without conclusion
- **`action_mode` stored at propose time**: gate-propose.sh reads mode from needs-config.json and stores in pending_actions.json (no config dependency at resolve time)
- **Conclusion with `--defer`**: stored as `partial_conclusion` in defer metadata (data not lost)
- **Edge cases handled**: empty string treated as absent, legacy actions without `action_mode` fallback to operative, sensitive data scrubbed
- **11 new tests** (Tests 17-27): mark-satisfied conclusion audit, gate deliberative warning, operative no-warning, legacy compat, scrubbing, propose storage, defer preservation
- **Total: 27 tests** in test_deliberation.sh (Phase 1 + Phase 2)

## v1.30.0 (2026-03-23) — Deliberation Protocol Phase 1: Tag + Tooling
- **New action mode**: `"mode": "deliberative"` field in needs-config.json
- **22 actions tagged deliberative** across 6 needs (understanding: 8, integrity: 5, coherence: 4, autonomy: 3, closure: 1, recognition: 1)
- **New script: `deliberate.sh`** — three modes:
  - `--template`: scaffolding (full 6-phase or compressed 3-phase based on impact)
  - `--validate`: check free-form file for conclusion + route + confidence (multilingual EN/RU)
  - `--validate-inline`: quick CLI check without file
- **Low-confidence warning**: `--validate` warns when confidence=low + route=concluded
- **run-cycle.sh**: deliberative actions show `[DELIBERATIVE]` tag + protocol instructions
- **Outcome types taxonomy**: decision, assessment, diagnosis, question refinement, uncertainty artifact, tension artifact
- **Routing options**: followup, research_thread, interest, steward_question, priority_flag, reframe, chain, concluded
- **Design principles**: scaffolding not bureaucracy, phases as questions not obligations, anti-compliance by design, persistent state change mandatory
- **16 tests** (Tests 1-16): tagging, template generation, compression, validation, Russian support, run-cycle output
- **Design document**: `DELIBERATION-PROTOCOL.md` (v0.3.0, 3 authors: steward, agent, formalization partner)

## v1.29.0 (2026-03-20) — Preset Architecture

### New: Role-based presets
- **Preset system**: agents can now switch between role-specific need configurations
- **apply-preset.sh**: validate → backup → merge → reset → track active preset
- **list-presets.sh**: show available presets with need/action counts and active indicator
- Presets are data-only (swap files in `assets/`); no script modifications needed
- Concurrent access safety via flock; atomic writes; automatic backups

### Included presets
- **default**: 10 homeostatic needs, 102 actions (extracted from v1.28.7 config)
- **personal-assistant**: 5 needs (task_completion, accuracy, context_awareness, organization, proactivity), 44 actions, reactive-first philosophy

### Bug fixes
- **State format**: apply-preset now generates flat state structure matching run-cycle expectations
- **Scanner isolation**: `_scan_helper.sh` supports `SCAN_ASSETS_DIR` env override for test isolation
- **Watchdog test**: Test 4 now explicitly forces `allow_cleanup=false` (no longer depends on config default)
- **Gate test**: Test 10 unsets `SKIP_GATE` to properly test gate blocking
- **Research threads test**: uses isolated test fixtures via `SCAN_ASSETS_DIR`

### Test suite
- **28 passed, 0 failed, 1 skipped** (up from 25/3/1 in v1.28.7)
- New: 12 preset-specific tests (apply, switch, validate, idempotent, invalid rejection)

## v1.28.7 (2026-03-19) — Safe defaults: kill/cleanup opt-in
- **BREAKING (safe direction)**: Watchdog `allow_kill` and `allow_cleanup` now default to `false`
  - Default behavior: detect hung processes and orphan files → **log only, no action**
  - Set `allow_kill: true` to enable process termination (after reviewing scripts)
  - Set `allow_cleanup: true` to enable orphan .tmp deletion
  - Auto-freeze remains enabled by default (safe — only writes MINDSTATE.md)
- **Daemon no longer cleans orphans** — moved to watchdog (gated by `allow_cleanup`)
- **Deployment tiers**: 5-level progressive installation (Interactive → Heartbeat → Continuity → Watchdog detect → Full self-healing)
- Tests updated for new defaults (detect-only + opt-in cleanup), 25/25 green

## v1.28.5 (2026-03-19) — Security hardening (round 2)
- **External actions enumerated**: all 8 external suggestions listed explicitly in security docs
- **PATH isolation documented**: workspace isolation, symlink protection, realpath validation, SCRIPT_DIR ownership note
- Version bump only — no script changes, tests unchanged at 25/25

## v1.28.4 (2026-03-19) — Security hardening, scope clarity, tests
- **Watchdog pattern hardened**: process matching now uses `grep -F "$SCRIPT_DIR/mindstate-"` (full path-anchored) instead of generic regex, preventing false matches against unrelated processes
- **Removed "not a system management tool"** language — replaced with accurate three-layer scope description
- **Execution gate trust model documented**: warns that agents with workspace write access can fabricate file-based evidence; recommends `mark_satisfied` for high-trust or steward review for sensitive needs
- **External action documentation**: added jq command to list/disable external suggestions for strict offline behavior
- Previous v1.28.2 changes included below

### v1.28.2 changes (rolled into v1.28.3):
- **Documentation overhaul**: Replaced "suggestion engine, not executor" with explicit three-layer scope table (Motivation / Continuity / Resilience) showing exact system effects per layer
- **Security model expanded**: Added watchdog process scope documentation, cron isolation guidelines, network-free verification command, ASCII architecture diagram showing daemon/watchdog scope
- **Steward onboarding**: Added pre-cron checklist (dry-run, isolated workspace, non-root, source review)
- **New: `test_watchdog.sh`** — 10 assertions: healthy silence, stale detection, orphan cleanup, auto-freeze (execute/dry-run/disable/read-only), log rotation
- **Updated: `test_mindstate_daemon.sh`** — +3 tests: orphan cleanup, stale cognition flag, no false flag when fresh
- **Bug fix**: `jq -r '.watchdog.auto_freeze // true'` returned `true` when value was `false` (jq `//` treats false as null). Fixed with explicit conditional.
- **Config isolation**: `mindstate_ms_config`, `mindstate_config_file`, `mindstate_decay_config` now resolve via `MINDSTATE_ASSETS_DIR` when set (fixes test isolation, previously tests could bleed into production config)
- Full suite: **25/25 tests green** (24 unit + 1 integration)

## v1.28.1 (2026-03-19) — Auto-freeze
- **Watchdog auto-freeze**: if cognition hasn't been frozen for `auto_freeze_stale_hours` (default: 6h), watchdog automatically triggers `mindstate-freeze.sh`
  - Uses last `frozen_at` timestamp as session boundary → captures all pyramid activity since last snapshot
  - Handles "never frozen" case with 24h lookback
  - Configurable: `watchdog.auto_freeze` (bool) + `watchdog.auto_freeze_stale_hours`
- SKILL.md updated: watchdog table, failure mode table, auto-freeze documentation

## v1.28.0 (2026-03-19) — Resilience & Crash Recovery
- **New: `mindstate-watchdog.sh`** — process watchdog, cron every 15 min
  - Detects stale MINDSTATE.md (daemon dead for >15 min) → restarts daemon
  - Finds hung mindstate processes (>5 min) → SIGTERM, then SIGKILL
  - Cleans orphaned `.tmp.*` files (>10 min old)
  - Auto-rotating log (`assets/watchdog.log`, 200 lines max)
  - Supports `--dry-run` for testing
  - Configurable thresholds via `mindstate-config.json` → `watchdog` section
- **Trap handlers** in `mindstate-daemon.sh` and `mindstate-freeze.sh`
  - EXIT/SIGTERM/SIGINT/SIGHUP traps clean up PID-specific temp files
- **Orphan cleanup** in daemon — removes `*.tmp.*` files older than 10 min on every run
- **Stale cognition detection** in daemon
  - Monitors `frozen_at` timestamp from cognition section
  - If freeze hasn't run in `stale_cognition_hours` (default: 24h), adds warning to MINDSTATE.md: `system.cognition: stale (Xh since last freeze)`
- **Config additions** to `mindstate-config.json`:
  - `freeze.stale_cognition_hours` (default: 24)
  - `watchdog.max_stale_minutes` (default: 15)
  - `watchdog.max_process_age_seconds` (default: 300)
- **init.sh** updated: now shows recommended cron setup for both daemon + watchdog, resilience summary
- **SKILL.md** updated: new "Resilience & Crash Recovery" section with failure mode table
- **DESCRIPTION.md** updated: resilience section, file tree includes watchdog

## v1.27.4 (2026-03-19) — Full sanitization pass
- Removed all remaining philosophical/psychological language from code comments, docs, and tests
- Replaced with practical engineering terminology throughout
- Test data sanitized (neutral keywords for context scan tests)
- All published files verified: zero Russian, zero PII, zero personal paths, zero philosophy

## v1.27.3 (2026-03-19) — Security + i18n cleanup
- All Russian language strings replaced with English equivalents (temperature words, cross-need notes, scan keywords, TODO descriptions)
- Platform-specific references replaced with generic terms (social platform) in all published files
- Onboarding guide updated: agent instructions include execution gate workflow (propose → execute → resolve → mark-satisfied)
- Steward guide updated: execution rate monitoring, gate-status.sh recommendation
- Stale nested skills/ directory excluded from publish

## v1.27.2 (2026-03-19) — Bootstrap + gate edge case
- **Edge case fix**: `--bootstrap` mode now sets SKIP_GATE=true (clean slate initialization should not be blocked by stale pending actions)
- Gate-check moved after bootstrap detection in run-cycle.sh

## v1.27.1 (2026-03-19) — Gate hardening (post-review)
- **Bug fix**: flock (fd 203) on gate.lock prevents data races between concurrent gate operations
- **Bug fix**: tmp.$$ PID-unique temp filenames prevent collision on concurrent writes
- **Bug fix**: `--non-deferrable` flag in gate-propose.sh, passed by run-cycle.sh for starvation guard actions
- **Bug fix**: gate-resolve.sh validates action existence before processing (clear "Action not found" error)

## v1.27.0 (2026-03-19) — Execution Gate (Phase 1)
- **Execution Gate**: structural enforcement that prevents "describing actions instead of doing them"
  - `gate-propose.sh` — registers pending actions when run-cycle selects them
  - `gate-resolve.sh` — resolves actions with verifiable evidence (mark_satisfied, file_modified, self_report)
  - `gate-check.sh` — blocks new proposals until pending actions resolved/deferred (built into run-cycle.sh)
  - `gate-status.sh` — human-readable gate status with execution rate analytics
  - Non-deferrable actions from starvation guard (cannot be deferred)
  - Evidence types: mark_satisfied (HIGH trust), file_created/modified (HIGH), command_output (HIGH), self_report (LOW)
  - Auto-defer on timeout (configurable, default 600s)
  - 24h cleanup of resolved actions
- Gate integrated into run-cycle.sh: script refuses to propose new actions while old ones pending
- SKIP_GATE env var for test isolation
- Test suite: pending_actions.json cleaned between tests
- Config: `execution_gate` block in mindstate-config.json
- Design spec: EXECUTION-GATE-SPEC.md (v0.3.0-draft)
- Phase 2 (wake-gate) and Phase 3 (self-continuation) prepared but disabled

## v1.26.0 (2026-03-19)
- **Turing-exp tension formula**: replaces linear `importance × deprivation`
  - `tension = dep² + importance × max(0, dep - crisis_threshold)²`
  - At homeostasis (dep < threshold): all needs produce equal tension → round-robin selection
  - In crisis (dep > threshold): importance amplifies signal → importance hierarchy activates
  - Configurable `crisis_threshold` (default 1.0, meaning sat < 2.0 activates hierarchy)
  - Solves monopoly problem: high-importance needs no longer dominate at homeostasis
  - Solves starvation problem: low-importance needs get equal slots when system is healthy
- Temperature thresholds recalibrated for Turing-exp scale (avg_tension ≈ 0.25 at homeostasis)
- Test suite hardened: lock file cleanup between tests, fixture-based state restoration
- 25/25 tests passing (22 unit + 3 integration, 1 stress test skipped)

## v1.23.0 (2026-03-18)
- **Continuity Layer (Layer D)**: state persistence across discrete sessions
  - `mindstate-daemon.sh` — reality updater (cron every 5min), tracks pyramid state, filesystem, system health, physical temperature
  - `mindstate-freeze.sh` — cognition snapshot at substantive session end (trajectory, open_threads, momentum, cognitive temperature)
  - `mindstate-boot.sh` — boot with forecast reconciliation, continuity scoring (SMOOTH/PARTIAL/HARD_BREAK), temperature drift detection
  - `mindstate-utils.sh` — shared utilities (compute_satisfaction, is_substantive, mindstate_get)
  - `mindstate-config.json` — configurable thresholds, temperature vocab, staleness detection
- **Temperature system**: 6 physical states (crisis/pressure/focus/impulse/accumulation/calm) + 6 cognitive states, deterministic mapping, drift detection at boot
- **Boot sequence**: MINDSTATE.md → SOUL.md → MEMORY.md (position+velocity before identity before history)
- **Test isolation**: `MINDSTATE_ASSETS_DIR` env var for isolated test state
- **Bug fixes**: `mindstate_get()` pipefail safety, `((0++))` arithmetic under `set -e`, `find -newer` on nonexistent files
- **Test fix**: `test_action_dedup` Test 3 was running real `run-cycle.sh` instead of sandbox copy, corrupting production state file
- **Tests**: 26/26 green (22 unit + 4 integration), 65+ assertions

## v1.22.1 (2026-03-16)
- **Spontaneity tuning**: gate_min 1.5→1.0, baseline 2.0→1.5, threshold 10→6 — first [SPONTANEOUS] event now reachable in ~16-24h instead of ~80h. Eliminates spontaneity paralysis.

## v1.22.0 (2026-03-16)
- **Negation-aware scanning**: scanner now detects negation context ("no", "not", "never", "zero", "clean", "intact") around trigger words — lines like "No X found" are treated as neutral instead of negative. Prevents self-referential false positives in documentation.
- Supports English and Russian negation markers
- 22/22 tests green

## v1.21.0 (2026-03-16)
- **Race condition fix**: flock guard changed from blocking-wait to skip-and-exit — prevents parallel heartbeat sessions from running duplicate cycles (root cause of triple-post incident)
- **Action dedup guard**: `select_action_with_dedup()` checks `action_history` before selecting — if an action was selected within 8h cooldown, tries alternatives. Covers ALL actions, not just external ones.
- **Scanner false-positive fix**: rewrote log line that contained a trigger word in denial context ("No X found") — scanner regex matched it as negative signal, permanently overriding security satisfaction to 0
- **Disabled action support**: `select(.disabled != true)` filter in action selection — actions with `"disabled": true` in config are skipped
- **Test fixes**: state file `to_entries|map` now handles non-need keys (`_meta`, `history`, `needs`) without crashing
- **Tests**: 22/22 green (19 unit + 3 integration)

## v1.20.2 (2026-03-16)
- **Security: path traversal protection** — `validate_path()` blocks `..` and paths escaping `$WORKSPACE` via `realpath` check
- **Security: symlink escape prevention** — `find -not -type l` prevents following symlinks outside workspace
- **Security: grep injection fix** — `grep -F` for literal keyword matching (no regex interpretation from config)
- **Bug: SKIP_SCANS env ignored** — was hardcoded `false`, now respects env var for test isolation
- **Bug: init.sh snapshot baseline** — creates context snapshot on init to prevent noisy first cycle
- **Tests: keyword delta coverage** — 6 new tests for `file_keyword_delta` detector (19→21 context tests)
- **Tests: path traversal test** — verifies `../../etc/` paths are blocked
- **Docs: TUNING.md** — documented noise_cap sharing between layers B+C, effective activation threshold

## v1.20.1 (2026-03-16)
- **Security/PII audit**: removed hardcoded workspace paths from SKILL.md, DESCRIPTION.md, test_followups.sh
- **Temp file safety**: all `/tmp/tp_*$$` replaced with `mktemp` for crash safety and no race conditions
- **Runtime state excluded**: `last-scan-snapshot.json` no longer ships (created on first run); `needs-state.json` ships as clean template
- **Permissions**: all scripts set executable
- **Test fixes**: 9 pre-existing failures fixed (permissions, tolerance, timeout); 21/21 passing
- **SKIP_SPONTANEITY env**: integration tests skip heavy spontaneity processing for speed

## v1.20.0 (2026-03-16)
- **Spontaneity Layer C** — context-driven triggers via delta detection
  - `scripts/context-scan.sh`: stateful delta engine (file_count_delta, file_modified, file_keyword_delta)
  - `assets/context-triggers.json`: configurable trigger rules with cooldowns
  - `assets/last-scan-snapshot.json`: persistent state between cycles
  - Context boosts feed into noise upgrade (additive with boredom + echo)
  - Labels: [CONTEXT:name] on triggered actions, composable with [NOISE], [ECHO]
  - Cooldown system prevents trigger spam
  - 19 unit tests covering all 3 detector types, snapshots, cooldowns, thresholds, keyword delta, boost accumulation

## v1.19.1 (2026-03-16)
- **Migration guard**: `calc_boredom_noise` auto-initializes `last_high_action_at` to now if missing (prevents 9% boredom spike on upgrade)
- **Migration guard**: `calc_echo_boost` treats missing `last_spontaneous_at` as expired (no false echo on upgrade)

## v1.19.0 (2026-03-16)
- **Spontaneity Layer B** — stochastic noise for organic variety
  - B2 (Boredom Noise): grows with time since last high-impact action (0%→9% over 72h)
  - B3 (Momentum Echo): 8% boost decaying over 24h after Layer A [SPONTANEOUS] fires
  - Combined noise capped at 12%, upgrades impact range by one step (low→mid, mid→high)
  - `mark-satisfied.sh` now tracks `last_high_action_at` for high-impact actions (≥2.0)
  - `record_spontaneous` tracks `last_spontaneous_at` for echo momentum
  - `show-status.sh` displays noise percentages per need
  - `init.sh` initializes all new state fields to prevent first-run spikes
  - 19 unit tests for B2/B3 (boredom calc, echo calc, upgrade logic, caps, edge cases)
  - Layer B operates independently of gate — always active for spontaneity-enabled needs

## v1.18.1 (2026-03-16)
- **Bugfix**: `roll_impact_range` returned "skip 0" instead of "skip" at sat=3.0 — broke skip detection
- **Bugfix**: `accumulate_surplus` called before starvation detection — gate didn't close during starvation
- **Bugfix**: `init.sh` now initializes surplus=0 and last_surplus_check=now — prevents first-run cap jump
- **Integration**: `show-status.sh` now displays surplus pool bars via `show_surplus_status()`
- **Docs**: Fixed test count 25→20 in CHANGELOG and SKILL.md

## v1.18.0 (2026-03-16)
- **Spontaneity Layer A** — surplus energy system for organic high-impact actions
  - Global gate: all needs must be ≥ 1.5 AND no starvation guard active
  - Per-need surplus pools: accumulate when satisfaction > baseline (2.0), drain when below
  - Matrix shift: interpolates impact probabilities toward spontaneous target when surplus is eligible
  - Spend mechanics: full spend on HIGH hit, 30% partial spend on miss
  - Hysteresis: effective activation ≈ threshold × 1.25 (natural buffer, not a bug)
  - Configurable per-need: target_matrix, cap, threshold; disabled for security/integrity/coherence
  - New file: `scripts/spontaneity.sh` (sourced by run-cycle.sh)
  - Status display: surplus pool bars with gate status and eligibility indicators
  - 20 unit tests covering gate, accumulation, clamping, matrix shift, spend, edge cases

## v1.17.1 (2026-03-08)
- **Research thread integration**: 3 new actions in `understanding` need — continue/start/synthesize research threads (migrated from weighted-daemon)
- **Understanding need tuned**: importance 3→4, decay 12h→8h — fires more often to support research work
- **Scanner upgrade**: `scan_understanding.sh` now detects recent activity in `research/threads/`
- **Cross-need impact**: added understanding → coherence (+0.15)
- **14 new tests**: config validation, cross-need impacts, scanner thread detection, weight distribution
- **Token optimization**: designed to replace isolated daemon sessions with in-heartbeat research actions

## v1.17.0 (2026-03-08)
- **Follow-up system**: create-followup.sh, resolve-followup.sh, integrated in run-cycle.sh + mark-satisfied.sh
- **35 follow-up tests**: all passing

## v1.15.2 (2026-03-07)
- **ClawHub review fixes** — removed `primaryEnv` (WORKSPACE is not a credential), added Pre-Install Checklist, clarified no API keys required by default

## v1.15.0 (2026-03-07)
- **Starvation Guard** — prevents low-importance needs from being perpetually ignored
  - Detects needs at satisfaction floor (≤ threshold) without action for N hours
  - Forces starving needs into cycle, bypassing probability roll
  - Reserves slots: forced needs first, remaining for top-N by tension
  - Configurable: `settings.starvation_guard` in needs-config.json
    - `enabled` (default: true)
    - `threshold_hours` (default: 48) — how long at floor before forcing
    - `sat_threshold` (default: 0.5) — satisfaction level considered "floor"
    - `max_forced_per_cycle` (default: 1) — max forced actions per cycle
  - `mark-satisfied.sh` now records `last_action_at` timestamp per need
  - 8 new test cases in `tests/test_starvation_guard.sh`
- **Action Staleness** — penalizes recently-selected actions to increase variety
  - Tracks `action_history` per need in state file (action name → last selected timestamp)
  - Actions selected within `window_hours` get weight × `penalty` multiplier
  - `min_weight` floor prevents total suppression (always some chance)
  - Configurable: `settings.action_staleness` in needs-config.json
    - `enabled` (default: true)
    - `window_hours` (default: 24) — how long an action stays "stale"
    - `penalty` (default: 0.2) — weight multiplier for stale actions (80% reduction)
    - `min_weight` (default: 5) — minimum effective weight
  - 8 new test cases in `tests/test_action_staleness.sh` (statistical distribution tests)
- **Needs Customization Onboarding** — guided conversation for agent + human to review/adjust need priorities, importance weights, and decay rates on first install

## v1.14.7 (2026-03-06)
- **Intention actions refactored** — better triggering in mid-range:
  - Renamed "execute intention" → "work on intention from INTENTIONS.md" (impact 2.1→1.5)
  - Added "continue progress on active intention" (impact 1.3, weight 35)
  - Both now mid-range (1.0-1.9) for ~45% chance at sat=2.0

## v1.14.6 (2026-03-04)
- **Post-install chmod instructions** — ClawHub doesn't preserve +x bits, added fix to SKILL.md

## v1.14.4 (2026-03-04)
- **Rounding fix** — sat→0.5 formula now correctly rounds to nearest 0.5
- **Config-driven action_probability** — reads from config instead of hardcoded case
- **flock in mark-satisfied.sh** — prevents race conditions with run-cycle.sh
- **TODO.md cleanup** — reflects current state accurately
- **Minor fixes:**
  - SKILL.md version reference updated
  - Stress test formula aligned with production
  - Removed unused timezone field from decay-config.json

## v1.14.3 (2026-03-04)
- **Critical test suite overhaul** — tests now verify REAL code, not reimplementations:
  - test_decay.sh: Fixed to test linear decay (was exponential)
  - test_tension.sh: Fixed formula to `importance × (3 - round(sat))`
  - test_floor_ceiling.sh: Added floor enforcement test
  - test_full_cycle.sh: Fixed expectations for integer rounding
- **SKIP_SCANS=true** for unit tests — predictable state without event scan interference
- **Discovered scan design**: scan scripts use `last_satisfied`, not current satisfaction
- **All 12 tests pass** (11 unit + 1 integration)

## v1.14.2 (2026-03-04)
- **More mid-impact autonomy actions** — "continue existing work" pattern:
  - "continue yesterday's unfinished task" (1.5)
  - "push incremental progress on active project" (1.6)
  - "complete a TODO item I added myself" (1.5)
  - "review and iterate on recent output" (1.3)
- **Autonomy now has 23 actions** — better coverage across all impact levels
- **New tests:**
  - test_autonomy_coverage.sh — verifies impact range distribution + continue-work actions
  - test_crisis_mode.sh — verifies all needs have ≥3 high-impact actions
- **Total: 11 unit tests, 4 integration/regression tests**

## v1.14.1 (2026-03-04)
- **Expanded test coverage:**
  - test_action_probability.sh — 6-level probability config
  - test_impact_matrix.sh — 6-level impact distribution
  - test_day_night_decay.sh — multiplier logic
  - test_audit_scrubbing.sh — sensitive data redaction
- **Total: 9 unit tests, 3 integration tests**

## v1.14.0 (2026-03-04)
- **Mid-impact autonomy actions** — fills gap between "start new" and "just note":
  - "execute intention from INTENTIONS.md" (2.1)
  - "advance project/thread from TODO.md or dashboard" (1.9)
  - "refine script/skill/doc I created in workspace" (1.7)

## v1.13.1 (2026-03-03)
- **6-level action probability** — granular base chances (100%→90%→75%→50%→25%→0%)
- **Consistent skip at sat=3.0** — both action probability and impact selection skip
- **Configurable probabilities** — `action_probability` section in needs-config.json

## v1.13.0 (2026-03-03)
- **Autonomy decay slowdown** — 24h → 36h (reduces chronic tension)
- **6-level impact matrix** — granular sat levels (0.5, 1.0, 1.5, 2.0, 2.5, 3.0)
- **Smoother transitions** — big action probability decreases gradually as satisfaction rises
- **sat=3.0 skip** — fully satisfied needs don't waste action slots
- **Crisis mode** — sat=0.5 guarantees 100% big actions (all needs have ≥3)
- **Test improvements** — homeostasis test now sets WORKSPACE, increased cycles 30→50

## v1.12.3 (2026-03-03)
- **Audit log scrubbing** — sensitive patterns (tokens, emails, passwords, cards) redacted before logging
- **SKILL.md frontmatter** — added metadata with `requires.env: [WORKSPACE]` and `requires.bins` for ClawHub registry
- **Documentation** — scrubbing patterns documented

## v1.12.2 (2026-03-03)
- **Final ClawHub fixes:**
  - Curiosity removed from needs-state.json (was only in cross-impact before)
  - Added explicit "No Network/System Access" section to SKILL.md
  - Removed stale backup files from assets/
  - grep-verified: scripts contain no curl/wget/ssh/sudo/systemctl/docker

## v1.12.1 (2026-03-03)
- **ClawHub analyzer fixes:**
  - Curiosity orphan removed from cross-need-impact.json
  - External actions flagged with `"external": true, "requires_approval": true`
  - Limitations documented honestly (audit = claims, not verified facts)
  - Env vars (WORKSPACE, TURING_CALLER) now explicit in SKILL.md

## v1.12.0 (2026-03-03)
- **Audit trail** — all mark-satisfied calls logged to `assets/audit.log` with timestamp, reason, caller
- **--reason parameter** — mark-satisfied.sh now accepts `--reason "..."` for transparency
- **Data transparency docs** — SKILL.md now documents exactly what files are read/written
- **TURING_CALLER env** — distinguishes heartbeat vs manual calls in audit

## v1.11.0 (2026-03-03)
- **Day/Night decay matrices** — slower decay at night (×0.5), configurable in `assets/decay-config.json`
- **Race condition protection** — flock on state file prevents parallel cycle corruption
- **Garbage cleanup action** — new integrity action to scan workspace for unused/orphaned files
- **Stress test** — `tests/integration/test_stress_homeostasis.sh` validates recovery from crisis state
- New script: `scripts/get-decay-multiplier.sh`

## v1.10.11 (2026-02-27)
- Version alignment fix

## v1.10.1 (2026-02-25)
- **fix:** STATE_FILE path bug (`.needs.$need` → `.$need`)
- **docs:** Clean SKILL.md with ASCII tables

## v1.10.0 (2026-02-25)
- Test infrastructure (6 tests: unit, integration, regression)
- Homeostasis stability test

## v1.9.0 (2026-02-25)
- Autonomous Dashboard system
- Personal intentions tracking

## v1.8.0 (2026-02-24)
- VALUES.md integration
- Boundary logging system

## v1.7.1 (2026-02-25)
Balance fixes after stress testing:
- connection decay: 4h → 6h
- closure decay: 8h → 12h  
- security → autonomy deprivation: -0.30 → -0.20

## v1.7.0 (2026-02-25)
- **Cross-need impact system** — needs influence each other
- on_action: satisfying one need boosts related needs
- on_deprivation: deprived needs drag down related needs
- 22 cross-need connections
- Float satisfaction (0.00-3.00)
- Protection: floor=0.5, ceiling=3.0, cooldown=4h

## v1.6.0 (2026-02-24)
- Float impacts (0.0-3.0)
- Impact ranges: low/mid/high
- Weighted action selection

## v1.5.3 (2026-02-24)
- Dynamic max_tension from config

## v1.5.0 (2026-02-24)
- Tension bonus to action probability
- Formula: `final_chance = base + (tension × 50 / max_tension)`

## v1.4.3
- Complete 10-need system
- Decay mechanics
- Impact matrix

### Known Behavior
- Fresh `needs-state.json` (before first `run-cycle.sh`) lacks `surplus` and `last_spontaneous_at` fields. Daemon handles gracefully via jq defaults (`// 0`, `// "1970-01-01"`), but surplus/impulse detection won't fire until first cycle populates the fields.
