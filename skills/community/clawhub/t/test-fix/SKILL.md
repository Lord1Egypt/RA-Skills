---
name: Test Fix
description: Fix failing tests without weakening them — run the suite once, rerun only the failing files to separate flaky from real failures, classify each real failure as source bug or wrong test, then propose minimal diffs for approval. Use when asked to fix failing tests or make the suite green.
---

# Test Fix (manual edition)

When the user asks to "fix the failing tests" or "make the tests pass", follow this
workflow. This edition has no scripts: you run the commands and apply the same judgment.

## Step 1 — Run the suite once

Detect the runner from `package.json`:

| Signal | Command |
| --- | --- |
| `vitest` in devDependencies or the test script | `npx vitest run` |
| `jest` in devDependencies or the test script | `npx jest` |
| `@playwright/test` in devDependencies | `npx playwright test` |
| none of the above | the project's own `npm test` |

Record the totals and every failing test (file + name + first line of the message).

- Green means zero failures AND exit code 0.
- A non-zero exit with no listed failures means the suite itself is broken (for example a
  test file fails to load). Report that; never call it green.

## Step 2 — Rerun only the failing files

Rerun each failing file once:

- vitest: `npx vitest run path/to/file.test.ts`
- jest: `npx jest --runTestsByPath path/to/file.test.ts`
- playwright: `npx playwright test path/to/file.spec.ts`

Classify each failure:

- **flaky** — failed, then passed on the rerun. Report only. Do not patch it, and do not
  add sleeps or retries to hide the race.
- **consistent** — failed both times. It needs a patch; go to step 3.

## Step 3 — Judge each consistent failure

Read the failure message, the test, and the source. Decide:

- **source bug** — the production code is wrong. Patch the source.
- **wrong test** — the assertion contradicts the intended behavior. Prove it first
  (doc comments, naming, sibling tests, specs). If you cannot prove the test is wrong,
  treat it as a source bug. Doubt goes to the code, not the axe.

## Step 4 — Propose patches (do not apply)

For each failure, write `patches/<n>.md` containing:

1. a unified diff of the smallest safe change
2. two lines of rationale: the cause, and why this is the minimal fix
3. risk: low / med / high

Then write `patches/README.md` with a table:
failure -> cause (source bug / wrong test) -> risk -> patch file.

## Step 5 — Report and wait

Lead with the verdict, for example:

> 3 failures: 1 source bug, 1 wrong test, 1 flaky — patches in `patches/`, nothing
> applied yet.

List flaky ones as report-only. Then ask for approval. Apply only after explicit
approval, one patch at a time, rerunning the affected test after each.

## Hard rules

- Never delete, skip, `.skip`, or weaken a test to make it pass.
- Never edit an assertion before proving the production code is right.
- Never apply a patch without explicit approval.
- Flaky means report only — no patch.
- Never silence a failure with sleeps or retries without explaining the real race.

---

This is the manual edition: the workflow and the hard rules, with nothing to install.
A paid edition with the same workflow plus two zero-dependency helper scripts (runner
detection, one run, rerun-and-classify) is listed on Agensi.
