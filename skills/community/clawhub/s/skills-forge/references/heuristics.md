# Detection Heuristics

Use these signals when deciding whether a missing capability deserves a skill.

## Strong signals

- the same user request appears three or more times
- the same task requires the same manual structure each time
- the same failure pattern keeps returning
- the same output format is repeatedly requested
- multiple agents would benefit from the same reusable guidance

## Weak signals

- a one-off niche request
- a task that is mostly raw reasoning with no repeatable structure
- a task that should be solved by better routing, not a new skill

## Good candidates

- PRD drafting
- paper reading
- citation formatting
- recurring data export workflows
- a stable API integration

## Bad candidates

- one private project quirk with no reuse
- a personality preference
- broad vague goals like "be smarter"

