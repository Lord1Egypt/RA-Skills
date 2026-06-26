# Release Gate

Use this checklist when the user asks if a branch, PR, or feature is ready to ship.

## Release Validation Structure

Report with these sections:
1. Scope validated
2. Evidence collected
3. Gaps / not tested
4. Risks / blockers
5. Recommendation

## Minimum Checks

### Functional
- critical flows pass
- bug fix/regression scenarios covered
- empty, invalid, and edge states considered

### Contract
- API status codes correct
- response shape matches expectations
- backward compatibility stated clearly

### Reliability
- no flaky waits in newly added E2E tests
- test setup/teardown is isolated
- failures are reproducible

### Evidence
Only report what is true:
- commands actually run
- results actually observed
- screenshots/logs/errors actually captured

If something was not run, say exactly that.

## Recommendation Labels

Use one of these:
- **Ready** — enough evidence, no blocking risk found
- **Ready with risk** — acceptable but known non-blocking gaps exist
- **Not ready** — blocking failures, missing validation, or high uncertainty

Never promote to Ready without evidence.
