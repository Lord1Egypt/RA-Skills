# Repair and Reuse Gate

Read this reference before entering `REPAIR` in either `repair` mode or a `release` run with `repair_authorized=true`. A release requested without repair authority must skip `REPAIR`; deployment authority does not authorize source edits.

## Diagnose before editing

For each confirmed issue:

1. trace the observable failure to the closest incorrect state, contract, or transition;
2. identify whether it originates in UI state, domain logic, API contract, persistence, permissions, configuration, or deployment;
3. inspect existing tests and the nearest working analogous flow;
4. explain one current hypothesis and the evidence that could falsify it;
5. make the smallest coherent change that repairs the violated contract.

Do not change code merely to silence a test or browser symptom.

## Mandatory reuse search

Before creating a component, hook, service, utility, abstraction, dependency, or pattern:

- search by responsibility and behavior, not only by the proposed name;
- inspect the closest existing consumers and extension points;
- compare lifecycle, state, accessibility, errors, permissions, and data contracts;
- choose one disposition and record it in the issue ledger:
  - `reuse`: use an existing unit unchanged;
  - `configure`: use existing behavior through supported options;
  - `extend`: add a compatible capability to an existing unit;
  - `extract`: consolidate repeated proven behavior from multiple places;
  - `new`: create a new unit because no existing responsibility fits.

Similarity of markup alone is not enough to force reuse. Different lifecycle, accessibility, error, or domain contracts may justify separate components.

## Pattern threshold

Use a named design pattern only when the code contains the matching pressure:

- state machine/reducer: legal transitions, async races, or multi-step state invariants;
- strategy: at least two real interchangeable algorithms chosen by policy;
- adapter: an external provider or unstable contract must be isolated;
- facade/application service: repeated orchestration spans several lower-level services;
- command: undo, queueing, offline replay, auditability, or retry semantics are required.

Do not introduce a global event bus, generic repository, factory hierarchy, or dependency-injection layer for a single branch. Prefer direct code until variation is real.

## Change boundaries

- Preserve public contracts unless the fix explicitly requires an intentional migration.
- Avoid unrelated formatting or cleanup in a bug fix.
- Add or update the narrowest automated test that fails before and passes after when practical.
- Follow repository conventions for errors, loading, state, telemetry, and accessibility.
- Reuse established design tokens and components. Do not add arbitrary colors or visual rules.
- Never edit generated, vendored, or lock files manually unless the repository workflow requires it.
- Do not replace the project's test framework or add a competing framework for one repair.

## Failed-fix discipline

Record every materially different attempt and its result against the issue and stable attempt identity. After two repairs preserve the same symptom without new evidence, return to diagnosis and widen observability. After three falsified hypotheses, stop and settle the work as blocked with the missing evidence or authority rather than continuing speculative edits. A blocked issue is accounted for, not successfully repaired.

## Review before verification

Before running the browser again, inspect the diff for:

- accidental scope expansion;
- new abstractions or dependencies without evidence;
- duplicated logic that should use an existing implementation;
- changed error, permission, state, or accessibility contracts;
- secrets, debug code, localhost URLs, feature flags, or test-only bypasses;
- missing tests for the repaired contract.
