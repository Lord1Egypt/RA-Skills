# super_memori v4 — Learning Improvement Loop

## Purpose
Turn repeated failures, corrections, reuse signals, and recurring retrieval misses into reviewable manual-promotion candidates without pretending that promotion is fully automatic.

## Why this exists
Learning memory is useful only if repeated signals become visible.
A flat pile of lessons is not enough.
This workflow aggregates patterns so a human or strong maintenance run can decide what deserves durable manual promotion.

## Maintenance workflow
1. Run `health-check.sh`.
2. Confirm rollback exists.
3. Run `python3 mine-patterns.py` from the skill root.
4. Review the generated pattern report.
5. Promote only patterns that are repeated, specific, and not already covered.
6. Re-index memory after approved manual promotions.

## Recommended review cadence
On a CPU-rich host, run `python3 mine-patterns.py` proactively:
- after every 50 new learning entries
- at least once per week during active development
- before any major version bump of `super-memori`

If two consecutive reports show no new actionable clusters, the cadence may be reduced.

## What `mine-patterns.py` and telemetry surfaces should surface
- repeated failures by normalized block signature
- repeated user corrections
- recurring missing-knowledge queries
- lessons that were reused several times
- stale learnings that no longer match current practice
- likely duplicates that should be merged manually
- retrieval-audit signals such as recurring lexical-only fallbacks, domain-specific miss clusters, or index-fragmentation hints
- positive reuse signals that show which procedures keep working and may deserve durable promotion
- local telemetry signals such as `retrieval_miss`, `stale_success`, and `relation_traversal_hit`

## Recommended promotion threshold
Use promotion review only when at least one is true:
- the same lesson pattern appears 3+ times
- the same correction changes future behavior repeatedly
- the same retrieval miss appears across multiple sessions
- the same reusable procedure is successfully referenced multiple times

## Safe outputs
The pattern report should include:
- cluster id
- frequency
- first seen / last seen
- active window days
- representative title
- suggested target (`procedural`, `semantic`, `lessons`, or `review-only`)
- confidence note
- source file list
- retrieval audit signal (`none`, `lexical-fallback`, `miss-cluster`, `index-fragmentation`, or `review-needed`)
- reuse signal (`none`, `low`, `moderate`, or `high`)
- recency weight (`current`, `cooling`, or `stale`)
- stale success candidate flag
- signature when available

## Retrieval-audit handoff
Use the pattern report plus telemetry surfaces for two parallel review tracks:
1. promotion-candidate review for durable memory
2. retrieval-quality review for `index-memory.sh`, `health-check.sh`, repair classification, and degraded-mode diagnostics

The pattern report and telemetry surfaces remain review-only.
They may recommend retrieval-quality investigation, but they must not silently rewrite retrieval scripts or health thresholds.

## Safety rules
- Do not auto-promote directly from the pattern report.
- Do not delete source learnings automatically.
- Do not claim a pattern is durable truth just because it is frequent.
- Prefer reviewable reports over silent mutation.
- When a stale success candidate appears, manually verify that the procedure or lesson still works before promoting or retaining it as current best practice.

## Host assumption
This workflow assumes a strong CPU-only local host.
Use CPU-heavy batch analysis when it improves clustering or deduplication quality.
Do not pretend GPU-only paths are required.
