# Unit Test Coverage Helper

## What It Does

Add meaningful unit tests to existing codebases by finding uncovered behavior, selecting high-value cases, and validating coverage without brittle test inflation.

This package was generated from demand signals in run `20260623-040526` and then rewritten for publication with domain-specific workflow guidance instead of generic task scaffolding.

## Best For

Software maintainers, qa engineers, open-source contributors, and product teams that need regression confidence from practical tests.

## Workflow Summary

1. Inspect the language, framework, test runner, coverage command, existing test style, and code paths or bug reports that motivated the request.
2. Identify high-value cases: pure functions, boundaries, errors, serialization, permissions, state transitions, and previously broken behavior.
3. Write tests in the repository's existing style with realistic fixtures and minimal mocking.
4. Add regression cases before broad coverage cases when a specific bug or incident exists.
5. Run the focused test command first, then the broader suite or coverage command when cost is acceptable.
6. Report coverage movement, uncovered risk, and any production changes needed to make testing clean.

## Deliverables

- A prioritized test plan for uncovered or risky paths.
- Concrete unit test files or patches that follow local conventions.
- Focused and broad verification commands.
- A short explanation of remaining coverage gaps and why they matter.

## Quality Bar

- Tests assert behavior, edge cases, and regressions instead of implementation trivia.
- The requested test runner or equivalent focused command passes locally.
- Mocks and fixtures are small, readable, and consistent with the codebase.
- Coverage improvement is described honestly, including areas left untested.

## Trigger Examples

- `Use $unit-test-coverage-helper to add regression tests for this bug fix.`
- `Find the highest-value unit tests to raise coverage in this module.`
- `Create a coverage plan before refactoring this service.`

## Files

- `SKILL.md`: English skill instructions.
- `SKILL.zh-CN.md`: Chinese skill instructions.
- `README.md`: English user-facing guide.
- `README.zh-CN.md`: Chinese user-facing guide.
- `references/requirement-plan.md`: Demand evidence and scoring details.
- `agents/openai.yaml`: Default invocation metadata.
