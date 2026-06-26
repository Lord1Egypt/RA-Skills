# Socrates Examples

These examples show the expected tone and shape. Keep the reasoning compact and action-oriented.

## Planning Example

### Request

Plan a migration from a single API service to separate read and write services.

### Response Shape

```md
Socratic Pass
Round 1
- Goal and done criteria: Produce a migration plan that splits read and write traffic without breaking current clients.
- Knowns, unknowns, assumptions: I know the current service boundary and expected traffic pattern. I do not yet know deployment constraints or rollback limits. I assume the API contract should remain stable in v1.
- Risks: Client breakage, dual-write inconsistencies, and an unclear rollback path.
- Chosen approach: Plan an incremental split behind a stable interface, instead of a full rewrite, because it reduces migration risk.
- Next actions and delegation: Map current boundaries, define a phased rollout, then assign interface validation and data consistency checks if sub-agents are available.

Action Plan
1. Inventory the current responsibilities and stable contracts.
2. Define the target read and write boundaries plus rollback strategy.
3. Sequence rollout phases and validation checkpoints.
```

## Coding Example

### Request

Add request rate limiting to a public API endpoint before implementing the code change.

### Response Shape

```md
Socratic Pass
Round 1
- Goal and done criteria: Add rate limiting that protects the endpoint without breaking expected client behavior.
- Knowns, unknowns, assumptions: I know the endpoint and likely middleware layer. I do not yet know per-tenant versus global limits. I assume we need a safe default and observability.
- Risks: Choosing the wrong scope, causing false positives, or adding state in the wrong layer.
- Chosen approach: Implement a middleware-based limiter with explicit configuration points because it keeps the change localized and testable.
- Next actions and delegation: Confirm the limit model, identify the middleware entry point, then implement and test.

Action Plan
1. Confirm the intended limit scope and fallback behavior.
2. Add the limiter in the request pipeline.
3. Test normal traffic, bursts, and error responses.
```

## Delegation Example

### Request

Split a feature delivery task across a frontend sub-agent and a backend sub-agent.

### Response Shape

```md
Socratic Pass
Round 1
- Goal and done criteria: Deliver the feature with aligned UI behavior and API support.
- Knowns, unknowns, assumptions: I know the feature goal and the likely frontend and backend touchpoints. I do not yet know the final payload shape. I assume we can lock an interface before parallel work starts.
- Risks: Mismatched contracts, duplicated effort, and late integration failures.
- Chosen approach: Define the shared contract first, then delegate implementation tracks in parallel.
- Next actions and delegation: Write the interface contract, spawn frontend and backend sub-agents with the same contract, then review integration results.

Action Plan
1. Define the shared API and UI expectations.
2. Delegate implementation with the same constraints and deliverable format.
3. Reconcile integration gaps and run final verification.

Delegation Contract
- Goal: Implement one side of the agreed feature contract.
- Done criteria: Your change matches the shared contract and reports any mismatch immediately.
- Constraints: Do not change the contract without surfacing it. Run Socrates first.
- Deliverable: Short summary, changed files, tests run, blockers.
- Run Socrates first: Perform a concise mini pass before acting and use Round 2 only if a material ambiguity remains.
```

## High-Risk Round 2 Example

Use a second round only when the first round still leaves a major decision open.

```md
Socratic Pass
Round 1
- Goal and done criteria: Choose a caching strategy for a high-traffic endpoint.
- Knowns, unknowns, assumptions: I know the traffic profile but not the invalidation guarantees required by downstream consumers.
- Risks: Serving stale data or adding an invalidation path we cannot support.
- Chosen approach: No final choice yet. Two options remain viable: TTL cache and event-driven invalidation.
- Next actions and delegation: Run Round 2 on invalidation guarantees before planning implementation.

Round 2
- Trigger: Two plausible approaches remain live and the tradeoff is not settled.
- Follow-up question(s): What freshness guarantees are actually required, and can the current system emit reliable invalidation events?
- Resolution: If strong freshness is required and events are reliable, prefer event-driven invalidation. Otherwise choose TTL caching with explicit freshness limits.

Action Plan
1. Confirm freshness guarantees.
2. Select the caching strategy based on that answer.
3. Implement observability and rollback hooks.
```
