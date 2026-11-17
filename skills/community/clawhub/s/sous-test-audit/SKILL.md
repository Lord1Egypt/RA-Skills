---
name: test-audit
description: Decide whether a test earns its place. Use before writing a new test, when reviewing a diff that adds or deletes tests, when a suite is slow or flaky, or when asked to "clean up tests". Gates new tests on the behavior they prove, flags junk patterns, and requires evidence before any test is deleted.
metadata:
  openclaw:
    homepage: https://github.com/OrenSegal/sous
---

# test-audit

A green suite only means something if every test in it could have failed.
This skill does three things: gates new tests, finds junk in existing ones, and
makes deletions prove they lose nothing.

It is the counterweight to test-first skills (`tdd`): those push tests in, this
one asks whether each test pays rent.

## 1. Authoring gate (before writing any test)

Answer all four in one line each, in the reply or the PR body. If an answer is
"nothing" or "not sure", don't write the test yet.

1. **Behavior**: what visible behavior does it prove? Name the output, state
   change, or error a caller could observe. "Calls X" is not behavior.
2. **Regression**: what specific bug would turn it red? Name the edit to
   production code that breaks it. If no plausible edit breaks it, it proves nothing.
3. **Gap**: which existing test does NOT already cover this? Search first
   (`rg` for the function / type under test in the test tree).
4. **Seam cost**: does it need a test-only hook in production code (a flag, an
   init param, a `#if DEBUG` branch)? If so, is that seam used by anything else,
   or does it exist only for this test?

## 2. Junk patterns (scan existing tests)

Flag each hit with `file:line` and the pattern number. Report, don't auto-fix.

| # | Pattern | Why it's junk |
|---|---------|---------------|
| 1 | No assertion at all | Passes whenever it doesn't crash |
| 2 | Asserts a constant: `expect(true)`, `XCTAssertTrue(true)`, `assert 1 == 1` | Can't fail |
| 3 | Compares a value to itself, or to the literal it was just built from | Tautology |
| 4 | Only asserts a mock was called (`verify(mock).called`) with no output check | Proves wiring, not behavior; breaks on every refactor |
| 5 | Snapshot of an entire object/response with no reviewer-readable intent | Rubber-stamped on every update |
| 6 | Same fixture copy-pasted across files | Drifts; one gets fixed, the rest lie |
| 7 | Asserts on log text or error message wording | Breaks on copy edits, misses behavior |
| 8 | Sleeps for timing (`sleep`, `Task.sleep`, `setTimeout`) instead of awaiting a signal | Flaky and slow |
| 9 | Swallowed failure: `try?` / bare `except:` / `.catch(() => {})` around the thing under test | Failure path becomes a pass |
| 10 | Test double with a single continuation / callback slot | Second caller orphans the first; suite hangs instead of failing |
| 11 | Test filter or suite name that matches zero tests, lane still green | Zero executed reads as success |
| 12 | Asserts on private/internal state reached via reflection or test-only accessors | Couples to implementation |
| 13 | Retries or `@flaky` markers hiding a real race | Converts a bug into noise |
| 14 | Order-dependent tests (shared mutable global, relies on a previous test) | Pass alone, fail in parallel, or vice versa |
| 15 | Duplicate of another test with a different name | Double maintenance, zero extra proof |
| 16 | Reads real host state (clock, locale, thermal/power mode, network) without injection | Non-hermetic; differs between laptop and CI |

## 3. Deletion evidence (before removing a test)

Record, per test, in the PR body:

- **Where**: `file:line` and full test id.
- **Catches**: the regression it would catch (from gate question 2), or "none: pattern #N".
- **Callers**: the production symbols it exercises, and their non-test callers (`rg`).
- **Covered by**: the other test that proves the same behavior, with `file:line`,
  or "not covered, deleting anyway because ..." with the reason.

No evidence line, no deletion.

## 4. Validation (prove the run executed)

A lane that prints "succeeded" after running zero tests is the most common
false green. After any add/delete, run the narrowest suite and read the
**executed count**, not the status line:

- Swift (Xcode): `xcodebuild test -only-testing:<Target>/<Suite>` then check
  `Executed N tests` (XCTest) or `Test run with N tests` (Swift Testing) is > 0
  and matches what you expect. `@Suite` names that don't match `-only-testing`
  run nothing and still pass.
- Swift (SPM): `swift test --filter <Suite>` and check the same counts.
- pytest: `pytest path::Test -q` and check `N passed`; `-p no:randomly` off.
- Vitest/Jest: `vitest run <file>` and check `Tests  N passed`.

Projects with a wrapper (e.g. `make test SUITE=<Suite>`) should use it
and still check the count: set it in the project's CLAUDE.md so this step
points at the real command.

sous ships the same check as a script, for CI and for wrappers:

```bash
<test command> 2>&1 | tee test.log
~/.sous/bin/tests-ran test.log           # exit 1 if zero tests executed
~/.sous/bin/tests-ran --min 40 test.log  # or below a floor you set
```

It reads the five formats above and counts skipped tests as not executed.

To check a diff for the other way tests go quiet, deletion, skips and fewer assertions:

```bash
~/.sous/bin/tests-weakened origin/main   # exit 1 lists each finding
```

## Output

```
test-audit: <scope>
gate:      <n> new tests, <k> pass all four questions, <n-k> held back (why)
junk:      <file:line> #<pattern> <one-line note>
deletions: <test id> -> covered by <file:line> | pattern #N
executed:  <suite> ran <N> tests (expected <M>)
```
