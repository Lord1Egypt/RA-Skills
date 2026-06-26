---
name: taku-review
description: Use after implementation is complete. Triggers after /taku-build. Analyzes diffs for security issues, bugs, and code quality. Run when asked to "review this", "check my diff", "code review", "审查代码", "看看有什么问题", "检查一下", "准备合并", "代码质量", or before shipping. Proactively invoke when the user is about to merge or land code changes.
allowed-tools:
  - Bash
  - Read
  - Edit
  - Write
  - Grep
  - Glob
---

# Taku Review - Delivery Gate

Review decides whether the change can ship. It is not a long critique and it is
not a nit collector.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

[IRON LAW] Hard stops come before concerns. Do not bury a blocking delivery
failure under style comments.

## Review Contract

Read the current diff against the base branch or, when there is no remote diff,
the local dirty diff. Then output exactly three sections:

```text
HARD STOPS
- [none | blocking finding list]

CONCERNS
- [none | non-blocking risks worth fixing or noting]

SUMMARY
- Changed files: [...]
- Verification evidence: [...]
- Scope/spec status: clean | drift | requirements missing | unknown
- Residual risk: none | [...]
- Status: DONE | BLOCKED | DONE_WITH_CONCERNS
```

Use `BLOCKED` whenever a hard stop exists. Use `DONE_WITH_CONCERNS` only when
remaining issues are non-blocking and explicitly listed.

## Step 1: Detect Base and Diff

Run the repo-appropriate equivalent of:

```bash
git remote get-url origin 2>/dev/null
git branch --show-current
git symbolic-ref refs/remotes/origin/HEAD 2>/dev/null | sed 's|refs/remotes/origin/||'
git status --short
git diff --stat
```

If on the base branch with no local diff, stop cleanly:

```text
HARD STOPS
- none

CONCERNS
- none

SUMMARY
- Changed files: []
- Verification evidence: not applicable; no diff
- Scope/spec status: clean
- Residual risk: none
- Status: DONE
```

Do not invent findings when no code changed.

## Step 2: Reconstruct Intent

Read the strongest available intent source:

- Build ledger from `/taku-build`
- `PLAN.md`
- approved Quick mini design
- `DESIGN.md`
- user request in the current session
- commit messages

Then compare intent to delivered changes.

Hard stops:

- **Scope drift:** unrelated files, behavior, or refactors not approved.
- **Missing requirement:** approved behavior absent from the diff.
- **Unapproved deviation:** Build recorded a deviation that was not approved.

Approved deviations are not hard stops, but must be listed in `SUMMARY`.

## Step 3: Check Verification Evidence

Review the observed evidence, not confidence statements.

Hard stops:

- The implementation claims completion but no test/build/lint/manual command
  evidence is visible.
- Verification output is stale or from before the relevant code changed.
- Required TDD anchor or reproduction check is missing.

If evidence is unavailable because the repo has no harness, say what was used
instead. Do not claim tests passed unless output or explicit user evidence shows
that.

## Step 4: Critical Pattern Pass

Read the full diff before commenting. Search for production-risk patterns:

- SQL/query injection from string-built user input
- Prompt injection or unvalidated LLM output crossing a trust boundary
- Missing auth checks or overly broad permissions
- Conditional side effects hidden in ternaries, short-circuits, or optional chaining
- Race conditions, shared mutable state, or non-atomic read/modify/write
- Resource leaks that can exhaust connections, files, streams, or listeners

High-confidence critical/security bugs are hard stops. Apply a fix directly
only when the correct change is clear from local context. Otherwise provide the
smallest safe recommendation and keep status `BLOCKED`.

## Step 5: Concern Pass

Only after hard stops are handled, list non-blocking risks:

- error paths that degrade behavior but do not block shipping
- weak type/null handling with bounded blast radius
- missing cleanup where impact is limited
- maintainability issues that make a follow-up risky

Skip nit floods. If a style pattern matters, mention it once.

## Auto-Fix Policy

- Auto-fix Critical and Important findings when the fix is clear and locally
  verifiable.
- After an auto-fix, run the smallest relevant verification.
- Do not commit, push, or open a PR.
- Do not mix review with broad refactoring.

## Output Rules

- `HARD STOPS` must appear first.
- Every hard stop needs a file/line or artifact reference when available.
- `SUMMARY` must include changed files, verification evidence, residual risk,
  and status.
- If Review finds scope drift, missing requirements, or missing verification,
  status is `BLOCKED` until fixed or explicitly approved by the user.

## Known Pitfalls

**Nit flood hides the real issue.** A review produced 40 style comments and one
SQL injection finding. The developer fixed the easy comments and missed the
security bug.

Prevention: hard stops first; concerns second; style notes only when they change
delivery risk.

**Review accepts a build summary as evidence.** The summary said "tests pass",
but no command output was visible.

Prevention: completion claims need observed command output, diff evidence, or
explicit user-provided evidence.

**Scope drift looks like cleanup.** A task approved `--json` output, but the diff
also rewrote command discovery.

Prevention: reconstruct intent before code-quality review. Good code outside
scope is still a delivery failure.
