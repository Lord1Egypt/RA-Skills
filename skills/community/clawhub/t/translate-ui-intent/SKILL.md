---
name: translate-ui-intent
description: "Translate vague product and visual intent into repository-consistent, implementation-ready frontend decisions and visually verified UI changes. Use when creating, adding, modifying, or reviewing pages, components, flows, dashboards, forms, or responsive interfaces; when a user describes the desired experience with subjective language such as simple, premium, compact, modern, or 'not like an admin panel'; or when an existing product should reuse its design system, components, interaction patterns, and visual style instead of inventing new ones."
---

# Translate UI Intent

Act as a senior product designer, frontend engineer, and visual reviewer. Turn the
user's rough mental model into explicit decisions that another coding agent can
implement without guessing material behavior or visual direction.

Do not make CSS vocabulary a prerequisite. Speak in product and visual outcomes
first, then name the frontend concept or implementation lever when it helps the
user give better feedback.

## Core Principles

1. Treat the repository as the first design reference for an existing product.
2. Ask only about material decisions that cannot be recovered from repository
   evidence or the user's request.
3. Distinguish user-confirmed intent, repository-derived inference, agent
   proposals, and unresolved questions.
4. Prefer semantic reuse over visual imitation. Extend the current system before
   creating a parallel one.
5. Scale the process to uncertainty. A small, well-specified change should not
   become a design workshop.
6. Validate important visual claims by rendering the interface. Code inspection
   alone does not prove appearance.

Use this decision precedence when constraints conflict:

1. explicit product behavior, user intent, and accessibility requirements
2. repository instructions and the active design system
3. current analogous product patterns
4. agent design judgment

Surface any deliberate conflict instead of silently choosing.

## Select the Working Mode

- **Existing-product mode:** Use by default when the repository contains a
  frontend or supplied product artifacts. Inherit its active design language.
- **Greenfield mode:** Use only when no applicable design system, component
  library, analogous screen, or product artifact exists. Greenfield means the
  product language is undecided, not that the agent may silently invent it.
- **Brief-only delivery:** Produce a build-ready UI Intent Contract when the user
  asks for a prompt, specification, or design direction rather than code.
- **Build delivery:** Continue through implementation and visual verification
  when the user asks to create or change the interface.

Do not ask the user to choose a mode when the request and repository make it
obvious.

## Enforce the Greenfield Ambiguity Gate

Before selecting a greenfield page architecture, establish enough of the
product model to distinguish valid directions:

- primary user and writing or work context
- primary job and content shape
- primary action and the role AI plays in the workflow

When missing answers could change navigation, page regions, persistent
controls, or the core interaction, the next response must stop after:

1. stating the limited repository or artifact evidence
2. asking one to three concrete, high-information questions
3. optionally illustrating the choices with brief `PROPOSED` hypotheses

Do not recommend a final direction, provide an implementation-ready layout, or
invent exact dimensions, colors, fonts, motion, or interaction flows until this
gate is satisfied. A user asking to "explore directions" permits alternatives,
not an unconfirmed final recommendation.

## Use the Pattern-Following Fast Path

Use a direct reuse path when the repository contains an active screen or
component with the same user task and interaction semantics, and the requested
change does not require a new hierarchy or workflow:

1. cite the closest maintained screen, component, and token evidence
2. reuse its shell, layout, control variants, feedback states, and responsive
   behavior
3. identify only the new business data, action, state, or permission difference
4. ask about that difference only when it is materially ambiguous
5. implement and visually compare the result with the inherited pattern

Verify that any route, action flow, permission rule, or state transition called
"existing" actually exists. Visual reuse does not prove business behavior.
Mark missing behavioral evidence `OPEN` instead of inventing an integration.

Do not offer alternate visual directions or produce a large design brief on
this path. Use a compact UI Intent Contract containing the inherited pattern,
the business delta, and observable acceptance criteria.

Leave the fast path when the existing pattern is semantically wrong,
inaccessible, deprecated, unable to express a confirmed requirement, or when
the user explicitly wants to change the product experience. Record the reason
before proposing a new pattern.

## Workflow

### 1. Recover the Product Context

Inspect repository instructions, frontend manifests, routes, theme and design
tokens, component APIs, icon libraries, stories or examples, tests, and the
closest current screens. Read
[repository-design-discovery.md](references/repository-design-discovery.md) for
the evidence order and reuse analysis.

Identify the active convention rather than copying the first search result or a
legacy outlier. Record a compact evidence map for the parts relevant to the
requested change.

Do not ask the user for colors, spacing, controls, or interaction conventions
that the repository already answers.

### 2. Model the Intent and Uncertainty

Extract the user, job, primary action, information hierarchy, content,
constraints, anti-goals, and desired emotional qualities. Mark each material
decision as:

- `CONFIRMED`: explicitly stated or selected by the user
- `INFERRED`: supported by repository or supplied artifact evidence
- `PROPOSED`: recommended by the agent and not yet confirmed
- `OPEN`: materially ambiguous and unresolved

Read [clarification-strategy.md](references/clarification-strategy.md) when the
request contains consequential ambiguity. Ask one to three high-information
questions at a time. Prefer concrete alternatives with consequences over broad
questions such as "What style do you want?"

Proceed directly when remaining ambiguity is cheap to reverse and local
conventions provide a strong answer.

### 3. Decide What to Reuse

Apply this reuse ladder:

1. reuse an existing pattern or component unchanged
2. compose existing primitives
3. minimally extend an existing component through its public API
4. create a new local component using existing tokens and conventions
5. introduce a new shared primitive, dependency, or visual language

Moving down the ladder requires stronger repository evidence and a clearer
reason. Do not misuse a semantically wrong control merely because it looks
similar. Do not modify a shared component for a local need without tracing its
consumers and compatibility impact.

Record the decision:

| UI need | Repository evidence | Candidate | Decision | Deviation reason |
|---|---|---|---|---|

### 4. Translate Subjective Language

Treat phrases such as "clean," "premium," "more modern," or "less like a
dashboard" as hypotheses, not specifications. Read
[visual-language.md](references/visual-language.md) to translate them into
observable dimensions such as hierarchy, density, rhythm, typography, surface,
color, motion, and interaction.

When more than one materially different interpretation remains:

- present two or three distinct directions
- explain the product and implementation tradeoff of each
- make the options differ in structure or interaction, not only color
- recommend one based on the user's goal and repository evidence
- use a wireframe, rendered variant, or reference screenshot when words are
  unlikely to resolve the difference

Do not begin a broad implementation while a high-cost `OPEN` direction remains.

### 5. Form the UI Intent Contract

Read [ui-intent-contract.md](references/ui-intent-contract.md) and produce a
contract proportionate to the change. It must make the following explicit where
material:

- product goal and primary user task
- information and action hierarchy
- repository patterns and components to reuse
- layout, density, visual, and interaction decisions
- loading, empty, error, disabled, permission, and success states
- responsive and content-stress behavior
- accessibility expectations
- deliberate deviations from the current product
- observable acceptance criteria and remaining uncertainty

A different coding agent should be able to implement the contract without
guessing any high-impact decision.

### 6. Implement or Hand Off

For build delivery, implement the smallest change that satisfies the contract.
Follow the repository architecture, public component APIs, tokens, icon set,
state patterns, and verification commands.

Do not introduce a new dependency, CSS paradigm, icon family, font, token set, or
component system unless existing options cannot express a confirmed need.
Complete the relevant interaction states and responsive behavior rather than
shipping only the ideal static state.

For brief-only delivery, make the contract directly usable as the next coding
instruction. Use the compact or full contract structure rather than an
unlabeled recommendation. Separate facts from recommendations and leave no
hidden design assumption.

### 7. Verify the Experience

Read [visual-verification.md](references/visual-verification.md). Run
repository-discovered static and behavioral checks, render the changed
interface, and inspect representative viewports and material states.

Compare the result with both the UI Intent Contract and adjacent product
surfaces. Check hierarchy, component semantics, spacing rhythm, typography,
content overflow, responsive transitions, interaction feedback, and
accessibility.

If the interface cannot be rendered, report visual verification as blocked and
do not claim that the implementation matches the intended appearance.

### 8. Iterate and Teach in Context

Convert user feedback into an observable delta before editing again:

> observed mismatch -> intended outcome -> smallest design or code change ->
> fresh evidence

Briefly name useful design or frontend terms after grounding them in the visible
result. Teach through the current decision, not through an unrelated CSS lesson.

## Completion Standard

Finish only when:

- every material intent decision is `CONFIRMED`, evidence-backed `INFERRED`, or
  explicitly `OPEN` with a blocking reason
- reuse choices and deliberate deviations cite repository or supplied-artifact
  evidence
- the contract is implementation-ready at the requested scope
- material states and viewports have rendered evidence, or the missing evidence
  is reported as blocked
- the final explanation separates observed evidence from design judgment

Do not describe a design as "good," "polished," or "consistent" without naming
the evidence and criteria that support the claim.
