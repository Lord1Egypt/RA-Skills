---
name: triage
description: "Triage failing Shiplight YAML tests: reproduce failures, inspect evidence, apply minimal correct fixes, report app/spec mismatches, and update project memory."
---

# Triage Failing Tests

Use this skill to reproduce, diagnose, and repair failing Shiplight YAML tests. If the application is broken or current behavior conflicts with the spec, report the mismatch instead of rewriting the test around it.

## When To Use

Use `/triage` when:

- A Shiplight test run is failing
- A deployment or UI change broke existing tests
- Several tests may share the same failure source
- CI needs a best-effort repair/report pass

Skip `/triage` when:

- Creating new tests from scratch; use `/create-tests`
- Verifying UI code changes without failing tests; use `/verify`
- Tests pass and the task is only quality improvement
- The product is being intentionally redesigned and tests need planned rewriting

## Required Context

Before editing YAML:

1. Read the `create-tests` reference guides `project-layout.md`, `updating-tests.md`, `test-implementation-guide.md`, and `knowledge.md`.
2. Read relevant `knowledge/` notes for the failing area, environment, auth, data, and tooling.
3. Read the matching spec under `specs/tests/`, if one exists.
4. Read `shiplight://yaml-test-spec` and `shiplight://schemas/action-entity`.

## Ground Truth

When sources disagree, this precedence applies:

1. Explicit user instruction
2. Feature or journey spec in `specs/tests/`
3. Existing YAML test `goal`, step `intent`, and `VERIFY` assertions
4. Current app behavior
5. Project context in `specs/context.md` and `knowledge/`
6. Agent docs
7. Agent inference

If current app behavior conflicts with a spec or test goal, report the mismatch. Do not silently rewrite intent to match current behavior.

## Workflow

1. **Reproduce** — run the specified target, or the narrowest relevant suite if no target was provided. If a failure looks transient, rerun the smallest affected target once before editing.
2. **Understand** — read the failure output, relevant YAML, matching spec, related tests, and shared templates/functions/hooks before opening a browser or changing files.
3. **Inspect when needed** — when logs and files are not enough, inspect the live app in a browser. Use the evidence needed for the failure: DOM, actions, locators, console logs, network logs, screenshots, or recordings.
4. **Fix minimally** — change the smallest correct surface: YAML, template, helper function, auth setup, environment data, or spec. Do not touch passing tests unless they share the same broken source.
5. **Validate and rerun** — validate edited YAML with `validate_yaml_test`, then rerun the narrowest changed target. After batch fixes, rerun the original target once.
6. **Reflect** — update specs, `specs/context.md`, or `knowledge/` when the session produced durable learning or corrected stale assumptions.

## Guardrails

- Do not guess rendered UI when the failure depends on current browser behavior.
- Do not delete assertions, skip required steps, or reduce coverage only to make a test pass.
- If intended product behavior changed, update the matching spec before updating YAML.
- If the app is broken, report the app issue instead of masking it with test changes.
- Preserve user changes and unrelated work.
- Prefer focused fixes over broad rewrites.
- Keep ACTION locators and VERIFY `js:` caches current when editing affected steps, but do not churn unrelated caches.
- In CI or non-interactive mode, do not block on user input. Make conservative best-effort decisions and document uncertainty.

Common causes include stale locators, changed user flows, assertion drift, expired auth, timing, shared templates/hooks, invalid parameter data, environment issues, and real app bugs. Use evidence to decide the minimal correct fix.

## Reporting

After triage, report:

- Target command(s) run and pass/fail result
- Files changed
- Tests repaired, skipped, still failing, or already passing
- Behavior covered or restored
- App/spec mismatches or unresolved blockers
- Knowledge, context, or specs updated
