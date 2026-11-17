# Debugging

Use for a bug report, a failing or flaky test, a crash, unexplained behavior or a production incident.

## Reproduce

Get the exact input, version, configuration and steps from logs, tickets or the running system before asking. Check the configuration and versions actually in effect. Capture the failure as an automated test at the lowest level that still fails, then shrink it until every remaining part matters.

If it will not reproduce, gather evidence instead of guessing. Compare a failing case with a working one and list what changed recently: deploys, configuration, flags, dependencies, data shape, traffic, certificates and clocks. Add targeted logging, metrics or a consistency check to catch the next occurrence. Do not ship a speculative change as a fix; report an unproven cause as suspected.

## Isolate the cause

Rank candidate causes by likelihood and by how cheaply each can be tested. Predict the result before each experiment, and prefer experiments that can rule a cause out. Change one thing at a time and revert experiments that did not help. A recent deploy is the first suspect, not the proven cause. After three failed hypotheses, widen the evidence before guessing again.

With a known good version, `git bisect run` finds the first bad commit using a script that exits 0 for good, 1 for bad and 125 for untestable commits. Finish with `git bisect reset`.

## Fix and guard

Name the cause and its evidence before changing code. Fix the cause: a null check, broad catch or retry that hides the error is a symptom fix. Show that the regression test fails before the fix and passes after it, then run the surrounding suite. Search for the same pattern elsewhere and fix it or list it. Remove temporary instrumentation, or turn it into proper telemetry.

## Flaky tests

Investigate before retrying. Run the test many times and record the failure rate, varying order, seed, parallelism, time zone and load. Shared state, time, ordering assumptions, unawaited async work, real network calls and leaked resources cause most flakiness. Fix the demonstrated cause; a retry only hides the race the test found. If the user agrees to a temporary quarantine, make it explicit and narrow, link a tracked issue with an owner, and never report it as a fix.

## Incidents

Stop the impact first. Use the fastest authorized and reversible mitigation, such as a rollback, a disabled flag or shifted traffic, before deep diagnosis, and check that a rollback still understands the current data and configuration. Ask for any production action that existing authorization does not cover, while diagnosing read-only. Preserve evidence: logs, the bad artifact, affected records. After recovery, find the cause and add the regression test, alert or procedure fix it calls for. See [delivery](delivery-and-release.md) for recovery; the optional [incident review](../templates/incident-review.md) suits incidents whose impact or team practice calls for one.

## Sources

- [Google SRE book: effective troubleshooting](https://sre.google/sre-book/effective-troubleshooting/)
- [Google SRE book: managing incidents](https://sre.google/sre-book/managing-incidents/)
- [Git documentation: git bisect](https://git-scm.com/docs/git-bisect)
- [pytest documentation: flaky tests](https://docs.pytest.org/en/stable/explanation/flaky.html)
