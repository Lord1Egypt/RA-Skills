---
name: tdd-spec
license: MIT
description: "Test-driven development using the approved SPEC SDD as the source of truth. Reads `.specs/SPEC-{YYYYMMDD}-{feature}.md`, turns requirements and acceptance criteria into red-green-refactor vertical slices. Use when implementing a feature or bugfix after the SPEC is approved. User-facing questions and recommendations must be in Portuguese (pt-BR). Part of the afonsoft/skills collection."
metadata:
  version: "1.0.0"
  visibility: public
  author: afonsoft
  url: https://github.com/afonsoft/skills
---

# TDD from SPEC

Test-driven development guided by the approved SPEC SDD. The SPEC is the single source of truth. Every test is derived from a numbered requirement or acceptance criterion.

Internal reasoning and commands are in English. All questions and explanations to the user are in **Portuguese (pt-BR)**.

## When to Use

- A `.specs/SPEC-{YYYYMMDD}-{feature}.md` exists with `Status: Approved`.
- The user asks to implement a feature, change, or bugfix.
- Before writing implementation code.

## When NOT to Use

- Do not use when the SPEC is missing or still in `Draft`.
- Do not use when the user only wants a code review or fix without tests.
- Do not use when the SPEC explicitly declines a requirement (marked `[A DEFINIR]`).

## Core Principles

1. **The SPEC is the oracle.** Every test must map to a requirement or acceptance criterion.
2. **One vertical slice at a time.** One failing test, one passing test, one refactor.
3. **No speculative code.** Write only the minimum code to make the current test pass.
4. **No refactor in RED.** Refactor only when the suite is green.
5. **Re-validate after every change.** Run the full suite before moving to the next slice.

## Process

### 1. Read the SPEC

Load `.specs/SPEC-{YYYYMMDD}-{feature}.md` and identify:

- Section 4 — numbered requirements (`RF-001`, `RF-002`, ...).
- Section 6 — acceptance criteria in BDD `Given...when...then`.
- Section 7 — task plan and validation strategy.
- Section 3 — files to create or modify.

If the SPEC is not approved, stop and invoke `/grill-me-with-spec`.

### 2. Slice the work

Order the work by the task plan (Section 7). Each slice is one requirement or one acceptance criterion. Never write all tests upfront.

### 3. Red-Green-Refactor loop

For each slice:

```text
RED    → Write one test that exercises a public seam and fails.
GREEN  → Write the minimum code that passes the test.
REFACTOR → Clean duplication, improve names, respect SOLID while green.
```

### 4. Test at the public seam

Test behavior through public interfaces (API, function, component), not internal implementation. Tests must survive internal refactors. See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mock rules.

### 5. Mapping to the SPEC

For each test, include a comment or description pointing to the source requirement:

```python
# Covers RF-003: order total must include tax
# Covers AC-02: Given an empty cart, when checking out, then the system returns 422
```

### 6. Re-validate and report

After every slice:

1. Run the full test suite for the affected stack.
2. Run lint / type check.
3. Confirm the SPEC requirement is satisfied.

Report progress to the user in Portuguese:

```text
Slice concluido: [RF-XXX / AC-YYY]
- Teste: [PASS/FAIL]
- Build: [PASS/FAIL]
- Lint: [PASS/FAIL]

Proximo slice: [PROXIMO].

Posso continuar?
```

### 7. Closure

When all slices are green:

- Run the full suite (unit, integration, relevant E2E).
- Run the validation strategy from the SPEC (Section 7.1).
- Update `docs/qa/test-plan-<feature>.md` or equivalent if it exists.
- Invoke `/qa-analyst` for the mandatory pre-PR review.
- Do not open the PR until QA approves.

## Anti-Patterns

- ❌ Writing all tests before any implementation.
- ❌ Testing private methods or internal state.
- ❌ Mismatched expectations in mocks (see [mocking.md](mocking.md)).
- ❌ Refactoring while a test is red.
- ❌ Skipping the validation strategy from the SPEC.

## Common Mistakes

| Mistake | Fix |
| --- | --- |
| Implementing before the test | Write the failing test first. |
| The test does not map to the SPEC | Link every test to `RF-###` or `AC-###`. |
| Slice too large | Break the slice until one behavior is tested. |
| Not running the full suite after a green test | Re-validate before moving on. |

## References

- `grill-me-with-spec` — for producing the SPEC SDD
- `qa-analyst` — for the mandatory pre-PR review
- `diagnose` — when a test fails unexpectedly and the cause is unclear
- `tests.md` — test examples and patterns
- `mocking.md` — mocking rules
- `refactoring.md` — refactoring guidance
- `deep-modules.md` — deep module design
- `interface-design.md` — interface design patterns
