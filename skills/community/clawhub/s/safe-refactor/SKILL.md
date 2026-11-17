---
name: safe-refactor
description: Execute a behavior-preserving refactor with a proof of preservation — establishes a safety net first (existing tests or new characterization tests over every touched path), locks a baseline green run, then moves in small always-green steps where each step is one mechanical transformation, and treats any needed assertion change as a smuggled behavior change to surface, not fix. Use this skill whenever the user says "refactor this", "clean this up without changing behavior", "extract this into", "restructure this module", "rename this across the codebase", "inline this", "split this function/class", or "/safe-refactor" — even if they don't explicitly say "refactoring skill". Do not use for choosing WHAT to refactor (use improve-codebase-architecture) or for changes that are supposed to alter behavior (use task-executor).
---

# Safe Refactor

Execute a refactor as a sequence of proofs, not a rewrite. "Behavior-preserving" is a falsifiable claim: the observable behavior before and after must be identical, and this skill's job is to make that claim checkable at every step instead of asserting it once at the end. The completion of the chain: `improve-codebase-architecture` names the target, `write-tests` builds the net, this skill makes the move.

## When to use this skill

- The user says "refactor this", "clean this up", "extract X into Y", "restructure without changing behavior", "rename across the codebase", "split this up", "inline this", "/safe-refactor".
- `improve-codebase-architecture` produced an approved deepening candidate and the user says "do it".
- A feature task requires restructuring existing code before the new behavior can land (do the refactor as its own phase, this skill governs that phase only).

Do **not** auto-trigger for changes meant to alter behavior — bug fixes, feature work, "improve this error message" — those are `task-executor` territory. If the user's "refactor" turns out to include behavior changes, split the work: refactor first under this skill, behavior change after, never interleaved.

## Workflow

1. **Write the behavior contract.** One short list: the observable surface of the code being moved — public functions/endpoints and their outputs, side effects (writes, emits, logs that anything consumes), error types thrown, and performance characteristics if anything depends on them. This list is what "preserved" means; everything not on it is fair game. If you can't write the list, you haven't read enough code yet — a claim about code you haven't opened is a hypothesis.
2. **Audit the safety net.** For each item on the contract, find the test that would fail if it broke — grep the test tree, cite `file:line`. Contract items with no covering test get characterization tests **before any restructuring begins** (per `write-tests`: pin actual behavior, prove each test can go red). No net, no refactor — this gate is not skippable, and "the change is simple" is not an exemption; simple changes with no net are how behavior drifts silently.
3. **Lock the baseline.** Run the full suite (single-run mode, never watch mode) and build; quote both summary lines. A result you didn't observe is "not run", never "passed". If anything is red before you start, stop and surface it — you cannot distinguish your breakage from pre-existing breakage on a red baseline.
4. **Plan the move as mechanical steps.** Each step is ONE named transformation — extract function, move file, rename symbol, inline variable, introduce parameter, replace conditional with polymorphism — small enough that if the suite goes red, the cause is unambiguous. Order steps so each leaves the code compiling and the suite green. Present the step list before executing.
5. **Execute step → verify → step.** After every step: build + run the affected tests (full suite at least at every commit point), quote the result. Green → proceed. Red → the step is wrong; revert or fix *the step*, never the test. Each step (or small coherent group) is a rollback point — ask once, up front, whether to commit at these points; committing without that yes is not authorized by this skill.
6. **Renames are grep-verified, not assumed.** After renaming or moving a symbol, grep for the old name repo-wide — including strings, configs, reflection sites, docs, and serialized names (JSON keys, DB column mappings, API routes). Zero hits or each remaining hit justified in one line. Dynamic-dispatch and reflection usages don't break the build; the grep is the only net they have.
   - ❌ "Renamed `getUser` to `fetchUser`; build is green, done." — the build can't see the `"getUser"` string in the route table.
   - ✅ "Renamed; repo grep for `getUser` returns 2 hits: a CHANGELOG entry (historical, left) and `routes.json:14` (updated)."
7. **The assertion-change tripwire.** If any step makes an existing test fail and the "fix" would be changing that test's assertion, expected value, or setup — **stop**. That is the definition of a behavior change wearing a refactor's clothes. Surface it: quote the old and new behavior, ask whether the change is intended. Only test changes allowed without asking: mechanical renames mirroring step 6, and import/path updates.
   - ❌ Silently updating `expect(total).toBe(107.10)` to `109.31` mid-refactor because "the new rounding is more correct."
   - ✅ "Step 4 changes the rounding point, which alters totals on multi-line invoices (old: 107.10, new: 109.31). That's a behavior change, not a refactor — proceed with old behavior preserved, or split this into a follow-up?"
8. **Final proof.** Full suite + build, summaries quoted. Then re-read the complete diff once, adversarially, hunting for the behavior change you smuggled in without noticing — reordered side effects, a dropped `await`, a widened catch, changed default parameter, iteration-order dependence, log lines something might parse. Report: contract (each item → covering test), steps taken, grep results for renames, and anything intentionally left un-refactored with a one-line why.

## Examples

### Example 1: extract a module

**User:** "Pull the pricing logic out of `OrderService` into its own `PricingEngine`."

**Claude:** Writes the contract (3 public methods, the discount side effect, 2 error types), finds tests covering 2 of 3 methods, writes characterization tests for the third and proves them red-capable, locks baseline (`112 passed`, build green), then: extract class → move methods one at a time → re-point callers → delete originals, suite quoted green after each, old-name grep clean, final adversarial diff read confirms no reordered side effects.

### Example 2: the smuggled behavior change

**User:** "Refactor this date-handling mess to use one formatter."

**Claude:** Mid-sequence, unifying formatters makes a test expecting `"3/5/2026"` fail because the shared formatter emits `"03/05/2026"`. Stops at the tripwire, shows both outputs, asks: preserve the legacy format via a format parameter (pure refactor), or adopt the new format (behavior change, separate commit, may affect consumers)?

## Anti-patterns

- ❌ Refactoring untested code because "it's a small change" — the net gate (step 2) exists precisely for the changes that feel too small to break anything.
- ❌ The big-bang rewrite: restructure everything, then see what's red. When five things break you can't attribute any of them.
- ❌ Fixing a red step by editing the test — the tripwire (step 7) exists because this is the single most common way behavior changes ship inside "refactors".
- ❌ Interleaving "while I'm in here" behavior improvements with the restructuring — one diff, two intents, zero reviewability. Queue them for after.
- ❌ Trusting the compiler to catch all breakage from a rename — strings, reflection, routes, and serialization don't compile-check.
- ❌ Reporting the refactor complete without quoting the final suite run — "not run" is the only honest label for an unobserved result.
- ❌ Refactoring toward a pattern the repo doesn't use because it's considered best practice — match the codebase's existing idiom; consistency is a feature.
- ✅ Contract → net → baseline → small proven steps → grep-verified renames → adversarial final read.

## Notes

- Commit hygiene: keep refactor commits free of behavior changes so `git bisect` stays useful and reviewers can verify "no behavior change" structurally. Use `conventional-commits` (`refactor:` type) when committing.
- If the safety-net phase reveals the code is nearly untestable, that finding may reorder the plan — sometimes the first refactor step must be the minimal seam that makes testing possible (extract the untestable I/O, pin the rest). Say so rather than silently expanding scope.
- Apply `think-like-fable` throughout: the contract is the decomposition into independently checkable pieces, every green claim is re-derived by running (never recognized), and the final adversarial read is attacking your own conclusion before handing it over.
