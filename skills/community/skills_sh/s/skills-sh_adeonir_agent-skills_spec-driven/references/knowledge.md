# Knowledge File Format

Canonical format for `.artifacts/knowledge.md`, owned by the spec-driven
workflow.

## When to Use

- Loaded by `design.md` Step 8 and `implement.md` Step 8 before appending
- Loaded by `quick-mode.md` Step 9 before appending
- Loaded by `design.md` Step 3 before designing, for project-level context

## Ownership

- **Sole writer:** the spec-driven workflow (design, implement, quick-mode)
- No other skill reads or mutates this file

## File Structure

```markdown
## Decisions

Cross-feature decisions with rationale. One bullet per decision.

- {decision} — {rationale}; source: {file:line / ADR / doc}; scope: {context it holds under} <!-- date:YYYY-MM-DD -->

## Gotchas

Traps discovered during design or implementation that would cost time
to rediscover.

- {gotcha} — {context} <!-- date:YYYY-MM-DD -->

## Conventions

Normative patterns the codebase already follows, observed while
implementing — recorded so future features stay consistent with how
this codebase does things. Normative means a standard worth keeping
consistent; descriptive "where things live / how an area works" detail
belongs in the `.artifacts/codebase/{area}.md` cache instead.

- {convention} — {where it applies / why it holds} <!-- date:YYYY-MM-DD -->
```

Always keep all three section headers, even when empty. Writers rely on
the headers existing to locate sections.

## Section Routing

When appending a discovery during design or implement, route by content:

| Content | Destination |
|---------|-------------|
| Project-level decision (why we chose X over Y for the project) | `## Decisions` |
| Runtime constraint, API quirk, workaround, non-obvious trap | `## Gotchas` |
| Normative pattern the codebase follows consistently (how it does X) | `## Conventions` |
| Descriptive area orientation (where things live, how an area works) | Not here — `.artifacts/codebase/{area}` cache |
| Inventory/structural fact (installed package, new route, new module, new directory, new env var) | **Not recorded** — re-derivable from code |
| Forward-looking item (milestone, planned feature, `(TBD)`, feature number) | **Not recorded** — knowledge.md is observable current state only |

Feature-specific details (only relevant to the current feature) do NOT
belong here — they live in the feature's own `design.md` or
`implement.md` artifacts.

Inventory and structural facts are not recorded because they are
re-derivable directly from the code. What belongs here is the
*interpretive* layer the code cannot state on its own: the why behind a
choice, the trap behind a behavior, the convention behind a pattern.

## Guidelines

- Record cross-feature decisions in `## Decisions` with rationale (the
  *why*, not the *what*)
- When a `## Decisions` entry is a project-wide architectural choice (not
  feature-grain), note it as an ADR candidate — promoting it to a formal ADR
  is the user's call; recording it here is a valid resting place either way
- Record gotchas in `## Gotchas` with enough context for a future reader
- Record normative patterns in `## Conventions` with where they apply
- Use ISO date in every row
- Create the file with all three headers if it doesn't exist

## Anti-Pattern: Recording Inventory Facts

Installed packages, new routes, new modules, new directories, and new
env vars are inventory — re-derivable directly from the code. Recording
them duplicates work and turns the file into a changelog. This file is
for interpretive content (why, trap, convention), not what.

## Anti-Pattern: Feature-Scoped Notes in a Cross-Feature File

A detail relevant only to the current feature belongs in that feature's
`design.md` or `implement.md`, not here. knowledge.md carries what
crosses features: durable decisions, traps, and conventions a future
feature would otherwise rediscover.

## Error Handling

- File missing: create with the three empty headers before appending
- Section header missing (partial file): add the missing header before
  appending
- Same item fits two sections (a normative pattern that is also a trap):
  keep it in `## Gotchas` if the cost is in *hitting* it, in
  `## Conventions` if the value is in *following* it
