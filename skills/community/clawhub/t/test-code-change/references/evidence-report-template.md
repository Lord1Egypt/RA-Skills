# Change Test Evidence

Use this template for every maintained-code implementation or review. Keep small-change entries compact, but retain enough evidence to audit every Gate and Risk ID.

## Contents

- [Gate Status](#gate-status)
- [Change Basis](#change-basis)
- [Observable Contracts](#observable-contracts)
- [Change Impact Traceability](#change-impact-traceability)
- [Test Portfolio Traceability](#test-portfolio-traceability)
- [Baseline Evidence](#baseline-evidence)
- [Execution Result](#execution-result)
- [Coverage and Oracle Quality](#coverage-and-oracle-quality)
- [Cross-Boundary and Non-Functional Evidence](#cross-boundary-and-non-functional-evidence)
- [Frontend Verification](#frontend-verification)
- [Residual Risk](#residual-risk)
- [Handoff](#handoff)

## Gate Status

| Gate | Status | Evidence or blocking reason |
|---|---|---|
| Change Basis |  |  |
| Contract |  |  |
| Impact |  |  |
| Portfolio |  |  |
| Baseline |  |  |
| Execution |  |  |
| Evaluation |  |  |
| Handoff |  |  |

Use `PASS` only when the Gate pass condition is met. Otherwise use `BLOCKED`.

## Change Basis

- **Request and acceptance criteria:**
- **Comparison base and inspected scope:**
- **Staged, unstaged, and untracked changes:**
- **Repository commands:**
- **Environment constraints:**
- **Pre-existing failures or unrelated work:**

## Observable Contracts

| Change ID | Old behavior | New behavior | Inputs/outputs/state | Side effects | Error modes |
|---|---|---|---|---|---|

## Change Impact Traceability

| Change ID | Changed contract | Affected surface | Repository evidence | Failure mode | Risk |
|---|---|---|---|---|---|

Assign a stable Risk ID and level in every material `Risk` cell.

## Test Portfolio Traceability

| Risk ID | Boundary | Method | Cases | Oracle | Evidence | Status |
|---|---|---|---|---|---|---|

Every Risk ID must end as exactly one of:

- `VERIFIED`
- `NO-TEST-RATIONALE`
- `BLOCKED`

Do not declare sufficient verification while a Risk ID has no final status or any High/Critical risk is `BLOCKED`.

## Baseline Evidence

- **Observed RED and GREEN:**
- **Characterization or comparison-base evidence:**
- **Alternative mechanism proof:** prior failure / mutation / fault injection / differential / other
- **Missing direct RED observation and residual uncertainty:**

Use the strongest available baseline evidence. Do not write `N/A` without explaining why direct evidence is unavailable.

## Execution Result

| Command | Collected | Executed | Passed | Failed | Skipped | What it proves |
|---|---|---|---|---|---|---|

Record deselected cases, retries, flakes, timeouts, and environment failures. Never report a recommended or unexecuted command as passing evidence.

## Coverage and Oracle Quality

- **Repository coverage gate:**
- **Changed executable lines and branches:**
- **Material uncovered changes and rationale:**
- **Would plausible defect reintroduction fail the test?:**
- **Mutation, differential, property, fault, performance, or security evidence:**
- **Unexplained skips or oracle concerns:**

## Cross-Boundary and Non-Functional Evidence

- **Consumers, contracts, data, and external IO:**
- **Errors, timeout, retry, idempotency, concurrency, and cleanup:**
- **Latency, throughput, capacity, and resource use:**
- **Authorization, abuse resistance, and sensitive-data checks:**
- **Logs, metrics, traces, and alerts:**

Use `Not impacted` only after the Impact Gate has evidence for excluding the surface.

## Frontend Verification

Complete this section only when frontend behavior, presentation, accessibility, client state, or browser runtime is materially affected.

- **Changed pages, components, tokens, routes, and transitive consumers:**
- **User-visible states and data conditions:**
- **Viewports, content boundaries, themes, locales, browsers, and input modes selected:**
- **Behavior, interaction, visual, and accessibility oracles:**
- **Console, network, SSR, hydration, and chunk-loading observations:**
- **Performance, rollout, client monitoring, and rollback controls:**
- **Untested dimensions and why they are not material or remain uncertain:**

| Surface or consumer | State and data | Viewport or runtime | Method and oracle | Executed evidence | Result |
|---|---|---|---|---|---|

Do not fill the matrix with every possible combination. Include representative boundaries, interacting dimensions, critical journeys, and historical failures selected from the impact analysis. A screenshot without an authoritative expected result is an observation, not a visual-regression oracle.

## Residual Risk

| Risk ID | Inherent level | Executed evidence or control | Residual level | Downgrade evidence | Remaining uncertainty |
|---|---|---|---|---|---|

Never lower the Impact dimension because tests pass. Cite concrete executed evidence for every residual-risk downgrade.

## Handoff

Summarize:

1. inspected change and discovered impacts
2. final status for every Risk ID
3. exact evidence executed and what it proves
4. unresolved test gaps and blocking reasons
5. residual risk and missing environments

Bound the conclusion to the inspected change, discovered impact map, executed environment, and observed evidence.

Final judgment: there is no known impact left undiscovered and no testing gap left unexplained.
