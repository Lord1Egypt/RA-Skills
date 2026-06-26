# Implementation Mapping

Use this file to map a terminal interaction design to a realistic stack.
These are starting points, not guaranteed final answers. Verify framework capabilities with official docs when the design depends on specific widgets, lifecycle behavior, async support, or version-sensitive APIs.

## Selection Heuristic

Start from the interaction shape:

- command-first CLI: parser + styled output is usually enough
- semi-interactive CLI: prompt or form libraries fit best
- full TUI: event loop + layout + widgets + styling are usually required

Prefer the smallest stack that can support the target flow.

## Go

- **Command-first CLI**: `cobra`, `urfave/cli`, or similar parsers plus plain text or styled output
- **Semi-interactive CLI**: prompt libraries or simple interactive flows; verify current prompt libraries if advanced validation is needed
- **Full TUI**: `bubbletea` for the event loop, `bubbles` for reusable widgets, `lipgloss` for styling, `huh` for forms

Use Go when you want a single static binary, good terminal performance, and a clean split between model, update, and view logic.

## Python

- **Command-first CLI**: `typer` or `click`
- **Styled output and rich text**: `rich`
- **Semi-interactive CLI**: `prompt_toolkit`, `questionary`, or a similar prompt layer
- **Full TUI**: `textual` when you want a batteries-included app model

Use Python when iteration speed matters and the environment can support a Python runtime.

## Node.js / TypeScript

- **Command-first CLI**: `commander`, `yargs`, or similar
- **Semi-interactive CLI**: `enquirer`, `prompts`, `clack`, or equivalent prompt flows
- **Full TUI**: `ink` or `blessed`-style ecosystems depending on the rendering model you want

Use this stack when the surrounding tooling is already JavaScript-heavy or when the CLI integrates with a JS-based platform.

## Rust

- **Command-first CLI**: `clap`
- **Styled output**: terminal styling crates as needed
- **Full TUI**: `ratatui` plus terminal backends such as `crossterm`

Use Rust when you want a native binary, strong type safety, and explicit control over rendering and state.

## Implementation Advice

For any stack, define these boundaries before coding:

1. input and event handling
2. state model
3. rendering layer or view functions
4. domain actions and side effects
5. error and notification strategy

Keep framework-specific code thin. Put business rules outside the rendering layer so the interaction can evolve without rewriting the core logic.

## Required Verification Cases

Before recommending a stack as final, confirm:

- the framework supports the target interaction pattern
- key widgets or equivalents exist
- resize behavior can be handled
- async or long-running tasks can report progress cleanly
- the development model fits the user's language and deployment constraints
