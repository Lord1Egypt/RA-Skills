# E2E Reliability

## What E2E Is For

Reserve E2E for critical flows such as:
- login/logout
- onboarding
- checkout/submission flows
- high-value admin operations
- cross-page regression journeys

## Selector Policy

Priority order:
1. `role`
2. `label`
3. `data-testid`
4. visible text

Avoid:
- CSS class selectors
- nth-child selectors
- fragile DOM path selectors

## Wait Strategy

Never use fixed sleeps.

Prefer:
- URL assertions
- visible/hidden assertions
- network response waits when necessary
- element enabled/disabled state
- built-in auto-waiting assertions

## Data Isolation

- each E2E test should create its own data if possible
- clean up created state
- do not depend on leftover state from previous tests
- avoid ordering assumptions

## Flaky Test Triage

When E2E is flaky, check in this order:
1. unstable selector
2. missing explicit wait condition
3. async race with network/UI
4. shared state or polluted environment
5. external dependency instability
6. animation/timing issue

## E2E Scope Control

A healthy suite has:
- few tests
- short scenarios
- business-critical coverage only

If a scenario is mostly form validation or local state behavior, move it to unit/integration.
