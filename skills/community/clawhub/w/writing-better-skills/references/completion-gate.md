# Completion Gate

A skill is not complete just because it looks organized.

## Minimum completion standard

Before claiming a skill is complete, verify:

- the description says when to use the skill
- the global skill does not contain project-specific commands, paths, or constraints
- `SKILL.md` routes the agent to `project.skill.md` early when local context matters
- references are named clearly and linked from `SKILL.md`
- shipped scripts are justified
- shipped scripts are tested or explicitly exempted with a reason
- self-healing is narrow and safe
- a fresh agent could use the skill without guessing critical facts

## Completion claim rule

Do not claim a skill is complete based on structure alone.

Completion requires both:
1. structural coherence
2. fresh-agent usability

## Stronger standard for operational skills

If the skill ships scripts, completion should also include:
- passing script tests
- clear validation instructions
- clear routing to the correct script

## Stronger standard for resilient skills

If the skill ships self-healing, completion should also include:
- a clearly documented safe trigger condition
- a rerun step after healing
- a stop condition when healing does not resolve the issue
