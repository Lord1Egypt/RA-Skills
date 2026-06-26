# Repository Audit Pack

Use this pack only for whole-repository audits.

## Table of Contents

- [Goal](#goal)
- [Audit Phases](#audit-phases)
- [Output Model](#output-model)
- [Noise Control](#noise-control)
- [Evidence Rules](#evidence-rules)
- [Source Notes](#source-notes)


## Goal

Assess the repository as it exists now, not just a diff.

Repository audit is different from PR review:

- broader scope
- less line-by-line granularity
- stronger need for prioritization and deduplication
- explicit separation between findings and coverage gaps

## Audit Phases

### 1. Inventory

Start with repository shape:

- root manifests and lockfiles
- CI workflows
- environment examples
- docs that define architecture or operational rules
- top-level app and service entry points
- test directories and quality gates

### 2. Stack detection

Map the repository by stack and runtime:

- frontend UI
- backend API
- jobs and workers
- database and migrations
- infra and CI

Load only the relevant language packs after the inventory step.

### 3. Hotspot selection

Prioritize the highest-risk areas:

- auth and authorization
- input validation and deserialization
- external network calls
- database writes and migrations
- secret loading and logging
- filesystem access
- shell or process execution
- background jobs and shutdown
- concurrency and shared mutable state
- isolated dead code and abandoned subsystems

### 4. Focused inspection

Inspect representative modules deeply before scanning wider:

- auth middleware, guards, or server actions
- route handlers and controllers
- repositories and query builders
- worker loops and retry code
- startup/bootstrap/config paths
- CI and release workflows
- modules and exports with unclear incoming references

### 4a. Dead-code inspection

Explicitly inspect for isolated dead code:

- files with no importers or route registrations
- handlers, jobs, commands, or workers no longer reachable from any entry point
- feature-flag branches that are permanently off or superseded
- fallback code that current config or control flow can no longer reach
- exports retained after refactors with no remaining callers

Be careful around:

- dynamic imports and lazy-loading conventions
- reflection, registration, or plugin discovery
- framework file-system routing
- generated files
- build tags or conditional compilation
- values whose only effect happens on drop or module initialization

### 5. Deduplication

Group repeated symptoms into one root-cause finding.

Bad:

- "10 handlers lack input validation" as 10 separate issues

Good:

- "Request validation is missing on the public write-path layer, affecting 10 handlers"
- "The legacy webhook subsystem is orphaned: routes are no longer registered, but handlers, secrets, and retry code remain in the tree"

## Output Model

Use repository audit output, not PR output.

### Priority Bands

| Priority | Meaning |
|---|---|
| P0 | Immediate security or data-loss issue |
| P1 | High-likelihood correctness or production stability issue |
| P2 | Structural risk or maintainability problem with operational consequences |
| P3 | Lower-priority follow-up item |

### Required Sections

- `Repository Audit Summary`
- `P0`
- `P1`
- `P2`
- `P3` if needed
- `Dead Code Findings` when applicable
- `Dead Code Removal Candidates` when applicable
- `Needs Runtime Verification` when applicable
- `Coverage Gaps`
- `Recommended Next Actions`

## Noise Control

Do not report:

- cosmetic style issues
- low-confidence guesses
- every single instance of the same root cause
- items already fully enforced by mandatory tooling

Do report:

- systemic validation gaps
- repeated unsafe patterns that indicate a real boundary failure
- CI or test blind spots that leave critical paths unverified
- architecture issues with direct security, correctness, or reliability impact
- isolated dead code that hides obsolete behavior, stale permissions, or abandoned integrations

## Evidence Rules

- Tie each finding to concrete files or repository areas.
- Say when a point is sampled evidence versus exhaustively verified.
- If a suspicion is not yet proven, put it under `Coverage Gaps` or `Next Actions`, not under `P0`-`P2`.
- For dead code, explain why it appears unreachable or unreferenced and note any dynamic-dispatch caveat.

### Dead-code section rules

- `Dead Code Findings`: use only when the code is strongly evidenced as unreachable or orphaned.
- `Dead Code Removal Candidates`: use for likely removable code that still deserves a quick local verification before deletion.
- `Needs Runtime Verification`: use when dynamic registration, build matrix, or deployment-only wiring means static inspection is insufficient.

## Source Notes

These repository-audit rules are aligned with:

- Google Engineering Practices: https://google.github.io/eng-practices/review/reviewer/looking-for.html
- OWASP Code Review Guide: https://owasp.org/www-project-code-review-guide/
- OWASP ASVS Project: https://owasp.org/www-project-application-security-verification-standard/
