# wreckit Build-Out Gameplan
_Sequential execution. Update status as each task completes._

## Status Legend
- [ ] TODO
- [🔄] IN PROGRESS
- [✅] DONE
- [❌] BLOCKED

---

## Task 1: Fix Orchestrator Collect Pattern
**Goal:** Make swarm actually work. No more fabricated results.
**Files:** `references/swarm/orchestrator.md`, `references/swarm/collect.md`, `references/swarm/orchestrator-prompt.md`, `scripts/run-audit.sh`
- [x] Rewrite orchestrator.md — explicit collect loop, anti-fabrication rules, timeout handling
- [x] Create orchestrator-prompt.md — copy-pasteable system prompt with hardcoded collect pattern
- [x] Update collect.md — verification checklist, concrete timeout/error examples
- [x] Create scripts/run-audit.sh — CLI bootstrap that validates config + outputs ready-to-paste orchestrator task
- [x] Fix broken path references (~/Projects/wreckit/ → ~/Projects/wreckit-ralph/) in orchestrator.md + orchestrator-prompt.md
**Status:** [✅] DONE — 2026-02-21

---

## Task 2: Adversarial Red-Team Gate
**Goal:** Actually find security bugs, not just describe what to look for.
**Files:** `references/gates/red-team.md`, `scripts/red-team.sh`
- [x] Gate definition — injection, logic bypass, input abuse, concurrency, resource exhaustion, crypto, error handling
- [x] Script — grep for 20+ vulnerable patterns, run adversarial inputs, JSON report
- [x] Test against ~/Projects/ipeaky/
**Status:** [✅] DONE — red-team.md gate + red-team.sh script (286 lines, 20 vulnerability patterns, JSON report).

---

## Task 3: Differential Testing Gate
**Goal:** Compare implementation against oracle/reference, catch "plausible but wrong" logic.
**Files:** `references/gates/differential.md`, `scripts/differential-test.sh`
- [x] Gate definition — oracle comparison, metamorphic testing, golden tests
- [x] Script — detect oracle, run both, diff outputs, JSON report (271 lines)
- [x] property-based.md + property-test.sh (356 lines, framework detection, stubs for Python/TS/Rust)
**Status:** [✅] DONE

---

## Task 4: Property-Based Testing Gate
**Goal:** Fuzz with random/boundary inputs, find crashes nobody wrote a test for.
**Files:** `references/gates/property-based.md`, `scripts/property-test.sh`
- [x] Gate definition — invariant extraction, fast-check/hypothesis/quickcheck, crash corpus
- [x] Script — detect framework, check if property tests exist, generate stubs if none, run fuzzer, JSON report (356 lines)
**Status:** [✅] DONE

---

## Task 5: Dynamic Analysis Gate
**Goal:** Memory leaks, race conditions, undefined behavior — things tests don't catch.
**Files:** `references/gates/dynamic-analysis.md`, `scripts/dynamic-analysis.sh`
- [x] Gate definition — sanitizers, heap profiling, race detection per language
- [x] Script — detect language, run appropriate tools (valgrind/asan/tsan/tracemalloc/go-race), JSON report (371 lines)
**Status:** [✅] DONE

---

## Task 6: Performance Benchmark Gate
**Goal:** Catch perf regressions, O(n²) patterns, memory blowups.
**Files:** `references/gates/performance.md`, `scripts/perf-benchmark.sh`
- [x] Gate definition — baseline establishment, regression thresholds (>20% = fail), load testing
- [x] Script — detect benchmark framework, run, compare vs baseline in .wreckit/, JSON report (373 lines)
**Status:** [✅] DONE

---

## Task 7: Upgrade Mutation Testing
**Goal:** Real mutation frameworks (Stryker/mutmut/cargo-mutants), not just AI text flips.
**Files:** `scripts/mutation-test.sh` (rewrite), `references/gates/mutation-kill.md` (update)
- [x] Stryker integration script (mutation-test-stryker.sh, 219 lines)
- [x] mutmut (Python) integration — detects, runs, falls back gracefully
- [x] cargo-mutants (Rust) integration — detects, runs --json, parses, falls back gracefully
- [x] Stryker detection in mutation-test.sh — calls mutation-test-stryker.sh if available
- [x] Fallback to AI mutations when no real tool available
- [x] "tool" field added to JSON output: mutmut / cargo-mutants / stryker / ai-mutations
**Status:** [✅] DONE — 2026-02-21

---

## Task 8: Rename + Republish
**Goal:** Remove Disney trademark risk. Rename wreckit-ralph → wreckit on GitHub + ClawHub.
- [x] Content renamed internally (SKILL.md name field = "wreckit")
- [x] Rename GitHub repo (christiancattaneo/wreckit-ralph → christiancattaneo/wreckit) ✅ 2026-02-21
- [x] Update local git remote to https://github.com/christiancattaneo/wreckit.git ✅
- [x] Published to ClawHub as wreckit v2.0.0 ✅ 2026-02-21
- [x] Updated installed skill locally (~/.openclaw/workspace/skills/wreckit/) ✅
**Status:** [✅] DONE — 2026-02-21

---

## Progress
- Tasks completed: 8/8 ✅ ALL DONE
- Last updated: 2026-02-21 09:45 CST
