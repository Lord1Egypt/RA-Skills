---
name: write-better-tests
description: Use when Codex is adding, editing, selecting, reviewing, or explaining tests in any repository, including mocks, fixtures, snapshots, CI validation, regression coverage, TDD/red-green proof, or readiness claims. Enforces behavior-first test design so tests catch real regressions instead of merely passing the current implementation.
---

# Write Better Tests

Use this skill whenever test quality matters. The goal is not "more tests"; the goal is tests a skeptical maintainer would trust.

## Core Rule

Before saying coverage is good, prove the test would fail for the old or broken behavior when practical. A passing test without a credible failure mode is weak evidence.

Accept a test only if it satisfies all three:

1. It asserts the user-visible, API-visible, CLI-visible, data-contract, security, persistence, or regression behavior the change is actually about.
2. It would fail if the implementation regressed in the specific way the change claims to fix or protect.
3. It does not mock, snapshot, fixture, or helper-share away the behavior under test.

If a meaningful test is not practical, say that directly and use a different proof path. Do not add decorative coverage.

## Workflow

1. Reconstruct the behavioral thesis from source, issue, failing path, docs, logs, user report, or maintainer context: "When X happens, current code does Y; this change should make Z happen."
2. Identify the contract boundary: public API, UI state, CLI output, database effect, filesystem effect, package command, config behavior, security boundary, migration, background job, or pure function.
3. Pick the lowest test layer that still exercises the real contract. Prefer an existing local pattern over a new harness.
4. Write or revise the test around the contract, not around the implementation shape.
5. Produce red-green proof when practical:
   - run the new test before the fix;
   - temporarily revert the implementation hunk and run the test;
   - check out the parent/base version and run the test there;
   - or inject the old bug locally and confirm the test fails.
6. Remove any temporary mutation or revert, then run the focused command again.
7. Run proportional broader validation only after the focused test proves the contract.
8. Re-read the test diff with the anti-pattern checklist in `references/test-smells.md` before calling the change ready.

Never keep a temporary mutation, broad debug fixture, or local-only proof artifact in the final diff.

## What Good Looks Like

Prefer tests that:

- start from realistic inputs or repo fixtures rather than expected-output literals shaped by the implementation;
- assert exact behavior where exactness matters and semantic behavior where formatting is incidental;
- include the negative, empty, duplicate, unauthorized, stale, boundary, overflow, or race-adjacent case that caused the bug;
- exercise real parsers, routing, filtering, serialization, persistence, CLI wiring, or rendering behavior unless the unit boundary is explicitly the contract;
- fail with a useful message when the contract breaks;
- follow nearby test style, helpers, naming, and setup.

## Reject These Tests

Reject or rewrite tests that:

- only prove the new code path returns the value the test hard-coded from the patch;
- mock the function, module, query, parser, or service whose behavior is the subject;
- assert "called with" on an internal helper while the observable behavior could still be wrong;
- use snapshots for behavior that should be asserted intentionally;
- use `toBeTruthy`, `not.toThrow`, or "renders something" as the main proof for a concrete regression;
- generate expected values with the same helper or normalization logic as the implementation;
- add broad fixture churn, unrelated cleanup, or public docs changes just to make the test look substantial;
- pass only because the mock omits the old failure case.

Read `references/test-smells.md` when a test feels plausible but maybe too convenient.

## Repo-Specific Notes

For OpenClaw repositories, use this skill alongside `openclaw-contributions`.

For ClawHub Convex work, respect `convex/_generated/ai/guidelines.md`; avoid unindexed scans and tests that bless expensive exact-count behavior when the product should use bounded `limit + 1` or `hasMore` contracts.

For `openclaw/openclaw` CLI, config, session, auth, filesystem, or sandbox work, isolate state with temp directories and test homes. Never run tests against Vyctor's real `~/.openclaw` instance unless he explicitly asks for that exact path.

## Reporting

In the final work summary, include:

- the behavioral thesis covered by the test;
- the focused command that passed;
- the red-green proof used, or the reason it was not practical;
- any broader validation run.

For public PR bodies, mention only repository-native commands and behavior. Do not mention this skill, Codex-local checks, local paths, or temporary mutation details.
