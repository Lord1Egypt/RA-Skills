---
name: unit-test-coverage-helper
description: >-
  Add meaningful unit tests to existing codebases by finding uncovered behavior, selecting high-value cases, and validating coverage without brittle test inflation. Use when a user asks for unit tests, coverage, regression, pytest, jest, or needs practical workflow, code, checklist, documentation, or review support for this job.
---

# Unit Test Coverage Helper

## Purpose

Use this skill when a project needs better unit coverage, regression tests for a bug, characterization tests before refactoring, or a coverage plan that prioritizes behavior over vanity percentages.

Audience: software maintainers, QA engineers, open-source contributors, and product teams that need regression confidence from practical tests.

Read `references/requirement-plan.md` when demand evidence, source links, scoring rationale, or review criteria are needed.

## Workflow

1. Inspect the language, framework, test runner, coverage command, existing test style, and code paths or bug reports that motivated the request.
2. Identify high-value cases: pure functions, boundaries, errors, serialization, permissions, state transitions, and previously broken behavior.
3. Write tests in the repository's existing style with realistic fixtures and minimal mocking.
4. Add regression cases before broad coverage cases when a specific bug or incident exists.
5. Run the focused test command first, then the broader suite or coverage command when cost is acceptable.
6. Report coverage movement, uncovered risk, and any production changes needed to make testing clean.

## Expected Outputs

- A prioritized test plan for uncovered or risky paths.
- Concrete unit test files or patches that follow local conventions.
- Focused and broad verification commands.
- A short explanation of remaining coverage gaps and why they matter.

## Validation

- Tests assert behavior, edge cases, and regressions instead of implementation trivia.
- The requested test runner or equivalent focused command passes locally.
- Mocks and fixtures are small, readable, and consistent with the codebase.
- Coverage improvement is described honestly, including areas left untested.

## Triggers

Keywords: `unit tests`, `coverage`, `regression`, `pytest`, `jest`, `test plan`, `quality`

Example trigger sentences:

- `Use $unit-test-coverage-helper to add regression tests for this bug fix.`
- `Find the highest-value unit tests to raise coverage in this module.`
- `Create a coverage plan before refactoring this service.`
