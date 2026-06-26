# self-improving-prompt Reference Details

## Compare-First Rules

Use compare-first only when one of these is true:

- refinement adds substantial value, or
- the user explicitly asks to compare or refine wording first

Substantial value means the refined prompt adds at least two of:

- clearer goal or success condition
- explicit scope or non-goals
- verification or acceptance criteria
- output format
- resolution of a meaningful ambiguity

If that threshold is not met, do not interrupt with a compare step.

## Interaction Flow

### Preferred flow

1. Show the refined prompt in chat
2. Ask the user to choose refined vs original

Preferred tool:

- `AskUserQuestion`

Fallback:

- plain-text confirmation in chat if `AskUserQuestion` is unavailable or disallowed

Never show a compare choice before showing the refined prompt itself.

## Learning Signal Event Types

Normalized preference events passed forward for later summarization:

| Event | Meaning |
|-------|---------|
| `choose_refined` | User chose the refined version |
| `choose_original` | User chose the original version |
| `explicit_no_compare` | User explicitly said not to compare versions |
| `explicit_compare_first` | User explicitly asked to compare versions first |
| `refine_only_requested` | User wants prompt refinement without execution |

Rules:

- Store labels only, never the full refined prompt
- Do not attach task-specific details
- Treat explicit verbal corrections as stronger than passive event counts
- Do not infer workflow acceptance from the absence of a complaint

## Clarification Question Rules

If critical context is missing:

- ask at most 1 to 2 blocking questions
- if missing info is optional rather than blocking, proceed
- do not ask questions merely to make the process feel thorough
