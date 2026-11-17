---
name: Technical Debt
slug: tech-debt
version: 1.0.0
homepage: https://clawic.com/skills/tech-debt
description: Reckless versus prudent categorization, tracking the inventory, and a payoff cadence that does not freeze delivery.
metadata: {"clawdbot":{"emoji":"⚙️","requires":{"bins":[]},"os":["linux","darwin","win32"]}}
---

## What counts as debt

The quadrant that matters is reckless vs prudent; the deliberate/inadvertent split is post-hoc. The #1 adds the axis that drives action: does the debt accrue interest?

- **Prudent, deliberate** = a conscious speed-vs-quality trade with a booked payoff. "Ship now, learn; pay down before X." The only debt that is genuinely a tool; write the item to the register when you merge the shortcut, or it is a gift, not debt.
- **Prudent, inadvertent** = you chose well with what you knew; a better path surfaced later. Retroactive, not a mistake. Pay when the better path lands on the critical path.
- **Reckless, deliberate** = "we don't have time to do it right." Convert it to prudent by writing the payoff trigger; without the trigger it is just bad code.
- **Reckless, inadvertent** = the dangerous quadrant: you do not know it is there until it bites. "What is the architecture?" answered with silence = here. Hunt it via the behavior signals below.
- Bugs are not debt: a defect is a correctness gap with user impact, paid through triage. Calling bugs "debt" inflates the register and defers the fix.
- Missing features are not debt: a gap is a product decision, not a quality trade. Conflating them makes "debt" mean "everything we didn't do."
- A kludge with no clean design in mind is not debt, it is bad code. Debt implies you know the clean version and chose to defer; if you don't know the clean design, the work is design, not payoff.
- The labels do not prioritize; the interest rate does. A prudent debt with high interest blocks the next feature; a reckless debt with zero interest is noise. Rank by interest x blast radius, not by how bad it feels.

## Three numbers per item: interest, blast radius, payoff cost

Every item carries three. The #1 ranks with all three; the #1000 ranks by gut annoyance.

- **Interest (carry)** = (time lost per change) x (change frequency). A complex file nobody touches has zero interest; a simple file touched weekly with a bad abstraction compounds fast. Estimate it as: how much longer does a typical change here take than it should, times how often.
- **Blast radius** = how many distinct changes the debt touches. Local (one module) vs structural (every cross-cutting change pays). Structural debt is far costlier per line than local; prioritize it out of proportion to its size.
- **Payoff cost** = refactor effort + regression risk + opportunity cost of the feature you are not shipping. The #1 budgets the regression risk explicitly (characterization tests, staged rollout); the #1000 estimates only the refactor hours.
- Pay when **fix cost < ~2-3x one quarter's carry**: the fix pays back within 2-3 quarters. Below that ratio, leave it with a comment and a trigger; the payoff capital is better elsewhere.
- High interest + high blast radius + low payoff cost = the highest-ROI work in the codebase. Low interest + high payoff cost = never worth a dedicated effort; fold it into boy-scout cleanup when you are already there.
- Interest compounds on test debt and architecture debt: each change layered on top makes the next one harder. Duplication and doc debt are mostly flat; they do not worsen on their own.
- Don't pre-pay debt on code with no upcoming change. Speculative refactoring is debt creation: you spend now, the code drifts, and you re-pay when the change finally arrives.

## The inventory

A debt register is a living doc, not tickets scattered among features. The #1 maintains one; the #1000 keeps debt "in our heads."

- One row per item: **id, area, type, interest (L/M/H), blast radius (local/structural), payoff cost (S/M/L), trigger, owner.** That is the minimum that prioritizes; less is noise, more rots.
- The **trigger** is the load-bearing field: "pay when we next touch auth," "pay when the dependency goes EOL," "pay when cycle time in this module > X." An item without a trigger is a wish; it will never be prioritized.
- TODOs are not inventory. A TODO is a wish; a register item with a trigger is a commitment. Auditing TODOs produces noise; auditing register items produces decisions.
- Tag debt items in the tracker with a `debt` label AND keep the aggregate register. Tracker-only scatters debt among features and hides it; register-only rots because engineers do not live there. Both: tickets for execution, register for the view.
- A register nobody triages is worse than none: it grows, demoralizes, and is never the source of a real decision. Prune monthly to quarterly: close paid items, re-rate interest, delete items whose code was deleted. An item that survives three prunes unpaid is mis-rated or has no real trigger.
- An empty register means the register is broken, not that there is no debt. Run a "debt wall" session: each engineer adds the items they route around daily. Zero debt = invisible, not absent.
- The register is the week-1 onboarding map: it tells a new hire where the bodies are and which decisions were deliberate. Withholding it makes every new engineer re-learn the traps by stepping in them.

## Payoff cadence

The #1 amortizes continuously; the #1000 oscillates between "ship only features" and "stop everything to clean up." Both ends of that oscillation are failures.

- Sustained allocation: **~15-25% of capacity on debt, every sprint, indefinitely.** Below ~10% the interest outruns the payoff and debt grows. Above ~30% delivery freezes, the business loses patience, and the swing to 0% follows.
- Never ask for a "debt sprint" or a "hardening sprint" as the primary mechanism. Debt sprints confess that continuous amortization failed; they become the only time debt gets paid, so debt accrues faster between them. Use one to break a crisis, then return to the allocation.
- If a hardening cadence is required: a slot every 4-6 sprints, not every sprint. Every-sprint hardening is continuous amortization with worse optics.
- **Opportunity-based payoff** is the default: when a feature touches a debt-bearing area, pay the debt there as part of the feature estimate. The feature absorbs the cost; the debt shrinks where the work is. Boy-scout rule, scoped to what you touched, not a license to go hunting.
- Reserve the dedicated allocation for high-interest structural debt no upcoming feature will touch. Wait for the feature and the interest compounds; pay it proactively.
- Two hats: when adding function, don't restructure; when restructuring, don't add function. Mixing both in one commit hides the refactor from review and entangles the test surface. Call scope expansion out explicitly; silent "I refactored while I was in there" erodes review trust.
- Tie every payoff to a measurable outcome: cycle time down in module X, flaky-test rate below threshold, dependency off the EOL list. "Cleaner code" is not a measurable outcome and loses every priority conflict with a feature. Most "debt payoff" sprints return 0 measurable gain because they paid debt that wasn't the bottleneck.

## Debt types, by interest profile

Each type has a different interest curve and fix order. Know the type before choosing the play.

- **Architecture debt** = the seams are wrong (sync where async belongs, a god module, a boundary that leaks). High interest, structural blast radius, high payoff cost. Fix via strangler fig, never a big-bang refactor. Shows as every cross-cutting feature taking longer than it should.
- **Test debt** = missing, slow, or flaky tests. Compounding interest: each untested change makes the next one scarier; flaky tests erode the trust that makes the suite useful. Fix order: flaky first (they poison the signal), then speed (a suite > ~10 min pushes people to skip), then coverage in the scariest module, not blanket coverage.
- **Dependency debt** = outdated, EOL, or CVE-bearing dependencies. Forced payoff on a deadline. Schedule 1-2 quarters before the EOL/CVE date; this is the one debt security gets to override the payoff queue for.
- **Duplication debt** = the same logic in two places. Mostly flat interest unless both copies are still evolving. Rule of three: copy once (acceptable), twice (smelly), three times (extract). If one copy is frozen, leave it; the coupling from extracting costs more than the duplication.
- **Doc debt** = stale or missing docs on decisions, APIs, onboarding. Low interest, high friction for new hires. Pay opportunistically when you touch the area; a "doc sprint" nobody reads is waste.
- **Dead-code debt** = unused code still in the repo. Near-zero interest but nonzero cognitive cost; every reader pays a tax. Cheapest payoff in the inventory: delete it. If you cannot prove it is unused, add a tombstone (deprecation log) and delete after a quiet release cycle.

## Reading the interest from the code

The #1 reads the interest from behavior, not from a complexity dashboard. Metrics are lagging; behavior is current.

- **Cycle time trending up in one module** = accruing interest. Plot change-to-merge time per module; a ~2x rise over a quarter is a loud signal. Throughput on similar-scope features dropping 20-30% over 6-12 months with stable headcount = debt, not morale.
- **Bug concentration**: a module producing bugs at > ~2x its share of code is a hot spot. The bugs are the interest paid in production.
- **Fear signal**: nobody wants to touch a file, or every change to it ships with a "be careful" comment. Fear is the most honest interest gauge; ask the team which files they avoid.
- **Untouched-but-central files**: a core file untouched for 6+ months is latent debt. The team has routed around it; when a feature finally forces a change, the cost surprises everyone.
- **Flaky-test rate**: > ~1-2% of runs flaky erodes trust; engineers start ignoring red, which hides real regressions. Track the rate; when it climbs, test debt is accruing fast.
- **PR size creeping up in one area**: changes that used to be 50 lines are now 300 for the same feature. The abstraction is fighting you; that is architecture debt.
- Complexity metrics (cyclomatic, cognitive, duplication %) flag candidates but do not prioritize. Target the intersection of top change-frequency and top complexity: the bulk of future defects lands there. A high-complexity file nobody touches is not priority debt.

## When not to pay it

The #1000 pays debt to feel clean; the #1 pays it to unblock a specific future move or to stop a measured bleed. Refuse to pay when:

- The code is slated for deletion or rewrite within ~2 quarters. Verify it is staying first; paying down debt in code you are about to delete is pure waste.
- The debt has no measurable interest (nobody touches the area, no bugs, no fear). Park it; the payoff cost exceeds the lifetime interest. Revisit on the prune cadence.
- You cannot articulate the trigger or the outcome. "It is messy" is not a trigger; "cycle time here is 2x and rising" is. No trigger = no payoff.
- The fix is a "clean slate" rewrite with no parallel-run plan. The rewrite trap: the old system keeps the lights on while the new one bloats (second-system effect), and you ship neither.
- The fix is to disable a flaky test. That converts test debt into hidden production debt; the regression the test was catching now ships. Fix the test, or quarantine it with a ticket and a deadline.
- You are gold-plating: abstracting before you have three concrete examples, or generalizing a path with one caller. Premature abstraction is itself debt; it freezes a design before you know its shape.

## Refactor vs rewrite

Default: refactor. Rewrite is the trap that keeps giving. The conditions for rewrite are narrow and all must hold.

- **Refactor** = behavior-preserving restructuring, verified by tests. If behavior changed, it is a rewrite; call it what it is. Without tests you are gambling, not refactoring; build the harness first.
- Small commits, one concern each: rename in one commit, move in another, change logic in a third. A "cleanup" diff touching 50 files is unreviewable and carries bugs that surface weeks later or gets reverted wholesale.
- A refactor is done when the old path is deleted, not when the new one works. Two implementations running in parallel is half-finished debt, not payoff.
- **Strangler fig** = the refactor pattern for a wrong seam: route new traffic to the new implementation, migrate edge by edge, starve the old until you can delete it. Never a flag-flip cutover on a live system.
- **Rewrite** only when ALL hold: the architecture is fundamentally wrong (not just messy), the old system can run in parallel as reference and fallback, the team understands the old system's behavior (otherwise you rediscover its hidden requirements in production), and there is a strangler-style migration path.
- The **second-system effect**: the rewrite bloats because now you "know" all the features you should add. Freeze scope to parity-first; new features come after migration, never during.
- A rewrite past ~2x the original build time is failing; cut scope or revert to strangler. The original was built under constraints you no longer respect, which is why rewrites overrun.
- Characterization tests are the bridge: before refactoring legacy code with no tests, pin its current behavior with tests that assert what it does (not what it should do). The #1 writes these before touching; the #1000 refactors blind and fixes the regressions in production.

## The metaphor as a translation device

The financial metaphor is for non-engineers; for engineers it is a prioritization frame. Know where it buys alignment and where it breaks.

- Translate debt into carry, not aesthetics. Not "the code is messy" but "each new report takes 3-4 days instead of 1 because the query layer is tangled; fixing it is one sprint and saves 2 days per report, every report, forever." The priced fork wins; "a cleanup sprint" loses.
- Frame the choice as a fork with numbers: "feature Y is 8 days as-is, 5 days if we first spend 3 fixing the auth module, and 5 days every time after." Engineers who ask for "cleanup" lose; engineers who price the fork win.
- Never bundle debt into a feature estimate silently. Inflating the feature to "pay debt" erodes trust and gets the debt cut first; call it a separate line item with its own ROI.
- The "we'll clean it up after launch" promise is rarely honored without a booked date and a named owner. Without both, treat it as permanent debt and decide now whether that is acceptable.
- The metaphor breaks in three places: code is never repossessed (no forced payoff without a trigger), interest can drop to zero (debt in untouched code is free, unlike money), and you can pay debt by deleting the code (no financial analogue). Do not push the metaphor past the allocation conversation.
- Never report debt as a moral failing ("we took shortcuts"). Report it as a balance sheet: what each item bought, what it costs now, the planned payoff. The frame is accounting, not confession.
- Security interface: dependency debt with a CVE or EOL date overrides the payoff queue. Translate it for the PM as "this debt has a foreclosure date," the one thing the financial metaphor models exactly.

## Situations

| Situation | Play |
|---|---|
| PM won't approve cleanup time | Don't ask for a debt sprint. Price the fork: "feature Y is 8 days as-is, 5 days if we first fix auth." The ~15-25% allocation lives inside feature estimates, not a separate ask. |
| A module nobody wants to touch | Measure cycle time + bug rate there. If both trend up it is accruing interest: schedule payoff tied to the next feature that touches it, characterization tests first. |
| Inherited codebase, no tests | Don't refactor first. Ship the next feature behind a characterization test on the behavior you depend on; build the harness incrementally. A big "add tests" effort stalls. |
| New tech lead proposes a rewrite | Default to refactor + strangler. Rewrite only if the seam is fundamentally wrong, the old can run in parallel, and there is a migration path. Parity-first scope. |
| Flaky tests are everywhere | Fix order: flaky first (they poison the signal), then speed (> ~10 min pushes skips), then coverage in the scary module. Never disable a flaky test. |
| A dependency is going EOL | Forced payoff with a deadline. Schedule 1-2 quarters before the EOL date; security overrides the queue. Not optional debt. |
| Two teams duplicated the same service | Only pay if both copies are still evolving. If one is frozen, leave it; the coupling from extracting is not worth it. Rule of three before extracting. |
| Register has 200 items, nothing gets paid | It is a graveyard. Triage to ~10-20 items with triggers and carry costs; archive the rest. A long register demoralizes; a short acted-on one pays. |
| "We'll clean it up after launch" | Get a date and an owner in the plan now, or treat the debt as permanent. Without both, the promise is rarely honored. |
| Velocity dropped, team "got slower" | Check whether the drop tracks a module that got harder to change. 20-30% throughput drop on similar scope in 6-12 months with stable headcount = debt, not morale. |
| A refactor PR touches 50 files | Reject or split. One concern per commit; bundled "cleanup" hides bugs and blocks review. |

## Where camps disagree

- **Dedicated debt sprints vs continuous amortization**: sprints win only to break an accumulated crisis the team cannot otherwise get permission for; continuous (~15-25% every sprint) wins for steady-state. The failure mode of sprints is they become the only time debt gets paid, so debt accrues faster between them. Default continuous; reach for a sprint as a reset, not a rhythm.
- **Rewrite vs refactor**: refactor wins by default. Rewrite wins only when the abstractions encode wrong assumptions (the domain model shifted, not just the code is ugly) AND the old system can run in parallel as reference. The trap is the second-system effect; the guardrail is parity-first scope and a strangler migration.
- **Track debt in the tracker vs a separate register**: tracker-only scatters debt among features (it becomes invisible); register-only rots because engineers do not live there. The frontier is both: `debt`-labeled tickets for execution, a register for the aggregate view and prioritization. One without the other fails in opposite directions.
- **Pay proactively vs pay on contact (boy scout)**: boy scout wins for low-interest, local debt you will touch soon; proactive wins for high-interest structural debt no upcoming feature will touch (interest compounds while you wait). The frontier is interest rate x change-frequency of the debt's location.
- **Complexity metrics vs behavior signals**: metrics find candidates, behavior (cycle time, bug rate, fear, flaky rate) prioritizes. A high-complexity file nobody touches is not priority debt; a simple file with rising cycle time is. Metrics are lagging; behavior is current.

## Related Skills

Install with `clawhub install <slug>` if the user confirms:
- `legacy-code` - inherited codebases and the no-tests scenario where characterization tests pin behavior before any payoff
- `refactoring` - the extract, rename, and strangler-fig mechanics behind every payoff that is not a rewrite
- `tdd` - test debt, characterization tests, and the suite health that test debt erodes
- `review-code` - the review surface where debt is caught at merge and "fix now vs record" gets decided
- `ci-cd` - the test and staged-rollout safety net that makes payoff low-regression-risk
