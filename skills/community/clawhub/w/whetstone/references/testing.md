# Verification

Use to choose evidence for a changed behavior. Preserve the repository's required checks.

## Find the cause

For a bug or failing test, reproduce the smallest failing case or inspect its actual output, read the relevant caller and implementation, and change the cause rather than adding a catch-all or retry that hides it. [Debugging](debugging.md) covers isolation, flaky tests and incidents. For performance work, compare the same workload and environment before and after the change. Include tail latency under stated concurrency when users experience slow outliers; an average from an idle system cannot establish that behavior. [Observability and performance](observability-and-performance.md) covers baselines and targets.

A flaky test calls for evidence about shared state, clock assumptions, order, concurrency or external dependencies. A temporary quarantine needs an explicit scope and a tracked fix; it does not establish correctness.

## Choose a check that could fail

| Changed behavior | Useful evidence |
|---|---|
| Parser or calculation | Known input/output plus malformed, empty or boundary input |
| Access decision | Allowed caller and denied caller, including another owner or tenant |
| Database constraint or migration | The actual database engine and the affected data/rollback behavior |
| Remote write or job | Timeout after acceptance, duplicate delivery and partial failure |
| Public response | Existing consumers and the changed response shape |
| UI interaction | User action and observable result, including keyboard operation |

Use a focused unit test for isolated logic and an integration check where the boundary matters. Do not mock away the behavior being verified. Derive expected values from the contract or independent fixtures, not the production calculation under test. Control clocks and state when timing affects the result. A bug regression should fail on the old implementation and pass on the fix when that comparison is practical.

For a small reversible edit, an existing test or direct check may be enough. Do not create tests that restate constants, wording or implementation details merely to increase coverage. Property-based, load or mutation testing belongs where the input space or failure cost justifies it.

## Stop with usable evidence

Run the focused check, then the project-required suite. Broaden or repeat tests only for a new failure or an unresolved concern. Distinguish pre-existing failures from regressions. If a test expectation is obsolete, explain the changed contract and preserve coverage of the intended behavior; do not loosen it just to pass.

State what ran, what passed or failed, and any material unchecked behavior. A mocked provider test does not prove live credentials work; unit tests do not establish model behavior or production recovery.

## Sources

- [Google engineering practices: code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)
- [Google Testing Blog](https://testing.googleblog.com/)
