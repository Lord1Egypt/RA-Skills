# Skill Quality Rubric

Score each category from 1 to 5.

## Trigger clarity

- Can another agent tell exactly when to use the skill?
- Does the frontmatter `description` include both capability and concrete trigger contexts?

## Reusability

- Will this skill be useful across multiple tasks or sessions?

## Structure fit

- Does it need only `SKILL.md`, or should it also ship scripts or references?
- Is `SKILL.md` lean enough to load often, with detailed variants moved into `references/`?
- Are bundled references linked directly from `SKILL.md` with clear read-when guidance?

## Execution fit

- Does the skill set the right degree of freedom?
- High freedom fits judgment-heavy workflows where many approaches are valid.
- Medium freedom fits repeatable patterns with configurable details.
- Low freedom fits fragile operations that need scripts, validation, dry-runs, and exact sequencing.

## Practicality

- Does it remove repeated work or reduce mistakes?

## Safety

- Would automatic installation be risky?
- Does it touch credentials, destructive actions, or self-modification?
- Does the package avoid user-facing docs such as `README.md`, `CHANGELOG.md`, or setup guides that do not help the agent execute the task?

## Install recommendation

- `20+`: strong candidate
- `15-19`: keep as draft, test more
- `<15`: do not productize yet
