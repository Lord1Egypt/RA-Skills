# Team Conventions

Review checklist for layer 3 (Conventions). Ships with common defaults — customize for your team.

## Commit Format

- Follows a consistent format (Conventional Commits, Gitmoji, or team standard)
- Subject line is imperative, under 72 characters
- Body explains *why*, not *what* (the diff shows what)
- References issue/ticket numbers where applicable

## Branch Naming

- Lowercase with hyphens (no spaces, underscores, or mixed case)
- Includes ticket/issue reference when applicable
- Descriptive enough to understand the purpose

## PR Requirements

- Title clearly describes the change
- Description includes context — why the change was made
- Links to related issues or tickets
- Breaking changes are called out explicitly

## Code Style

- Consistent with the existing codebase
- No commented-out code committed (use version control instead)
- No debug logging left in (console.log, print, debugger)
- Imports are organized (stdlib → external → internal)

## Naming

- Variables and functions are descriptive (not `x`, `temp`, `foo`)
- Boolean variables read as questions (`isEnabled`, `hasAccess`, not `flag`)
- Constants are UPPER_SNAKE_CASE (or team convention)
- File names match the primary export

## Customize

Replace or extend the sections above with your team's specific standards.
Delete sections that don't apply.
