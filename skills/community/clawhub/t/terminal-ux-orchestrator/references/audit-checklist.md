# Audit Checklist

Use this checklist when reviewing an existing CLI or TUI.

## 1. Entry and discoverability

- Is the primary action obvious within the first screen or command output?
- Can a new user tell what to do next without reading source code or external docs?
- Are help text, examples, defaults, and required inputs visible at the point of use?

## 2. Interaction fit

- Is the tool using the right mode: command-first CLI, semi-interactive CLI, or full TUI?
- Is a prompt or wizard replacing something that would be clearer as flags and subcommands?
- Is a full-screen TUI being used where a short prompt flow would be enough?

## 3. Navigation and escape

- Are keyboard hints visible when the user needs them?
- Is it obvious how to go back, cancel, quit, or confirm?
- Do destructive actions require explicit confirmation?

## 4. State clarity

Check whether the interface clearly distinguishes:

- idle
- loading
- success
- warning
- error
- empty
- disabled or unavailable actions

## 5. Output readability

- Is the information hierarchy clear at a glance?
- Are spacing, grouping, and labels doing enough work before color or borders are added?
- Does the interface still read well on a narrow terminal?
- Are tables, logs, and long lines wrapped or truncated intentionally?

## 6. Copy quality

- Are prompts and labels short, specific, and action-oriented?
- Do errors explain the problem and the next step?
- Do success messages confirm what changed or what happens next?
- Are terms consistent across commands, prompts, help text, and status lines?

## 7. Feedback loops

- Does the tool acknowledge long-running work quickly?
- Are progress indicators honest and useful?
- Can the user tell whether work is still happening, stalled, or finished?

## 8. Consistency

- Do colors mean the same thing across the interface?
- Are repeated controls presented in the same order and style?
- Do related commands and screens share the same naming and tone?

## 9. Accessibility and resilience

- Is color the only signal for state?
- Does the interface remain usable without mouse support?
- Does resize behavior break layout, clipping, or navigation?
- Are fallback text modes available when richer rendering is not appropriate?

## Audit Output

When you finish the audit, report:

1. the top usability problems
2. why they matter
3. the smallest effective fixes
4. whether the current interaction mode should change
