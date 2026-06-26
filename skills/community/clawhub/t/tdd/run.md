# Test Run (Test Execution and Result Reporting)

Procedure for running tests and analyzing/reporting results.

## When to Use

- When test execution is needed after code changes
- Test verification before submitting a PR
- Use when "run tests", "test run", "execute tests", "verify" is mentioned

## Step 1: Environment Detection

Identify the project's test stack and configuration.

```bash
# Detect test framework
ls package.json pyproject.toml Cargo.toml go.mod 2>/dev/null

# Check test commands
grep -E '"test"|"test:"|"vitest"|"jest"|"playwright"' package.json 2>/dev/null
```

Items to check:
- Test framework (vitest, jest, pytest, go test, etc.)
- Test execution command (`pnpm test`, `npm test`, `pytest`, etc.)
- Test commands run in CI (check `.github/workflows/`)
- Required external services (DB, SSO, Redis, etc.)

## Step 2: Impact Scope Analysis

Determine which tests are affected by the changed code.

```bash
git diff --name-only HEAD
```

| Change Type | Test Scope |
|----------|-----------|
| Single function modification | Only unit tests for that function |
| Module/class change | Tests for that module + dependent modules |
| API endpoint change | Unit + integration + e2e tests |
| Schema/type change | All tests |

## Step 3: Test Execution

**Order: unit → integration → e2e (fastest first)**

```bash
# 1. Type check (if available)
pnpm typecheck  # or tsc --noEmit

# 2. Run only related tests (fast feedback)
pnpm test -- --filter "auth"  # or vitest run src/utils/auth.test.ts

# 3. Full test suite (after related tests pass)
pnpm test
```

**Execution principles:**
- Run related tests first for fast feedback
- Run full test suite after related tests pass
- Stop immediately on failure and analyze the cause

## Step 4: Result Analysis and Reporting

### All Passed

```
Test result: All passed
- Unit tests: 42/42 passed
- Integration tests: 8/8 passed
- Type check: No errors
```

### Failed

```
Test result: Failed
- Failed test: src/utils/auth.test.ts > validateToken > should reject expired
- Error: Expected false, received true
- Root cause: Missing expiration time comparison logic in validateToken
- Fix proposal: [specific fix details]
```

**Actions on failure:**
1. Analyze error message
2. Determine if the failure is caused by **the changed code** or a **pre-existing defect**
3. If caused by the changed code, fix immediately
4. If a pre-existing defect, report to user (outside fix scope)

## Application Criteria by Task Complexity

| Task Complexity | Scope |
|------------|----------|
| trivial (1-2 line change) | Run related tests only |
| moderate (3-10 files) | Related tests + full test suite |
| complex (10+ files, schema change) | Type check + full test suite + e2e |

## Prohibited Actions

- Claiming "tests passed" without actually running them
- Bypassing failed tests with skip/disable
- Reporting completion with only related tests without full suite (moderate and above)
- Reporting "tests failed" without analyzing the failure cause

## Pre-Commit Test Execution (MANDATORY)

After code changes, related tests MUST run before commit. "It would fail anyway" is not a valid reason to skip — even when external deps (API, DB) cause failures, run the tests to record the current state.

> Exception: when tests literally cannot run in any local environment (CI-only execution surface), see `cycle.md` "`[CI-VERIFY]` Red-only commit" — tag the commit and treat Green as incomplete until CI confirms.

| # | Don't | Do |
|---|-------|-----|
| 1 | Commit and report "done" without running tests | Check `package.json` scripts (or repo's runner) → execute → report results before commit |
| 2 | Skip tests because "they will fail due to external deps" | Run regardless — failure state is information. Note external-dep failure cause in the report |
| 3 | Sequence: change → commit → (later: tests) | Sequence: **change → verify → commit**. Reporting "test passed" after commit when tests were not run is procedure violation |

The principle: every commit ships a measured state — passing or failing. Untested commits ship an unknown state.

## CI Failure Triage (CRITICAL)

Recommendation priority when a test fails in CI:

| Priority | Action | When |
|----------|--------|------|
| 1st | **Fix the test code** | Test assertion/pattern does not match actual behavior |
| 2nd | **Add environment branching** | Behavior differs by environment — CI vs local, OS differences (`process.env`, `test.runIf`, conditional URL patterns, etc.) |
| 3rd | **Fix the app code** | The app logic itself has a bug, so the test fails legitimately |
| 4th | **Investigate infrastructure** | An external service (DB, SSO, API server) is unhealthy |

### `test.skip` / `test.fixme` recommendation limits (CRITICAL)

**Do not recommend `test.skip` except for environment branching (`test.runIf`, `process.env`-based conditional execution).**

- ❌ "Flaky due to infra — let's skip" — fix the infra, or make the test detect the environment and branch
- ❌ "Unrelated to this PR — let's skip" — if it is unrelated, there is no reason to skip either. Pre-existing test issues are fixed separately
- ✅ "CI runner cannot reach the staging cluster" → branch with `test.runIf(process.env.TEST_AUTHENTIK_URL)`
- ✅ "Test only runs on macOS" → branch with `test.runIf(process.platform === 'darwin')`
