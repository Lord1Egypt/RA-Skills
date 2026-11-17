---
name: test-code-change
description: "Mandatory risk-driven verification workflow for maintained-code changes. Use when implementing, fixing, refactoring, deleting, migrating, or reviewing code to identify all materially affected behavior, map failure risks to sufficient tests, execute required evidence, and report unresolved test gaps and residual risk."
---

# Verify Code Changes

Maximize confidence in code changes by identifying every materially affected behavior and requiring risk-proportionate evidence capable of exposing its important failure modes.

For every material impact, assign exactly one final status:

- `VERIFIED`: sufficient evidence was executed and observed.
- `NO-TEST-RATIONALE`: testing is unnecessary or impossible for a stated reason.
- `BLOCKED`: required evidence could not be obtained.

Do not declare verification sufficient while any material impact has no status, or any High/Critical risk remains `BLOCKED`.

Operate independently. Accept an existing contract, impact analysis, or test plan when available, but verify it against the repository. Never claim that an unexecuted test passed.

Render all eight Gate statuses and both mandatory traceability tables for every maintained-code change. Keep small-change entries compact, but do not replace them with prose, renamed checks, or a summary table.

## Mandatory Workflow

### Gate 1: Establish the Change Basis

Inspect repository instructions, comparison base, staged, unstaged and untracked changes, affected manifests, CI configuration, and discovered verification commands. Separate unrelated work and pre-existing failures.

**Required output:** comparison base, inspected change scope, repository commands, environment constraints, and unrelated work.

**Pass condition:** the complete intended change is represented in the inspected scope.

### Gate 2: Define the Contract

Classify additions, modifications, deletions, bug fixes, behavior-preserving refactors, contract changes, migrations, and dependency upgrades. State old and new behavior where applicable, including inputs, outputs, preconditions, postconditions, state transitions, side effects, and error modes.

For frontend changes, include user-visible behavior, interaction, presentation, responsive and content behavior, accessibility, client state, and browser-runtime expectations when they are material.

**Required output:** changed contracts with old/new behavior, inputs, outputs, state, side effects, and errors.

**Pass condition:** every semantic change has an explicit observable contract.

### Gate 3: Map Impact and Risk

Trace changed symbols to callers, consumers, dependencies, tests, public contracts, data, external effects, security boundaries, performance, capacity, resources, and observability. Read [impact-analysis.md](references/impact-analysis.md) and record every material impact in the mandatory table:

For frontend changes, also read [frontend-change-verification.md](references/frontend-change-verification.md). Trace direct and transitive component consumers, design-system assets, routes, client state, supported runtime dimensions, and user-visible states. Keep this reference active through the Portfolio and Evaluation Gates.

| Change ID | Changed contract | Affected surface | Repository evidence | Failure mode | Risk |
|---|---|---|---|---|---|

Assign a stable Risk ID and level in the `Risk` cell for each distinct failure mode. Split impacts that require different evidence.

**Required output:** callers, consumers, boundaries, failure modes, repository evidence, and calibrated risk levels.

**Pass condition:** every changed contract has an impact record, and every material failure mode has a Risk ID.

### Gate 4: Design the Test Portfolio

Select the cheapest stable boundary capable of exposing each failure mode. Read [test-method-selection.md](references/test-method-selection.md) and maintain the mandatory table:

| Risk ID | Boundary | Method | Cases | Oracle | Evidence | Status |
|---|---|---|---|---|---|---|

Define a discriminating oracle for every planned case. Do not mechanically require every test type; make the portfolio proportionate to risk.

For frontend risks, select evidence by failure mechanism. DOM tests do not prove layout, screenshots do not prove behavior, and end-to-end tests do not replace focused component or integration evidence.

**Required output:** risk-to-test mapping with boundary, method, cases, oracle, expected evidence, and status.

**Pass condition:** every material Risk ID has an evidence plan or a specific `NO-TEST-RATIONALE`.

### Gate 5: Prove the Baseline

For a reproducible bug fix, require observed red-to-green evidence.

When direct RED execution is unavailable, require the strongest available alternative: prior failure evidence, comparison-base execution, mutation, fault injection, differential testing, or a mechanism-level regression proof.

Record the missing RED observation as residual uncertainty. For behavior-preserving refactors, establish characterization or differential evidence before restructuring. For deletions, prove consumer migration and the intended absence, compatibility, or rejection behavior.

**Required output:** observed RED, characterization baseline, or strongest available mechanism-level alternative, plus any missing direct observation.

**Pass condition:** the selected evidence can expose the target failure mechanism, and missing RED evidence is recorded as residual uncertainty.

### Gate 6: Execute Required Evidence

Execute the risk-proportionate portfolio using repository-discovered commands. Include targeted, affected, cross-boundary, static, build, and full-suite checks only where required by the impact map or repository policy. Record collection and execution counts; do not hide skips, deselections, flaky retries, or environment failures.

**Required output:** exact commands, collected count, executed count, passed, failed, skipped, and observed result.

**Pass condition:** all required evidence was actually executed, or the affected Risk ID is marked `BLOCKED` with the exact reason.

### Gate 7: Evaluate Sufficiency

Check oracle strength, changed-line and branch coverage where supported, affected consumers, cross-boundary behavior, error paths, performance or security evidence, and all unexplained skips or gaps. Honor repository coverage gates without inventing a universal percentage.

For frontend impacts, evaluate the selected state and runtime matrix, visual and interaction evidence, accessibility, console or hydration failures, content stress, and any untested browser, viewport, theme, locale, or input-mode uncertainty.

Coverage proves execution, not assertion effectiveness. Ask whether reintroducing each plausible defect would fail the selected test.

**Required output:** coverage gaps, oracle assessment, cross-boundary evidence, unexplained omissions, and residual uncertainty.

**Pass condition:** no material coverage, oracle, consumer, boundary, or failure-path gap remains unexplained.

### Gate 8: Close the Handoff

Use [evidence-report-template.md](references/evidence-report-template.md). Assign every Risk ID exactly one final status and distinguish executed evidence from static analysis or recommended commands.

Before the final response, render the eight Gate rows with their exact names, the Change Impact table, and the Test Portfolio table. Preserve Risk IDs across both tables.

**Required output:** exact Gate status table, both mandatory traceability tables, Risk ID status, executed evidence, unresolved test gaps, and residual risk.

**Pass condition:** all eight Gate rows and both traceability tables are present; every material impact is `VERIFIED`, has an accepted `NO-TEST-RATIONALE`, or is explicitly `BLOCKED`; no High/Critical risk remains `BLOCKED` when declaring verification sufficient.

Never describe testing as absolutely complete. Bound the claim to the inspected change, discovered impact map, executed environment, and observed evidence.

Final judgment: there is no known impact left undiscovered and no testing gap left unexplained.
