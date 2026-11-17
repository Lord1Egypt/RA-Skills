---
name: write-tests
description: Author tests that actually catch regressions — picks WHAT to test by risk (branch points, boundaries, error paths, money/auth/concurrency), proves every new test can fail (a test never seen red is decoration), mocks only boundaries you don't own, and pins untested legacy code with labeled characterization tests before anything else touches it. Use this skill whenever the user says "write tests", "add tests", "test this", "add coverage", "unit test this function", "increase coverage", "add a regression test", "characterization tests", "TDD this", or "/write-tests" — even if they don't explicitly say "test skill". Do not use for diagnosing a failing test (use diagnose) or reviewing existing tests as part of a diff (use code-review).
---

# Write Tests

Author tests whose only job is to fail when the behavior breaks. Everything else — coverage numbers, green checkmarks, test count — is a proxy, and every proxy here can be gamed by accident. This skill makes the non-gameable thing the deliverable: each test is proven capable of failing, targets a behavior chosen by risk, and asserts what the caller can observe.

## When to use this skill

- The user says "write tests", "add tests", "test this", "add coverage", "unit test this", "add a regression test", "TDD this", "characterization tests", or "/write-tests".
- A feature just landed without tests, or task-executor hands off a test-writing step.
- The user wants to change untested legacy code safely (pin first, then change — composes with `safe-refactor`).

Do **not** auto-trigger when the user is debugging a failing test (`diagnose`) or reviewing test quality in a diff (`code-review`).

## Workflow

1. **Establish the baseline.** Detect the test runner (`package.json` scripts, `*.csproj`, `pytest.ini`, `go.mod`, `Cargo.toml`, `Makefile`) and run the existing suite **in non-interactive mode** — a `test` script that launches watch mode never exits and never yields a result; use the runner's single-run form (`CI=true`, `--run`, `--watchAll=false`, or the repo's `test:ci` script). Quote its summary line in your report. A result you didn't observe is `tests: not run`, never "passing". If the suite is already red, stop and surface it — new tests on a red suite are unverifiable.
2. **Read the whole unit under test**, not just the part the user pointed at. A claim about code you haven't opened is a hypothesis. Note every branch, early return, thrown/returned error, and boundary (empty, zero, max, null, duplicate, concurrent).
3. **Enumerate candidate behaviors and rank by risk.** Risk = likelihood of being wrong × cost of being wrong. Error paths, money, auth, deletion, retry/idempotency, and date/timezone logic outrank happy paths. Write the ranked list down before writing any test — it is the spec for step 5.
   - ❌ One happy-path test per public method, top to bottom.
   - ✅ Three tests on the refund-calculation branch and its rounding boundary, one on the happy path. The refund bug costs money; the happy path is exercised by every caller already.
4. **Check for existing coverage first.** Grep the test directory for the unit's name and read what's already asserted. Zero new tests is a valid outcome — if the ranked behaviors are covered, cite the existing test `file:line` and stop. Duplicating coverage is negative value: two tests break on every refactor instead of one.
5. **Write each test to a fixed shape.** Arrange-act-assert, one behavior per test, name = scenario + expected outcome (`refund_over_balance_is_rejected`, not `test_refund_2`). Assert observable behavior — return values, thrown errors, persisted state, emitted calls across a real boundary — never internal call order or private state.
   - **Name the break before writing the body.** Answer: *what production change would make this test fail — and is that change a bug or a decision?* Can't name one → redesign around an observable behavior. Only intentional decisions would fail it (a constant's value, exact message wording, private structure) → it's a change detector that fires on redesign and sleeps through bugs; test the behavior that *depends* on the decision instead (not `MAX_RETRIES == 5`, but "a failing call is retried 5 times and the 6th never happens").
   - **Derive expected values by hand.** Literals and hand-checked fixtures; table-driven tests with literal `want` values are the preferred shape. An expectation computed by the code under test (or its helpers) passes no matter what the code does.
     - ❌ `expect(buildQuery({tag:'urgent'})).toBe(buildQuery({tag:'urgent'}))` — mirror assertion, always true.
     - ✅ `expect(buildQuery({tag:'urgent'})).toBe('tag:"urgent"')`.
   - **Your contract, not the framework's.** Test the route you register, the query you emit, the payload you produce — not that the router calls a registered handler. Constructors, getters, constants, and trivial forwarding earn a test only when they validate, normalize, default, derive, or cause side effects.
6. **Prove each test can fail.** This is the step that separates a test from decoration, and it is not skippable:
   - TDD path (the default whenever you are also writing the behavior): write the test before the fix/feature, run it, quote the failure. **It must fail, not error, and fail for the right reason** — "function not defined" / "expected 401, got 200" is red; a typo, import error, or fixture crash is not a red run, fix it and re-run. Passes immediately → you're testing existing behavior; fix the test. Then write the *minimal* code that turns it green — no extra options, hooks, or generality the test didn't ask for — and confirm the rest of the suite stayed green and the output is pristine (no new warnings). Refactor only after green.
   - After-the-fact path: temporarily break the behavior under test (invert the condition, return the wrong value), run, confirm red, revert, confirm green. Quote both runs. **Mutation hygiene:** before reporting, run `git diff` on the production sources and confirm it contains none of your mutations — only the new test files. A leftover mutation is worse than no test; the green suite can't catch the one you made it agree with.
   - A test that stays green against broken code is tautological. Fix its assertion or delete it — never ship it.
   - **Mutation check before finishing a file.** Mentally (or actually) apply each realistic mutation and confirm at least one test goes red: wrong constant or argument; wrong branch handler; missing state change or side effect; empty/default return; missing validation for zero, empty, null, unauthorized, or malformed input. A mutation nothing catches marks that behavior unprotected — add the test or state the gap in the report.
7. **Mock only boundaries you don't own** — network, clock, filesystem, database, message bus, external SDKs. Use the project's existing test-double convention (grep sibling tests for the fixture/mocking pattern and match it). Never mock the unit's own collaborators just to assert they were called: that welds the test to the implementation, and the test now fails on refactors and passes on bugs — the exact inversion of its job.
   - ❌ `expect(userService.formatName).toHaveBeenCalledWith(user)` — asserts plumbing; survives `formatName` returning garbage.
   - ✅ `expect(response.displayName).toBe("Smith, Jane")` — asserts the observable result; survives any internal restructure that keeps behavior.
   - **Learn the real method's side effects before mocking it.** Mock the slow/external level *below* the behavior the test depends on; a mock that swallows the config write your assertion reads passes while integration breaks. Unsure → run against the real implementation first and observe what actually needs to happen. **Mock responses mirror the complete real structure** (all documented fields), not just the ones this test reads — partial mocks fail silently downstream. When mock setup outgrows the test logic, switch to an integration test with real components.
   - **Test-only code stays out of production classes.** A `destroy()`/`reset()` called only from tests belongs in a test utility, not on the class under test. Ask: is this method called only from tests? Does this class own the resource's lifecycle? Wrong answers → test utility.
8. **For untested legacy code: characterization tests first.** Capture what the code *does* (run it, record actual outputs for the ranked inputs), not what you believe it should do. If an output looks like a bug, pin it anyway with a comment: `// characterization: pins current (possibly wrong) behavior — see #issue`. Report the suspected bug separately; changing it is a behavior change, not a test.
9. **Final gate.** Run the full suite once more and quote the summary. Report: behaviors covered (with test names), behaviors deliberately not covered and why, and any suspected bugs found while reading. Rank the report — the two tests that matter, not fifteen equal bullets.

## Examples

### Example 1: "add tests for this service"

**User:** "Add tests for `InvoiceService.applyCredit`."

**Claude:** Runs the suite (quotes `47 passed`), reads the whole method plus the two private helpers it calls, ranks behaviors (credit > balance, negative credit, concurrent double-apply, happy path), finds the happy path already covered in `InvoiceServiceTests.cs:88`, writes the three missing tests, breaks the guard clause to prove each goes red, restores, quotes final green run.

### Example 2: pinning legacy code before a refactor

**User:** "I need to restructure this 400-line pricing function but there are no tests."

**Claude:** Enumerates its branches, runs the function against boundary inputs to record actual outputs, writes characterization tests pinning them (including one output that looks off, labeled and reported separately), proves they fail against a mutated copy, then hands off to `safe-refactor`.

## Anti-patterns

- ❌ Reporting "tests pass" without quoting an observed run — a result you didn't observe is "not run".
- ❌ Shipping a test you never saw red. Green-only tests are the largest source of fake coverage.
- ❌ Asserting a mock was called with the arguments you configured it with — the test proves the test.
- ❌ Testing private methods directly or reaching into internal state — test through the public surface; if a private method needs its own tests, that's a signal it wants to be its own module (note it, don't force it).
- ❌ Snapshot-testing large structures as a substitute for choosing an assertion — a 200-line snapshot fails on everything and tells the reader nothing.
- ❌ `sleep()`-based waits for async behavior — poll a condition or inject the clock; time-based tests are flaky by construction.
- ❌ Sharing mutable fixtures across tests so ordering matters — each test arranges its own world.
- ❌ Change detectors — asserting a constant's value, exact copy text, or private structure. Fires on every redesign, silent on every bug.
- ❌ Mirror assertions — expected value built by the same code (or helper) under test. Always green.
- ❌ Asserting a `*-mock` test ID or that a mock element rendered — the test proves the mock exists, not that the component works.
- ❌ Grepping source text to "test" a script, skill, or config — run the artifact against controlled inputs and assert outputs/exit codes; prose for humans earns no test.
- ❌ Chasing a coverage percentage — coverage measures execution, not assertion. A line executed by a tautological test is worse than uncovered, because it looks protected.
- ❌ "Fixing" a legitimately-failing existing test by weakening its assertion to get to green — that's deleting a regression alarm; surface it instead.
- ✅ Ranked behavior list → match project conventions → observable assertions → every test proven red-capable → summary lines quoted.

## Notes

- Framework specifics (NUnit conventions for .NET APIs, RTL queries for React, etc.) come from the repo, not from memory — grep sibling tests and imitate the strongest existing example, matching its fixture, naming, and assertion style.
- When the unit is hard to test (needs six mocks, giant setup), say so in the report: test pain is design feedback. Offer `improve-codebase-architecture` rather than heroically mocking through it.
- Apply `think-like-fable` discipline throughout: effort follows risk (step 3), claims are re-derived not recognized (steps 1, 6), and the report leads with what matters.
