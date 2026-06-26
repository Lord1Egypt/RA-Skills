# Sandbox Testing

Use this reference when evaluating a third-party or unfamiliar skill.

## Goal

Reduce risk before trusting the target skill.

## Workflow

1. Read `SKILL.md` first.
2. Scan scripts, shell commands, and references for side effects.
3. Identify credentials, network access, file writes, or destructive actions.
4. Prefer isolated sessions or disposable workspaces before any deeper execution.
5. Report which claims are based on static inspection versus runtime evidence.

## High-Risk Signals

- `rm`, `git reset`, or destructive shell flows
- External credentials or paid APIs
- Writes outside the target skill directory
- Hidden setup steps not reflected in `SKILL.md`
- Network or browser automation with unclear scope

## Output Guidance

State clearly:

- what was inspected
- what was executed
- what remains unverified
