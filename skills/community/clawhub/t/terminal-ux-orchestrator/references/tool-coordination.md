# Tool Coordination

Use this file to decide when `terminal-ux-orchestrator` should stay self-contained and when it should coordinate with optional capabilities.

## Core Rule

Use the lightest useful coordination path.
Do not pull in extra tools or skills unless they materially improve understanding, feasibility, or validation.

## When to Stay Inside terminal-ux-orchestrator

Stay self-contained when the task is mainly:

- auditing an existing CLI or TUI
- proposing a better interaction structure
- mapping a design to a concrete stack
- giving a concise before/after explanation
- defining validation steps

## When to Use Optional Visualization

Use a browser or other visual-comparison tool when:

- the user should compare two or more interface directions
- a wizard, results page, or state layout is easier to understand visually
- the user needs a mockup to judge hierarchy or flow
- a before/after visual comparison would reduce ambiguity

If no such tool exists, provide a compact text-based comparison instead.

## When to Use Current Web Verification

Use web or official-doc verification when:

- framework capability is uncertain
- the user asks for the latest best practice
- library APIs, widgets, or support matrix may have changed
- you are comparing frameworks for suitability
- terminal compatibility or async behavior could affect the design

Prefer:

1. official docs
2. official repositories and examples
3. release notes
4. strong community references

## When to Suggest a Planning Step

If the UX improvement is large enough to touch multiple commands, shared rendering helpers, state models, or command families, suggest a written plan before implementation.

Typical triggers:

- redesigning multiple command outputs for a unified visual language
- changing both interactive flows and non-interactive results pages
- introducing a new shared presentation layer
- refactoring multiple commands to follow one UX contract

## When to Emphasize Validation

Validation becomes mandatory when:

- code has already been changed
- the user asks whether the redesign is effective
- the change affects destructive actions, lock handling, or recovery flows
- fallback behavior and terminal constraints matter

Validation should focus on user-visible outcomes, not only implementation correctness.
