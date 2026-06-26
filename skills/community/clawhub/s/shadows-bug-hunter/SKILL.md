---
name: bug-hunter
description: "Structured debugging with 4 techniques — Log Injection, Screenshot Analysis, Manual Trace, Test-Driven Fix. Use when facing errors, broken UI, regressions, or runtime issues."
metadata: { "openclaw": { "emoji": "🐛", "homepage": "https://clawhub.ai/NakedoShadow", "requires": { "bins": ["git"] }, "os": ["darwin", "linux", "win32"] } }
---

# Bug Hunter — Structured Debugging Protocol

**Version**: 1.1.0 | **Author**: Shadows Company | **License**: MIT

---

## WHEN TO TRIGGER

- Runtime errors, exceptions, stack traces
- UI rendering issues or visual bugs
- Regression after recent changes
- User says "debug", "fix this bug", "it's broken", "not working"
- Test failures with unclear root cause
- Performance degradation

## WHEN NOT TO TRIGGER

- Feature requests (use brainstorming skill)
- Code style / formatting issues
- Simple typos with obvious fix

---

## PREREQUISITES

**Required**:
- `git` — Used in Triage step to inspect recent changes via `git log --oneline -10`. Detection: `which git` or `git --version`.

**Optional** (auto-detected per project):
- `pytest` — Python test runner, used in Technique 4. Detected via `python -m pytest --version` or presence of `pytest.ini` / `pyproject.toml [tool.pytest]`.
- `jest` — JavaScript test runner, used in Technique 4. Detected via `npx jest --version` or presence of `jest.config.*`.
- `vitest` — Vite-based test runner, used in Technique 4. Detected via `npx vitest --version` or presence of `vitest.config.*`.

If no test runner is detected, Technique 4 (Test-Driven Fix) is limited to writing the test file — execution must be deferred.

---

## PROTOCOL — 4 TECHNIQUES

Before choosing a technique, run **Triage** first:

### Triage (MANDATORY — 60 seconds max)

1. **Read the error message** completely — what does it actually say?
2. **When did it start?** Check recent git changes: `git log --oneline -10`
3. **Is it reproducible?** Try the failing action once
4. **Classify severity**: Crash / Wrong result / Visual / Performance

Based on triage, select the most appropriate technique:

---

### Technique 1 — LOG INJECTION (Best for: backend, data flow, async issues)

1. Add strategic `console.log` / `print()` at key decision points
2. Log inputs AND outputs of suspected functions
3. Run the failing scenario
4. Read logs to identify where expected != actual
5. Fix the root cause
6. **CLEANUP**: Remove ALL debug logs before committing

```
[LOG] function_name() called with: {params}
[LOG] function_name() returned: {result}
[LOG] condition_check: variable = {value}
```

> **WARNING**: This technique temporarily modifies source files. All injected debug code MUST be removed before any commit. See CLEANUP GUARANTEE below.

### Technique 2 — SCREENSHOT ANALYSIS (Best for: UI bugs, layout issues)

1. Capture or describe the current (broken) state
2. Identify what SHOULD be displayed vs what IS displayed
3. Inspect the component tree top-down
4. Check: CSS specificity, z-index, overflow, flexbox/grid alignment
5. Fix the styling or rendering logic
6. Verify at breakpoints: 375px, 768px, 1024px, 1440px

### Technique 3 — MANUAL TRACE (Best for: logic errors, algorithm bugs)

1. Read the failing function line by line
2. Manually compute expected values at each step
3. Identify the exact line where expectation diverges from reality
4. Check edge cases: null, undefined, empty array, zero, negative
5. Fix the logic and add a test for the edge case

### Technique 4 — TEST-DRIVEN FIX (Best for: regressions, complex interactions)

1. Write a failing test that reproduces the bug FIRST
2. Run the test to confirm it fails: `python -m pytest {test_file} -x -q` or `npx jest {test_file}` or `npx vitest run {test_file}`
3. Fix the code until the test passes (green)
4. Run the full test suite to check for regressions: `python -m pytest -x -q` or `npx jest` or `npx vitest run`
5. Refactor if needed (refactor)

> **NOTE**: Technique 4 executes the project's test suite, which runs repository code. Only use on trusted repositories or within a sandboxed environment.

---

## PROCESS

```
TRIAGE → SELECT TECHNIQUE → INVESTIGATE → HYPOTHESIZE → FIX → VERIFY → CLEANUP
```

### Verification Checklist (after fix)

- [ ] The original bug is fixed
- [ ] No new errors introduced
- [ ] Existing tests still pass
- [ ] Debug artifacts removed (logs, console.log, print, TODO)
- [ ] Edge cases covered

### CLEANUP GUARANTEE

After every fix, the agent MUST perform a final verification pass:

1. Search modified files for debug markers: `grep -n "\\[LOG\\]\|console\\.log\|print(\|debugger\|# DEBUG\|// DEBUG" {modified_files}`
2. Remove any remaining debug artifacts
3. Confirm the working tree is clean of injected debug code before reporting completion

This step is non-negotiable and applies to all techniques, not just Technique 1.

---

## RULES

1. **Read before guessing** — always read the actual error, never assume
2. **One fix at a time** — change ONE thing, test, repeat
3. **Root cause, not symptoms** — fix WHY it broke, not just the surface
4. **No shotgun debugging** — don't change random things hoping it works
5. **Clean up** — remove ALL debug code before committing
6. **Regression test** — add a test to prevent the same bug from returning

---

## SECURITY CONSIDERATIONS

- **Commands executed**: `git log` (read-only). Technique 4 runs project test suites (`pytest`, `jest`, `vitest`) which execute repository code.
- **Data read**: Source files in the local repository.
- **File modification**: Technique 1 (Log Injection) temporarily modifies source files to inject debug statements. All injected code MUST be removed before commit (see CLEANUP GUARANTEE).
- **Network access**: None.
- **Persistence**: None.
- **Credentials**: None required.
- **Sandboxing**: Recommended when using Technique 4 on untrusted repositories, as test execution runs arbitrary project code.

---

## OUTPUT FORMAT

```markdown
## Bug Report
- **Error**: [exact error message]
- **Severity**: [Crash/Wrong Result/Visual/Performance]
- **Reproducible**: [Yes/No + steps]

## Root Cause
[Explanation of why the bug occurs]

## Fix Applied
[Description of the fix with file:line references]

## Verification
- [x] Original bug resolved
- [x] Tests pass
- [x] No debug artifacts remain
```

---

**Published by Shadows Company — "We work in the shadows to serve the Light."**
