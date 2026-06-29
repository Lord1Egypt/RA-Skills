# Example: safe web-to-Markdown capture

## Identity

- ID: `example-web-capture-evaluation-20260616`
- Status: `awaiting_review`
- Phase: `finalize`
- Created at: 2026-06-16T11:56:27Z
- Updated at: 2026-06-16T13:11:30Z
- 🔍 Awaiting human review before final completion

## Goal

Prepare a public-safe repository example for Research Mode about safe web-to-Markdown capture in agent research workflows: what risks matter, what workflow should an agent follow, and what artifacts make the example useful for users evaluating the project.

## Progress snapshot

- Iterations: 7 / 8
- Meaningful iterations: 7
- Last iteration at: 2026-06-16T13:07:09Z
- Last meaningful progress at: 2026-06-16T13:07:09Z
- Last transition: clear-bound-job
- Last reason: awaiting_review:passed-validation
- Last terminal reason: -
- Low-yield streak: 0 / 2
- Topic saturated: no
- Failures: 0 (consecutive 0)
- Milestone cadence: every 2 meaningful iterations

## Budget

- Budget phase: `soft_limit`
- Iteration budget: 7 / 8 (88%)
- Source budget: 7 / 18 (39%)
- Soft limit threshold: 80%
- Dominant limit: iterations
- Runtime budget: 75.05 / 180.0 min (42%)

## Adequacy

- Status: `passed`
- Attempts: 1 / 2
- Recommended next phase: `finalize`
- Recommended next angle: Run the finalization phase to package the candidate directory as the human-reviewable deliverable.
- Operator next action: `-`

## Working memory

### Summary

Finalization pass completed for the public-safe web-capture example package. The package contains the required five files, uses English public-repository prose, cites primary/official sources, documents the no-live-capture limitation, and passed the saved verification helper with no missing files, privacy issues, source gaps, or coverage gaps.

### Next angle

Lifecycle completion; no further research is needed unless a reviewer requests a synthetic capture fixture.

### Constraints

- No private workspace paths, chat-system identifiers, personal memories, tokens, or local-only tool names in final example files.
- Final deliverable must be a directory/package, not a raw internal workspace dump.

### Deliverable

A review-ready multi-file example package suitable for copying into the public repo under examples/web-capture-evaluation/: README.md, prompt.md, research-plan.md, sources.md, final-report.md. Keep it provider-neutral and avoid private paths, real chat ids, tokens, or OpenClaw-local personal context.

### User instructions

- Write all user-facing example materials in English for the public repository.
- Prefer direct official docs and primary sources for claims about web capture, Markdown conversion, URL safety, redirects, robots/politeness, and prompt-injection handling.

### Open questions

- Formal adequacy verification still needs to confirm that the generated package is sufficient for finalization.
- The package intentionally omits a live capture transcript to avoid redistribution and unsanitized-capture concerns; this is documented as a limitation rather than a blocker for the requested five-file example.

## Analysis runtime

- Runtime prepared: no
- Runtime tool: -
- Venv python: -
- Installed packages: -
- SQLite ready: no
- Default SQLite DB: <research-root>/example-web-capture-evaluation-20260616/workspace/data/analysis.sqlite
- SQLite schema path: <research-root>/example-web-capture-evaluation-20260616/workspace/analysis/schema.sql
- SQLite queries dir: <research-root>/example-web-capture-evaluation-20260616/workspace/analysis/queries
- Screenshots dir: <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/screenshots
- Vision dir: <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/vision
- Last iteration used code: yes
- Code used recently: yes
- Last code run at: 2026-06-16T13:07:09Z
- Last iteration used DB: no
- Database used recently: no
- Last database run at: -
- Last iteration used vision: no
- Vision used recently: no
- Last vision run at: -
- Last analysis artifacts:
  - [script] workspace/analysis/verify_package.py — Re-runnable package validation helper used for the finalization check.
  - [artifact] workspace/analysis/verify-package-report.json — Saved verification output showing required files, source coverage, safety-term coverage, and privacy scan results.
  - [artifact] workspace/outputs/web-capture-evaluation — Review-ready five-file public example package candidate.

## Corpus

- Mode: `web`
- Files attached: 0

## Completion validation

- Passed: yes
- Triggered by: worker
- Phase: finalize
- Evidence: sources=7, findings=30

## Validation scorecard

- Status: `passed`
- Attempts: 2 / 3
- Last validated at: 2026-06-16T13:07:09Z
- Operator next action: `review_candidate` — Review candidate deliverable
  - Rationale: The worker supplied passing finalization evidence and the task is gated for human review.
- Inferred user need: A human-reviewable, public-safe repository example package that can be copied into examples/web-capture-evaluation/ to demonstrate safe web-to-Markdown capture in agent research workflows.
- Intended recipient: Repository maintainer or evaluator reviewing the Research Mode example package before public inclusion.
- Primary deliverable kind: package
- Artifact roles: internal=3, candidate=1
- Validation evidence:
  - [evidence] -
  - [evidence] -
  - [evidence] -
  - [evidence] -
  - [evidence] -
- Checks: 8/8 passed
  - finalization_trace: PASS (ok)
  - candidate_artifact_inspection: PASS (ok)
  - package_deliverable_quality: PASS (ok)
  - draft_artifacts: PASS (ok)
  - human_readiness: PASS (ok)
  - naming_hygiene: PASS (ok)
  - delivery_manifest: PASS (ok)
  - deliverable_contract: PASS (ok)

## Delivery

- Ready: no
- Primary file: <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/README.md
- Attachments:
  - <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/final-report.md
  - <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/prompt.md
  - <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/sources.md
  - <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/research-plan.md
  - <research-root>/example-web-capture-evaluation-20260616/workspace/outputs/web-capture-evaluation/README.md

## Recent run outcomes

- iter=7 | phase=finalize | outcome=awaiting_review | reason=awaiting_review:passed-validation | Finalization pass completed for the public-safe web-capture example package. The package contains the required five files, uses English public-repository prose…
- iter=6 | phase=finalize | outcome=finalize | reason=continued:iteration-complete | Finalized the review-ready five-file public example package for safe web-to-Markdown capture. Re-ran the verification helper, confirmed required files, source…
- iter=5 | phase=verify | outcome=idle | reason=continued:iteration-complete | Verified the generated five-file web-capture example package against the goal, constraints, source coverage, and publication-safety requirements. The package i…

## Artifacts

- State: `<research-root>/example-web-capture-evaluation-20260616/state.json`
- Sources JSONL: `<research-root>/example-web-capture-evaluation-20260616/sources.jsonl`
- Findings JSONL: `<research-root>/example-web-capture-evaluation-20260616/findings.jsonl`
- Iterations dir: `<research-root>/example-web-capture-evaluation-20260616/iterations`
- Input dir: `<research-root>/example-web-capture-evaluation-20260616/input`
- Corpus dir: `<research-root>/example-web-capture-evaluation-20260616/input/corpus`
- Corpus manifest: `<research-root>/example-web-capture-evaluation-20260616/input/corpus-manifest.json`
- Runs TSV: `<research-root>/example-web-capture-evaluation-20260616/runs.tsv`
- Playbook: `<research-root>/example-web-capture-evaluation-20260616/task-playbook.md`
- Workspace dir: `<research-root>/example-web-capture-evaluation-20260616/workspace`
- Workspace analysis dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/analysis`
- Workspace tools dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/tools`
- Workspace data dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/data`
- Workspace outputs dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/outputs`
- Workspace tmp dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/tmp`
- Workspace screenshots dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/outputs/screenshots`
- Workspace vision dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/outputs/vision`
- SQLite DB path: `<research-root>/example-web-capture-evaluation-20260616/workspace/data/analysis.sqlite`
- SQLite schema path: `<research-root>/example-web-capture-evaluation-20260616/workspace/analysis/schema.sql`
- SQLite queries dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/analysis/queries`
- SQLite imports dir: `<research-root>/example-web-capture-evaluation-20260616/workspace/analysis/imports`
- Runtime dir: `<research-root>/example-web-capture-evaluation-20260616/.runtime`
