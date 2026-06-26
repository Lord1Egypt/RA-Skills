# Local Overrides Example

Skill Router should support local preference overrides without treating them as universal defaults.

Examples of local preference:
- prefer `pinchtab-browser` over another browser-control skill in this workspace
- prefer `github` over more general repo skills for GitHub tasks
- prefer `distill` when the user says "record this" or "write down the lesson"

## Rule

Public routing logic should remain capability-based.
Local preferences should only tune tie-breaking and default choice within the same capability.

## Practical use

A local environment can maintain a small override note such as:
- browser-control → prefer `pinchtab-browser`
- github-workflow → prefer `github`
- skill-vetting → prefer `skill-vetter`

These are preferences, not hard assumptions about every user's install set.
