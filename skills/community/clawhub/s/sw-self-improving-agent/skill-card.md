## Description:

Build agents that learn from user corrections by updating and following dated rules to improve performance and reduce repeated mistakes over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amdf01-debug](https://clawhub.ai/user/amdf01-debug)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to add a correction loop that records recurring user feedback as dated operating rules. It is intended for agents that should reduce repeated mistakes across future sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill encourages long-term storage of user corrections as agent rules without enough built-in consent, scoping, or review controls.

Mitigation: Use it only where persistent agent memory is intended, require explicit approval before writing or updating RULES.md, and keep changes reviewable and reversible.

Risk: Stored rules could capture sensitive names, client details, secrets, or security instructions.

Mitigation: Avoid storing sensitive details and review new rules before they become part of the agent's operating guidance.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/amdf01-debug/skills/sw-self-improving-agent)
- [Source skill artifact](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with example RULES.md and AGENTS.md sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces dated operating-rule guidance; no executable code is included.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
