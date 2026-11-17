# Frontend Change Verification

Use this reference for changes that can affect rendered interfaces, user
interaction, client state, accessibility, responsive behavior, or browser
runtime. Apply the mandatory workflow from the parent Skill; this reference
specializes impact analysis and evidence selection rather than adding a separate
process.

## Contents

- [Start from the Observable System](#start-from-the-observable-system)
- [Define the Frontend Contract](#define-the-frontend-contract)
- [Map the Propagation Graph](#map-the-propagation-graph)
- [Build Falsifiable Failure Models](#build-falsifiable-failure-models)
- [Select the State and Runtime Matrix](#select-the-state-and-runtime-matrix)
- [Choose Evidence by Failure Mechanism](#choose-evidence-by-failure-mechanism)
- [Use Visual Evidence Correctly](#use-visual-evidence-correctly)
- [Assess Oracle Strength](#assess-oracle-strength)
- [Control Residual Production Risk](#control-residual-production-risk)
- [Close Frontend Verification](#close-frontend-verification)

## Start from the Observable System

Treat frontend behavior as a function of interacting inputs:

```text
user outcome =
code x data x client state x permission x network timing
x viewport x browser/runtime x input mode x theme x locale/content
```

The combination space cannot be exhausted. Sufficient verification means every
material failure mechanism has evidence capable of exposing it, while omitted
dimensions have repository evidence or explicit residual uncertainty.

Control risk before testing:

1. minimize the change and reuse current components, tokens, and interaction
   patterns
2. keep styles, state, and APIs inside stable ownership boundaries
3. preserve type, schema, and component contracts
4. verify the affected propagation graph and representative runtime matrix
5. limit exposure with flags, staged rollout, monitoring, and rollback when
   verification cannot reproduce production diversity

## Define the Frontend Contract

Inspect and state only the contracts affected by the change:

| Contract | Observable concerns |
|---|---|
| Business | user outcome, rules, permissions, irreversible actions |
| State | loading, empty, partial, ready, success, error, disabled, denied |
| Interaction | pointer, keyboard, focus, validation, submit, cancel, recovery |
| Presentation | hierarchy, visibility, spacing, typography, color, stacking, overflow |
| Responsive and content | reflow, collapse, scrolling, priority, long or sparse content |
| Integration | API, schema, router, cache, store, analytics, browser storage |
| Accessibility | semantics, name, focus order, non-color cues, contrast, motion |
| Runtime | browser APIs, SSR, hydration, chunks, service worker, supported platforms |
| Non-functional | bundle size, rendering, interaction latency, resource use, privacy |

Do not classify presentation as harmless by default. Hidden actions, occluded
content, broken narrow layouts, or unreadable status information are behavioral
failures when they block or mislead the user.

If an approved design or UI Intent Contract exists, use it as one oracle source
and verify it against repository behavior. Do not require that artifact or
couple this workflow to another Skill.

## Map the Propagation Graph

Trace from every changed frontend asset in four directions:

- **Upward:** importing components, pages, routes, stories, tests, and product
  journeys.
- **Downward:** child components, hooks, tokens, utilities, adapters, data, and
  browser APIs.
- **Lateral:** global CSS, themes, shared stores, caches, router state, portals,
  service workers, analytics, and feature flags.
- **Runtime:** supported states, permissions, viewports, browsers, themes,
  locales, content shapes, input modes, and network conditions.

Classify the source because the same line count has different exposure:

| Changed surface | Typical regression radius |
|---|---|
| Leaf markup or local style | local states, content boundaries, and parent layout |
| Shared component or hook | all consumers, variants, states, semantics, and interactions |
| Token, reset, theme, or global CSS | transitive product-wide presentation and contrast |
| Route, store, cache, or adapter | cross-page state, history, stale data, and recovery |
| API type or serialization | every producer, consumer, and visible data state |
| SSR, hydration, build, or dependency | entry points, chunks, supported runtimes, deployment |

Use repository evidence such as imports, token references, component stories,
route registration, store selectors, browser support, analytics events, and
existing regression suites. Do not infer a small blast radius from a small diff.

Build the affected regression scope as:

```text
direct changed behavior
union transitive consumers
union shared/global presentation matrix
union affected cross-boundary journeys
union repository-required checks
```

## Build Falsifiable Failure Models

Write one concrete statement for each materially different failure mechanism:

> Because of **specific frontend change**, **specific user-visible or runtime
> failure** may occur for **specific consumer, state, or environment**, supported
> by **repository evidence**.

Probe these common mechanisms only when applicable:

| Change shape | Plausible failures |
|---|---|
| Shared control | broken variant, focus, label, disabled or loading behavior |
| Layout or CSS | clipping, overlap, wrong stacking, layout shift, unreadable contrast |
| Responsive change | failure below/at/above a breakpoint, touch target or scroll loss |
| Async state | stale result, duplicate action, race, missing rollback or recovery |
| Routing | broken deep link, history, redirect, guard, or preserved state |
| Data contract | loading, empty, partial, malformed, unauthorized, or error rendering |
| SSR or hydration | server/client mismatch, event loss, console error, content flash |
| Dependency or browser API | unsupported runtime, changed default, chunk or polyfill failure |
| Accessibility | wrong semantics, name, focus order, keyboard trap, color-only signal |
| Security or privacy | sensitive rendering, unsafe content, client-only authorization |
| Performance | bundle growth, slow render, interaction latency, retained resources |

Frontend risk is not synonymous with visual risk. Split failure modes that need
different oracles.

## Select the State and Runtime Matrix

Consider these dimensions:

```text
state x role x viewport x content x theme x locale
x browser/runtime x input mode x network timing
```

Do not execute the full Cartesian product. Select:

1. the primary repository-supported scenario
2. below, at, and above material boundaries
3. each dimension that contains the failure mechanism
4. pairwise combinations where dimensions interact
5. critical journeys and historical failures
6. broad consumer samples for shared components or tokens

Examples of useful boundaries include longest supported labels, empty and dense
data, narrow and wide layouts, denied and allowed roles, light and dark themes,
keyboard and pointer input, offline or delayed responses, and supported
server/client rendering modes.

Every omitted material dimension must have a rationale or remain residual
uncertainty. Do not invent browser or device coverage that the repository does
not support.

## Choose Evidence by Failure Mechanism

| Evidence boundary | What it can prove | What it cannot prove alone |
|---|---|---|
| Type, lint, and build | structural contracts, imports, syntax, bundling | runtime behavior or appearance |
| Unit | pure rules and state transitions | framework or browser integration |
| DOM component | semantics, events, state, accessible queries | real layout, CSS, browser APIs |
| Browser component | rendering, focus, CSS, browser-dependent interaction | full application integration |
| Router/API/store integration | cross-module state and controlled failure behavior | production browser diversity |
| Visual regression | approved appearance for selected states and viewports | requests, state transitions, semantics |
| Accessibility automation | machine-detectable semantic and contrast rules | complete keyboard or assistive usability |
| End-to-end | a few critical cross-boundary user outcomes | exhaustive local state and edge coverage |
| Performance or bundle check | measured regression against a controlled baseline | correctness of user behavior |
| Cross-browser differential | supported-runtime compatibility | unrelated state and business correctness |

Prefer the cheapest stable boundary that contains the failure mechanism.

- Exercise actual serialization, routing, browser APIs, focus, CSS, SSR, or
  hydration when those semantics create the risk.
- Use controlled network responses for loading, empty, partial, error, retry,
  stale, optimistic, rollback, duplicate, and out-of-order outcomes.
- Test authorization at the trusted boundary. A hidden button is not a security
  control.
- Reserve end-to-end tests for critical journeys whose failure spans multiple
  owned boundaries.

## Use Visual Evidence Correctly

Use real-browser visual evidence when geometry, visibility, hierarchy, styling,
responsive behavior, themes, or content stress is part of the contract.

A valid visual regression needs:

1. an authoritative expected result
2. deterministic state, data, fonts, animation, clock, and viewport
3. a selected consumer, state, and runtime matrix
4. a comparison method and reviewed difference
5. evidence that the updated baseline represents intended behavior

Do not update a baseline merely to remove a failure. Do not mask dynamic regions
that contain the failure mechanism. Treat a standalone screenshot without an
expected result as observation evidence, not a regression oracle.

Visual evidence does not replace interaction, accessibility, network, or state
assertions. DOM execution does not replace visual evidence when browser layout
is the failure mechanism.

## Assess Oracle Strength

For every frontend risk, ask:

> If the plausible defect were reintroduced, would this exact check fail for
> the affected consumer, state, and runtime?

Strengthen weak evidence that only:

- renders without asserting the expected state
- checks an implementation class instead of user-visible behavior
- snapshots a large tree without a reviewed semantic reason
- captures only the ideal desktop happy path
- mocks away routing, serialization, focus, CSS, timing, or browser semantics
- ignores console, network, hydration, or unhandled rejection failures
- treats screenshot approval as proof of business correctness

Record collection, execution, skips, retries, browser/runtime, viewport, and
state selection. A test discovered but filtered out is not executed evidence.

## Control Residual Production Risk

Some frontend uncertainty cannot be reproduced locally, especially real content,
browser extensions, device constraints, production latency, CDN behavior, and
long-tail browser combinations.

Use proportionate controls:

- feature flags or staged rollout
- client error, console, hydration, and failed-resource monitoring
- Web Vitals or owned interaction measurements
- analytics for critical journey completion and abandonment
- support and accessibility feedback channels
- rapid rollback or kill switches

These controls reduce exposure or detection time; they do not retroactively make
untested behavior verified.

## Close Frontend Verification

Before marking frontend risks verified, confirm:

- changed and transitive consumers are identified
- every material contract and failure mode has a Risk ID
- the selected state and runtime matrix follows repository support and risk
- behavior, visual, accessibility, integration, and performance evidence are
  separated by what each can prove
- browser-dependent mechanisms were exercised in a real browser when required
- console, network, SSR, hydration, and chunk failures were evaluated when
  impacted
- visual baselines were reviewed rather than blindly replaced
- omitted dimensions and production-only uncertainty remain explicit

Sufficient frontend regression means there is no known affected consumer,
failure mechanism, or material runtime dimension left without evidence or an
explained residual gap.
