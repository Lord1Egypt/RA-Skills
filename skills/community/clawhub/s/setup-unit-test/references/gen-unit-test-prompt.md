# AI Unit Test Generation Rules

> This file is written to the project's .claude/commands/gen-unit-test.md by /setup-unit-test

## Input

Analyze the path specified by $ARGUMENTS. Supports the following modes:

- **Single file**: `/gen-unit-test src/utils/format.ts` → generate tests for that file
- **Directory**: `/gen-unit-test src/services/` → scan all source files in the directory and generate tests one by one
- **Full scan**: `/gen-unit-test src/` → scan the entire src directory and generate tests for files missing them
- **No arguments**: `/gen-unit-test` → equivalent to `/gen-unit-test src/`

## Workflow

1. Determine the input type (file / directory):
   - If a directory, recursively scan all `.ts` / `.tsx` / `.vue` files (excluding `.test.`, `.spec.`, `.stories.`, `index.ts`, etc.).
   - For each file, check whether a corresponding test file already exists under `tests/unit/`; skip if it does.
2. For each source file to generate tests for:
   a. Read the source code and extract all exported functions/classes/components.
   b. Analyze parameter types, return values, branch paths, and external dependencies.
   c. Determine the test type:
      - Pure function → Vitest unit test
      - React component → @testing-library/react component test
      - Vue component → @testing-library/vue component test
      - API call → MSW mock integration test
      - Custom Hook/Composable → renderHook test
   d. Generate the test file according to the specification, including:
      - Happy Path (at least 1)
      - Boundary values (at least 2)
      - Error paths (at least 1)
3. Run `vitest run <generated test file>` to verify.
4. If it fails, analyze the error and auto-repair (up to 3 rounds).
5. After all tests pass, output a generation summary: which files were generated, pass/fail counts.

## Framework Requirements

- Use Vitest (`import { describe, it, expect, vi } from 'vitest'`).
- Use @testing-library/react or @testing-library/vue for component tests (based on the project framework).
- Use MSW (Mock Service Worker) for API mocking.
- Follow the AAA pattern (Arrange-Act-Assert).

## Coverage Requirements

- Every exported function/component must cover:
  1. Happy Path (normal input → expected output).
  2. Boundary values (null, zero, extremely large/small values).
  3. Error paths (invalid input → expected error).
  4. Branch coverage (at least one test case per if/switch branch).

## Naming Conventions

- describe: Name of the function/component under test.
- it: "should [verb] [expected behavior] when [condition]".
- Example: `it('should return 0 when both arguments are 0')`.

## Mocking Conventions

- Prefer MSW to intercept network requests rather than directly mocking modules.
- Use `vi.fn()` only for callback function verification.
- Never mock the internal implementation of the module under test.

## File Conventions

- Test files are centralized in the `tests/unit/` directory, mirroring the source code structure by module.
- Unit tests: `src/utils/format.ts` → `tests/unit/utils/format.test.ts`.
- Component tests: `src/components/Button.tsx` → `tests/unit/components/Button.test.tsx`.

## Constraints

- Use Vitest, not Jest.
- Mock network requests with MSW; do not mock internal module functions.
- Test files are centralized in the `tests/unit/` directory, mirroring the `src/` structure.
- Use the component/function name for describe; use English to describe expected behavior in it (for easier maintenance).
