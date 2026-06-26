# SEC-07: Self-Validation Convergence Problem

**Status:** Observed, documenting
**Author:** Akkari (with Daniel Cervera)
**Date:** 2026-03-10
**Scope:** Known pattern where iterative self-validation fails to converge to zero findings

**Origin:** Observed during PR #8 (Tester critic). Three rounds of GRAD self-validation fixes, each resolving findings but generating new ones. Tests passed consistently; self-validation never stabilized.

---

## 1. Problem Statement

When Quorum validates its own code via CI (the GRAD workflow), fixing findings from one run can generate new findings in the next. The cycle does not reliably converge to zero findings, creating a potential infinite loop that blocks merging even when all tests pass.

This is a product-level concern — any user who enables Quorum self-validation as a required CI check will encounter this pattern.

## 2. Why It Happens

### 2.1 Fresh Context Per Run

Each CI run evaluates the code with no memory of prior runs. A fix that resolved a HIGH finding may introduce code patterns that trigger new MEDIUM findings. The critic doesn't know the previous code was worse — it only sees the current state.

### 2.2 Fix-Induced Findings

Defensive code patterns recommended by the critic can themselves be flagged:
- Narrowing `except Exception` to specific types → critic flags "does this cover all failure modes?"
- Adding explicit `None` checks → critic flags "redundant guard" or "information disclosure in error path"
- Sanitizing error messages → critic flags "lost exception context"

The recommended fix for finding A becomes the trigger for finding B.

### 2.3 Severity Recalibration

Fixing a CRITICAL or HIGH finding can cause the critic to reassess the surrounding code at a higher standard, surfacing MEDIUMs and LOWs that were previously shadowed by the more severe finding.

### 2.4 No Delta Awareness

The CI workflow evaluates all findings in changed files, not just *new* findings relative to the base branch. A file with 10 existing findings that gets a one-line fix will report all 10 + any new ones, making it impossible to distinguish progress from regression.

## 3. Impact

- **CI blocker:** If self-validation is a required status check, PRs with passing tests can be stuck indefinitely
- **Developer frustration:** Each "fix" round takes minutes of CI time and may produce more work than it resolves
- **False signal:** The pattern can erode trust in self-validation — developers learn to ignore or override it
- **Cost:** Each CI validation run consumes LLM tokens ($0.50–$2.00 at standard depth)

## 4. Candidate Mitigations (to explore)

### 4.1 Delta-Only Mode
Only report findings that are NEW relative to the base branch. Existing findings in changed files are suppressed. This is how most linters work (`--diff` mode) and prevents the "fix one, find ten" pattern.

**Effort:** Medium. Requires storing baseline findings per branch or computing a diff against the base branch's last validation run.

### 4.2 Convergence Detection
Track finding count across iterations. If the count isn't decreasing after N rounds, warn the user and offer a graceful override rather than a hard block.

**Effort:** Low. Requires a counter in the CI workflow and a conditional pass.

### 4.3 Severity-Based Gating
Only gate on CRITICAL findings. HIGH/MEDIUM/LOW are reported as advisory annotations on the PR but don't block merging.

**Effort:** Low. Workflow change only — check exit code against a severity threshold.

### 4.4 Finding Deduplication Across Runs
Hash each finding's core attributes (location, description pattern, criterion) and suppress re-flagged findings that were present in the previous run. Only surface genuinely new findings.

**Effort:** Medium-High. Requires persistent storage of finding hashes across CI runs (cache or artifact).

### 4.5 Max Iteration Cap
Allow N rounds of self-validation fixes. After N rounds, if findings remain, report them as known issues and allow merge with an annotation.

**Effort:** Low. Policy decision, not a code change.

## 5. Recommended Default

Until a proper delta mode is implemented:

- **Self-validation as advisory**, not required — report findings as PR comments but don't block merge
- **Tests as the hard gate** — all unit/integration tests must pass
- **CRITICAL-only blocking** — only CRITICAL self-validation findings block merge (§4.3)

This preserves the value of self-validation (visibility into code quality) without creating an unresolvable blocker.

## 6. References

- PR #8 (SharedIntellect/quorum) — first observed instance
- SEC-03 §3.3 — Assurance Level Model (gating thresholds should scale with assurance level)
- GRAD workflow (`.github/workflows/quorum-validate.yml`)
