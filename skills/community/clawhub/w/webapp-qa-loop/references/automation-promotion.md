# Automation Promotion

## Use existing automation first

Discover the project's current unit, integration, component, contract, and E2E frameworks. Extend the closest layer that can prove the repaired contract. Do not install a second E2E runner or create an isolated test architecture without strong repository evidence and user authorization for the dependency change.

## What to promote

Promote a browser-discovered defect into stable automation when at least one applies:

- it affects a P0/P1 or frequent P2 journey;
- it has regressed before or is easy to reintroduce;
- it depends on a non-obvious state transition, permission, cache, navigation, or async race;
- the fix changes shared code with multiple consumers;
- manual verification is costly or ambiguous;
- release confidence materially depends on the behavior.

Do not automate transient third-party failures, visual preferences without an approved baseline, or scenarios requiring prohibited real-world side effects.

## Choose the cheapest reliable layer

- unit: pure transformation, validation, selector, reducer, or policy;
- component: rendering, focus, interaction, and local state contract;
- integration/contract: API mapping, persistence, permissions, message/schema boundary;
- E2E: cross-route, browser, auth, storage, or deployed-system behavior that lower layers cannot prove.

Prefer a narrow lower-layer regression plus one critical E2E path over duplicating every assertion in the browser.

## E2E reliability rules

- locate by role, label, accessible name, or stable test ID;
- wait on observable state, not fixed time;
- create unique deterministic data and clean only what the test owns;
- assert durable outcomes, not implementation details or toast text alone;
- isolate external dependencies through the project's supported test environment;
- capture screenshot, trace, console, and network artifacts on failure when the framework supports them;
- avoid global ordering and shared mutable accounts;
- keep the test readable as a user journey.

## Flake policy

Do not hide a flaky test with unconditional retries. First classify the source:

- product race or nondeterminism: fix the product contract;
- test synchronization: wait on the correct observable state;
- environment instability: isolate or record the dependency;
- third-party instability: stub only if the test objective allows it;
- data collision: generate owned unique fixtures.

Use the repository's existing retry policy only after the failure class is understood. Quarantine is a temporary documented state with owner and exit condition, not a pass.

## Coverage maintenance

Link each promoted test to its ledger issue in the issue verification text or repository convention. Record the exact command and result as a ledger check. Remove redundant browser steps only after the automated test proves the same contract and the declared manual coverage remains sufficient.
