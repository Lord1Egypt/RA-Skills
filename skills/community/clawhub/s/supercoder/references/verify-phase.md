# Phase 6: Verify

Confirm that the implementation works and meets the acceptance criteria. This is the final quality gate.

## What to Communicate

Present a delivery summary covering:

- **Test results** — suite ran or not available, all pass or N failures, any pre-existing failures
- **Acceptance criteria** — each criterion marked pass or fail, with the specific code that satisfies it (file and line)
- **Edge case coverage** — error handling, boundary conditions, security, performance
- **Known limitations** — what's not covered and why
- **Reviewer notes** — areas that need careful human review

## Context to Preserve

Before finishing, make sure the conversation retains: the final test results summary, how many acceptance criteria passed vs failed, any known limitations, and the key files in the implementation.

## Steps

1. TaskUpdate — set Phase 6 to `in_progress`.
2. Run the full test suite with Bash.
   - Related failures: fix and re-run (failing tests first, then full suite).
   - Pre-existing failures: note them and proceed. Do not fix unrelated failures.
   - No test suite: note this explicitly and recommend test coverage as follow-up.
3. Verify each acceptance criterion. For each, check if it's met, identify the specific code (file + line), and mark pass or fail.
   - Minor failure: fix directly, re-verify.
   - Major failure: roll back to Implement or Design.
4. Edge case scan:
   - Error handling — invalid input, network/API failures
   - Boundary conditions — empty inputs, maximum size, null/undefined, concurrent access
   - Security — input validation, auth checks, injection risks, sensitive data
   - Performance — N+1 queries, unnecessary loops, memory leaks, large payloads
5. Present the delivery summary.
6. Ask the user for final confirmation via AskUserQuestion.
7. TaskUpdate — set Phase 6 to `completed`.

## Issue Severity

| Severity | Examples | Response |
|----------|---------|----------|
| Minor | Typos, missing edge case | Fix directly, re-verify |
| Moderate | Incomplete error handling | New increment, implement, re-verify |
| Major | Core functionality broken | Roll back to Implement or Design |

## Rollback

For major issues: report with specific details, set Phase 5 (or Phase 4) back to `pending`, and re-enter with prior findings.

## Done

After the user confirms delivery, all six tasks should be in `completed` status and the workflow is finished.
