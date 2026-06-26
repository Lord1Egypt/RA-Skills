---
name: terminal-ux-orchestrator
description: Orchestrate CLI and TUI UX improvement across languages. Use this skill whenever the user wants to audit a terminal interface, redesign a command flow, add or improve prompts, selectors, forms, tables, progress views, result pages, help screens, keyboard hints, or compare terminal interaction directions. Also use it when the request needs an implementable stack recommendation, visible before/after UX evidence, or current-doc verification for framework feasibility. Do not use it for ordinary shell usage, pure flag wiring, or backend logic that does not materially affect terminal interaction.
---

# Terminal UX Orchestrator

Use this skill to turn terminal UX requests into implementable engineering work.
The goal is not to produce abstract design commentary. The goal is to help an agent diagnose the current interaction, recommend a better terminal flow, map it to a realistic implementation stack, and make the improvement legible to the user.

This skill is language-agnostic. Keep the solution inside the user's existing stack unless there is a clear mismatch between the desired interaction and the current toolchain.

## Trigger Boundary

Use this skill when the task is primarily about terminal interaction quality, including:

- CLI or TUI flow redesign
- prompts, confirms, selectors, forms, wizards, step flows
- help screens, onboarding output, result pages, status summaries
- progress feedback, empty states, error states, retry or cancel paths
- keyboard hints, navigation clarity, screen hierarchy, information density
- choosing a terminal framework or validating whether a framework can support a desired pattern
- showing what changed in a terminal UX redesign

Do not use this skill as the main path when the task is mainly:

- ordinary shell usage or shell command explanation
- pure argument parsing or flag plumbing with no meaningful UX question
- backend logic, storage, networking, or APIs unrelated to terminal interaction
- generic code cleanup with no user-facing terminal effect

If the request is mixed, use this skill only for the UX-facing slice and keep the rest scoped to the underlying engineering task.

## Operating Principle

Always optimize for a design another coding agent can implement and verify.
Prefer the smallest interaction model that solves the job:

1. command-first CLI
2. guided or semi-interactive CLI
3. full TUI

Do not recommend a full TUI just because it looks more sophisticated. Most developer tools benefit more from a clearer guided CLI, better result presentation, and stronger state feedback.

## Request Classification

Classify the task before proposing changes. A single request may combine several modes.

1. **Audit**: review an existing CLI or TUI and identify the highest-impact UX issues.
2. **Design**: define a new terminal interaction model, states, layout, and copy.
3. **Implementation mapping**: translate an agreed design into frameworks, modules, and state boundaries.
4. **Feasibility verification**: check whether a library or framework can actually support the required interaction.
5. **Change visibility**: make the before/after effect easy to perceive.
6. **Validation**: define or execute checks that show the redesign works.

If several modes are present, use this sequence:

1. summarize the goal or current pain
2. diagnose the interaction problem or define the design target
3. recommend the interaction model
4. map it to implementation
5. verify unstable assumptions when needed
6. show the visible difference
7. close with validation

## Workflow

### 1. Choose the interaction shape

Pick one primary interaction class:

- **Command-first CLI**: subcommands, flags, static output, low ceremony
- **Guided CLI**: prompts, confirmations, selectors, short wizards, structured summaries
- **Full TUI**: persistent state, keyboard navigation, panels, continuous redraw

If the current design mixes modes poorly, say so and recommend a cleaner primary shape.

### 2. Diagnose the real UX problem

Use `references/audit-checklist.md` to inspect the current or proposed experience.

Prioritize:

- discoverability of primary actions
- clarity of current state and next step
- handling of loading, success, empty, error, and cancel states
- consistency of copy, semantic styling, and keyboard hints
- terminal-appropriate density and hierarchy
- match between task complexity and interaction complexity

When auditing an existing tool, lead with the 3-7 issues that most affect usability.

### 3. Design the improved flow

Use `references/design-principles.md` and `references/interaction-patterns.md`.

For every recommendation, define:

- the interaction shape
- the major steps, screens, or result sections
- the critical states
- prompt, hint, error, and success copy strategy
- entry, retry, back, cancel, and exit behavior

Prefer clarity, momentum, and recovery over decoration.

### 4. Map the design to implementation

Use `references/implementation-mapping.md`.

Always explain:

- why the chosen stack fits the interaction shape
- which library or module handles parsing, prompting, layout, styling, and feedback
- what should become reusable presentation components
- where state lives and how events or navigation should be handled

If the user already chose a language, stay inside that constraint unless it is clearly unsuitable.

### 5. Verify feasibility when details may have changed

Do not assume framework capabilities are timeless.

Actively verify with official docs or current high-trust sources when:

- the user asks for the latest, current, or best-supported option
- a design depends on version-sensitive APIs, widgets, or lifecycle behavior
- you are not sure a library supports a required interaction
- terminal compatibility, async behavior, mouse support, or resize behavior matter
- you are comparing several frameworks or libraries

Prefer these sources in order:

1. official documentation
2. official repositories and examples
3. release notes or migration guides
4. high-quality community references

Separate clearly in the answer:

- stable design guidance
- verified conclusions
- assumptions or open risks

### 6. Make the UX delta visible

Use `references/change-visibility.md`.

Never stop at "this should feel better."
Choose the lightest artifact that makes the improvement obvious:

- concise before/after summary
- before/after help or result-page structure
- flow comparison
- visual mockup when the environment supports it
- validation-backed summary of the newly clarified states

### 7. Validate the outcome

Close with a small validation plan or the checks you ran.

Validate at least:

- the main happy path
- one failure or invalid-input path
- one empty, no-result, or skip path when relevant
- cancel, quit, or destructive confirmation when relevant
- narrow terminal or fallback behavior when relevant

## Optional Environment Amplifiers

This skill should work even in a plain text environment.
If extra capabilities are available, use them only when they materially improve the result:

- **Current web or docs access**: verify framework support, version-sensitive APIs, and current best practices
- **Visual comparison tools**: show competing terminal directions or before/after layouts when text would be ambiguous
- **Planning or execution helpers**: break a large multi-command redesign into implementation steps

If these capabilities are unavailable, degrade gracefully:

- provide a text-first comparison
- state what remains assumed
- call out any feasibility checks the implementing agent should run next

Do not make this skill depend on another skill being present.

## Output Contract

Default to this structure unless the user asks for something else:

### 1. Goal or current-state summary

State the target flow or the main UX problem in 2-4 lines.

### 2. Key diagnosis or design goals

List the high-impact problems or the design goals that drive the solution.

### 3. Recommended terminal design

Describe the interaction model, flow, major states, and presentation choices.

### 4. Implementation path

Provide:

- primary stack recommendation
- fallback option when relevant
- module or component breakdown
- state and event-handling guidance

### 5. Feasibility and evidence

State:

- what is verified
- what is inferred
- what still needs checking

### 6. Visible impact

Show how the user should perceive the change.

### 7. Validation

Give a compact verification plan or summarize the checks already run.

## Constraints

- Do not give purely aesthetic advice with no implementation path.
- Do not over-engineer a full TUI when a guided CLI is enough.
- Do not overload the terminal with borders, color, or dense tables if simpler output is clearer.
- Do not hide uncertainty when framework capability is unclear.
- Do not claim UX improvement without showing what changed.
- Do not let framework selection override the user's deployment constraints without justification.

## References

- `references/audit-checklist.md`: audit questions for current terminal UX quality
- `references/design-principles.md`: hierarchy, density, semantics, and feedback guidance
- `references/interaction-patterns.md`: common terminal interaction patterns and when to use them
- `references/implementation-mapping.md`: cross-language stack mapping and selection heuristics
- `references/change-visibility.md`: ways to make the before/after effect obvious
- `references/tool-coordination.md`: when to use optional verification, visualization, or planning support
