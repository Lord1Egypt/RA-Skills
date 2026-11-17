# Scope and Scenario Selection

## Build one test charter

Convert the request and repository evidence into a compact charter before interacting with the app:

- authority mode, `repair_authorized` when relevant, and depth;
- target URL/environment, immutable target identity when needed, and expected version;
- roles and authentication constraints;
- in-scope journeys, recent changes, acceptance criteria, and exclusions;
- state-changing or externally visible actions and their authorization status;
- viewports, browsers, locale, data states, and network states that materially affect behavior;
- existing automated coverage and known baseline failures;
- for `release` only: intended artifact, deployment path, separately authorized Git/delivery operations, and rollback readiness/execution authority.

Do not ask the user to restate facts already visible in the repository or active browser, except facts that must be explicit in the current task: production identity and external-action authorization. An `audit` does not need and must not ask for a release path.

## Separate mode from depth

Mode describes authority:

- `audit` observes and reports, including verification of a build that is already deployed;
- `repair` permits source/test edits and local verification but not delivery or deployment;
- `release` means this run will initiate a deployment. It may use `repair_authorized=false` when deploying a prepared artifact without source changes.

Depth describes coverage. Apply these rules in order:

1. Honor an explicit depth or coverage statement from the user.
2. Use `release-regression` for an actual release, verification of an already-deployed build, or shared-impact changes involving auth, global navigation/state, schema, tokens, or infrastructure.
3. Use `targeted` for a named defect, page, journey, or recent change when rule 2 does not apply.
4. Use `smoke` for a vague broad check without comprehensive or release intent.

“Test checkout end to end” is `targeted` coverage of the checkout journey from entry through durable downstream effect. It does not mean every route, role, or site-wide release regression. “End to end” changes the boundaries of the named flow, not the whole application.

An audit is nontrivial, and therefore uses the durable ledger, when any of these apply:

- more than one route or material journey is covered;
- authentication or state-changing behavior is exercised;
- depth is `release-regression`;
- P0/P1 risk is plausible;
- the work may pause, resume, cross agents, or needs durable evidence for handoff.

A narrow, read-only, single-public-route check can remain lightweight.

## Resolve targets and authority

Repository configuration can reveal candidates but cannot authorize production. Before any production access or action, require the current task to name provider, account, project, environment, and region, plus an immutable target identifier when the platform provides one. This remains mandatory when production is the only configured/default target or the browser is already open there.

For a non-production target, state the resolved identity and confirm it is isolated or shared. A single discoverable isolated target may be selected when consistent with the request. Shared non-production remains read-only by default unless the required mutation has exact authorization.

Exact authorization records:

- environment and immutable target identity;
- action;
- affected object, account, and recipient as applicable;
- amount or maximum item count;
- expected external effect;
- cleanup or recovery plan;
- authorization boundary for this one run.

Do not ask again when these are already clear and unchanged. “Do everything,” “do not ask,” and “you decide” do not fill missing fields or add Git, delivery, deployment, rollback, production, or high-side-effect authority.

## Discover journeys from evidence

Prioritize evidence in this order:

1. explicit user request and acceptance criteria;
2. repository instructions and product documentation;
3. existing E2E/integration tests;
4. route and navigation definitions;
5. API clients, state machines, feature flags, and permission guards;
6. analytics names, fixtures, and recent code changes;
7. visible UI.

Map each journey as `entry → decision/state → mutation → confirmation → persistence/downstream effect`.

## Risk scoring

Use a lightweight score to choose scenarios, not to create false precision:

`risk = impact (1-4) × likelihood (1-4) × change reach (1-3)`

- 24-48: class A, always execute and verify persistence or downstream effect.
- 10-23: class B, execute the most likely boundary/error/permission variants.
- 1-9: class C, sample when time and scope allow.

Increase impact for money, privacy, identity, permissions, irreversible state, contractual workflows, or shared infrastructure. Increase change reach for shared tokens, router, auth, schema, state, or component primitives. Risk scoring selects coverage; it never authorizes a mutation.

## Scenario classes

For each material journey, consider:

- happy path;
- required and invalid input;
- empty, loading, error, and retry states;
- duplicate submission and rapid interaction;
- refresh, back/forward, deep link, and interrupted navigation;
- authorization and role boundaries;
- persistence and cross-page consistency;
- responsive layout, keyboard use, focus, and accessible naming;
- slow or failed dependency where safely reproducible.

Select only applicable variants. Do not manufacture invalid states or cause prohibited real-world effects merely to fill a matrix.

## Pairwise matrix

When several variables interact, cover pairs rather than the Cartesian product. Typical variables include role, viewport, data state, network state, locale, and entry path. Ensure each important pair appears in at least one declared scenario, then add explicit high-risk triples for known production risks.

## Impact radius for regression

For a changed file or behavior, map:

- direct route/component/service;
- callers and consumers;
- shared state, cache, schema, and event effects;
- permissions and error boundaries;
- equivalent workflows using the same abstraction;
- build, deployment, and runtime configuration.

The map selects R0-R3 regression. It does not authorize unrelated refactoring or expand the declared target.
