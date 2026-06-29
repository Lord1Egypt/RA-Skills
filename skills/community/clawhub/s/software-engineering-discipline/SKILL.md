---
name: software-engineering-discipline
description: "Engineering discipline for coding agents on large, complex codebases. Apply when writing, refactoring, or reviewing non-trivial code in real systems — enforce architecture boundaries, SOLID/cohesion, contracts, concurrency, migrations, security, and bounded blast radius instead of just completing the task."
---

# Software Engineering Discipline

Constraints for coding agents working in large, complex, real systems. The goal is not to *complete the task* — it is to leave the system **more coherent, not less**.

**A passing test is necessary, not sufficient. Code that works but corrodes the architecture is a defect.**

**Skip this skill when:** the change is <~50 LOC, single-file, throwaway prototype/spike, or glue/script code with no existing tests. This enforces a Clean-Architecture / SOLID / DDD bias that is overkill for small jobs — use judgment.

## 0. Understand Before You Touch

Before writing in an existing codebase:
- Read the module you're changing AND its callers/callees. Trace the data flow in and out.
- Find the existing pattern for this kind of work (`grep` a sibling feature) and follow it. Match existing style even if you'd do it differently.
- Name the architectural layer you're in (domain / application / infrastructure / UI) and its rules.
- Read the existing tests; they encode the intended behavior and contracts.

Self-check: Can you name the layer, the convention, and who depends on this code? If not, stop and investigate.

## 1. Boundaries & Dependency Direction

- Don't reach across a layer to grab internals — call the public interface.
- **DIP:** depend on abstractions, not concretions. High-level policy must not import low-level detail.
- Dependencies should also point toward the more *stable* module (Stable Dependencies Principle).
- No new circular dependencies. No domain logic importing framework/IO.
- (This skill's style) keep business rules out of controllers/handlers; if your framework's idiom differs, follow the codebase's existing convention.
- If the clean change requires crossing a boundary, surface it and propose the seam — don't smuggle it through.

Self-check: Does your new code import from the IO/framework/UI layer into core logic? If yes, you're inverting the wrong way.

## 2. Cohesion & Single Responsibility

- A unit should do one coherent thing. **If its name or docstring needs an "and", split it.**
- Separate policy vs mechanism, decision vs side-effect.
- One responsibility lives in one place; don't smear it across files, don't pile unrelated ones into one class.
- Prefer adding a new code path over threading a special-case `if` deep into stable core logic — **but a plain `if` is often the correct, simplest answer; don't add inheritance/strategy ceremony just to honor OCP.**

Self-check: Does one conceptual change land in one place? If it forces edits in many unrelated spots, your seams are wrong (unless it's a genuine cross-cutting concern).

## 3. Abstractions That Earn Their Keep

- **DRY is about knowledge, not text.** Two copies of the *same rule/decision* → extract immediately. Code that merely *looks* similar → leave it; premature DRY couples unrelated things.
- Rule of three applies only to *coincidentally similar* code: wait for the third before extracting.
- **YAGNI:** build for today's known requirements. No speculative generality, no "framework" for one caller, no config knobs nobody asked for.
- Prefer a clear name + small function over a clever one-liner. Code is read far more than written.

Self-check: Does this abstraction let a reader change *more* while understanding *less*? If they must learn the machinery first, it's the wrong abstraction.

## 4. Design by Contract & Edges

- State the contract before the body: inputs, outputs, preconditions, postconditions, invariants, error modes.
- **Validate** untrusted input at the system edge (API/UI/IO). Don't re-validate the same thing in every inner function.
- **Assert** invariants that should be impossible to violate (programmer errors) — fail fast and loud. Validation ≠ assertion: edges validate, core asserts; don't sprinkle asserts everywhere.
- Handle expected operational errors deliberately. Don't swallow exceptions.
- Don't break a published contract silently. A signature/behavior/wire-format change is an API change — find callers; version, deprecate with a window, or migrate them.

Self-check: Can a caller use this from the signature + types + name alone, without reading the body?

## 5. Testable, Observable, Evolvable

- If something is hard to test, the design is usually too coupled — inject dependencies, isolate side-effects, separate pure logic from IO. Fix the design, not the test. (Exception: difficulty intrinsic to the domain — real concurrency, time, external IO.)
- Pin the behavior you implement, or reproduce the bug with a failing test *first*, then fix.
- Emit observability where it matters: structured logs + correlation/request IDs at boundaries and failure paths; right log levels; **never log secrets or PII**. Not noise everywhere.
- Keep config out of logic; name constants; leave seams for the next edit.

Self-check: Could a teammate test this in isolation and diagnose a production failure from the signals you left?

## 6. Bounded Blast Radius

- The diff size should match the request size. Touch only what the change requires.
- Don't opportunistically refactor/reformat/"improve" unrelated code in the same change — note it separately.
- A refactor and a feature don't share one commit. One logical change per commit; message says *why*, not just *what*.
- Before a wide change, state the impact surface (files/modules, callers, contracts that move) and confirm if it's large.
- After changing a contract, follow every caller. Don't leave half-migrated state.

Self-check: Every changed line traces to the request, and the reviewer can follow the diff without a map of the whole repo.

## 7. Large-System Hazards (where LLMs ship the most bugs)

- **Concurrency & ordering:** name the transaction boundary. Guard shared state. Assume requests race, retries duplicate, and messages arrive out of order.
- **Idempotency:** any retried/at-least-once operation (payments, webhooks, jobs) needs an idempotency key or a natural unique constraint. "Exactly once" is a lie at the wire level.
- **Data migrations:** schema changes are expand → migrate → contract across releases. **Never drop/rename a column in the same release as the code that stops using it.** Plan backward-compatible reads.
- **Backward compatibility:** additive changes for live APIs/events; gate risky behavior behind a feature flag; remove only after the deprecation window.
- **Failure design:** every remote call has a timeout + a defined behavior on partial failure (retry-with-backoff, fallback, or fail closed). Don't assume the network/dependency succeeds.
- **Performance budget:** know the Big-O and the hot path. No N+1 queries, no unbounded fetch/allocation in a loop, bound payload sizes.
- **Security edges:** authenticate and **authorize at the boundary** (not just validate shape). Parameterize queries; escape at sinks; keep secrets out of code and logs; treat all external input as hostile.

Self-check: For this change — what races, what gets retried, what migrates, who's authorized, what's the cost on the hot path?

## Operating Loop (non-trivial changes)

```
1. Understand → layer, convention, callers, existing tests
2. Design     → contract + seam + blast radius + §7 hazards; pick the simplest fit
3. Confirm    → if radius is large or a boundary/contract/migration moves, surface it first
4. Implement  → smallest change that fits the architecture; follow existing patterns
5. Verify     → new behavior pinned by tests; existing tests green; diff bounded
6. Self-review→ run the self-checks; if one fails, fix the design, not the symptom
```
