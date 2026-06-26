---
name: taku-think
description: >
  Clarify ambiguous development requests, new feature ideas, product/design choices,
  and idea-stage work before planning. Three adaptive modes: Quick (small clear
  changes -> fast alignment), Design (feature requests -> architecture + DESIGN.md),
  Explore (new ideas -> forcing questions before committing). Triggers on "add a
  feature", "I have an idea", "should we build", "let's design", "设计一下",
  "需求分析", "我有个想法", or when the user describes a desired end state but
  implementation choices or success criteria are not yet settled. Also handles
  design system creation. Bug fixes and refactors use `/taku-debug` or
  `/taku-review` directly unless they need fresh design decisions.
---

# Taku Think - Minimum Necessary Design

Think prevents wrong work from starting. It should be as short as the task
allows and as explicit as the risk requires.

Rule labels: `[IRON LAW]` means a non-negotiable correctness constraint. `[GUIDANCE]` means a strong default that may adapt when context justifies it.

[IRON LAW] No implementation until the selected design path is visible and the
user approves it.

## Mode Selection

Choose by request maturity, not keywords.

- **Quick:** one clear change, obvious implementation location, no architecture
  decision, success criteria are already stated or strongly implied.
- **Design:** normal feature work where data model, integration points,
  component structure, or behavior boundaries are open.
- **Explore:** idea-stage work where success criteria are unknown or the real
  question is whether/what to build.

When in doubt, use Design. Quick should feel obviously safe.

## Quick Mode

Use Quick when heavy artifacts would be wasteful.

1. Ask one alignment question:

   ```text
   I understand this as: [change], touching [files/areas], verified by [check].
   Is that right?
   ```

2. If corrected, restate once.
3. Present a chat-visible mini design:

   ```text
   MINI DESIGN
   - Change:
   - Why:
   - Touch points:
   - Risk:
   - Done when:
   ```

4. After approval, route directly to `/taku-build` for a single obvious change,
   or `/taku-plan` when task breakdown matters.

Do not create `DESIGN.md` or `PLAN.md` just to satisfy process for tiny tasks.
The mini design is enough when it contains scope, risk, and verification.

## Design Mode

Use Design when implementation choices matter.

Before proposing a design:

- read the directly relevant project docs/config/files
- inspect nearby patterns
- ask at most two clarifying questions, one at a time
- skip questions already answered by the user

Present 2-3 distinct approaches:

- one minimal viable path
- one stronger long-term architecture
- one lateral option only if it is genuinely different

Recommend one and explain the tradeoff. After the user chooses, write
`DESIGN.md` using `references/design-doc.md` as the local scaffold.

Design depth scales to risk:

- **Lightweight:** problem, approach, touch points, risks, done when.
- **Standard/Deep:** add architecture, data flow, error handling, testing
  strategy, and open questions.

Before asking for approval, remove placeholders such as TBD, TODO, "appropriate",
or "handle later." A design with placeholders is not a contract.

## Explore Mode

Use Explore when the request is not ready to become a build contract.

Ask the smallest set of forcing questions needed to identify whether there is a
real task:

- What evidence shows this is needed?
- Who is the first user or maintainer affected?
- What is the smallest useful version?
- What happens if we do nothing?
- What existing code or workflow already solves part of it?

If the user asks to proceed despite unanswered questions, ask the two most
important remaining questions, then respect the answer.

Record useful exploration notes in `.taku/explore-{date}.md` only when the
session produces decisions worth preserving. Otherwise summarize in chat.

## Handoff Contract

Before routing to `/taku-plan` or `/taku-build`, verify:

- approved design or approved mini design exists
- one approach is selected
- success criteria are concrete and testable
- scope boundaries are explicit
- open questions are answered or accepted as known risk

If any item is missing, resolve it before handoff. Plan and Build must not invent
design decisions.

## Scope Guard

If the request contains multiple independent subsystems, split it. Run Think on
the first coherent slice and list what remains out of scope.

## Design System Mode

Only activate for explicit design-system or visual-identity requests. Load
`references/design-system.md` when triggered. Backend, CLI, and API projects skip
this mode.

## Known Pitfalls

**Quick mode used for a non-quick task.** "Add settings" often hides storage,
permissions, audit, migration, and UI decisions.

Prevention: Quick requires one obvious implementation path. If two reasonable
approaches exist, use Design.

**Three fake approaches.** "React", "React with hooks", and "React with hooks
and TypeScript" are not distinct options.

Prevention: present two real options instead of three cosmetic ones.

**Design doc with TBDs.** Build treats TBD as permission to invent behavior.

Prevention: placeholder scan before approval.
