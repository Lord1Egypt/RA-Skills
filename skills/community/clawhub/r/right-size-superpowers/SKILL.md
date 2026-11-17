---
name: right-size-superpowers
description: Use when the user explicitly wants Superpowers workflow depth calibrated to task scope and risk, especially when routine or bounded work is receiving heavyweight process.
---

# Right-Size Superpowers

Preserve correctness while scaling Superpowers process to what can materially change the result. The user's requested outcome and constraints remain authoritative.

## Choose the Smallest Sufficient Route

| Route | Observable condition | Response |
|---|---|---|
| Direct | Outcome is clear, scope is bounded, action is reversible or read-only, and no material design choice is unresolved | Act immediately |
| Focused | Root cause is unknown, several related files are involved, or regression risk is meaningful | Use only the one discipline needed to resolve that risk |
| Full | Architecture, public interfaces, persistent data, security, destructive actions, or materially ambiguous product behavior are involved | Explain the trigger and use the appropriate deeper workflow |

For Direct and Focused work, do not automatically chain brainstorming, writing-plans, worktrees, TDD, subagents, or review workflows merely because code is involved. Domain-specific skills required for the artifact or tool still apply.

## Execution Contract

1. Infer routine details from the request and existing project conventions.
2. Inspect only the context needed to identify the target and avoid collateral changes.
3. Make the smallest coherent change that completes the request.
4. Verify with the closest existing check or targeted test once. Broaden verification only after a failure, a cross-cutting change, or evidence of wider risk.
5. Add a regression test when it can catch a meaningful behavior failure. Do not add tests that merely mirror a reversible configuration, copy, wording, or formatting change.
6. Review the resulting diff for scope, accidental edits, and unmet requirements.
7. Report the outcome, changed files, verification performed, and any unresolved risk concisely.

Ask one focused question only when its answer would materially change the result. Do not request another approval for reversible work already authorized by the user.

## Example

Request: “Rename this setting and update its two references.”

Use Direct: locate the definition and references, make the rename, run the nearest relevant check, inspect the diff, and report completion. Do not create a design document, implementation plan, new worktree, subagent review, or unrelated test suite.

## Red Flags

- Treating every code change as architectural work
- Producing a plan artifact for a mechanical edit
- Re-running unchanged checks without new evidence
- Loading unrelated process skills “just in case”
- Asking for approval after the user already authorized a reversible action

If one appears, return to the smallest sufficient route.
