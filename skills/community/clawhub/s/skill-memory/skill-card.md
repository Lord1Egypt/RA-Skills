## Description:

Skill Memory routes tasks to preferred skills using a self-updating local mapping of task types, parameters, scenarios, and usage counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[systiger](https://clawhub.ai/user/systiger)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to look up preferred skills and preset parameters for recurring tasks, then record or update routing entries when task scenarios change.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task details, parameters, scenarios, timestamps, and usage counts can be saved across sessions without clear opt-in, redaction, retention, or deletion controls.

Mitigation: Use only when local skill-routing memory is desired; avoid secrets and sensitive free-form text in memory fields; inspect and clear references/memory.json when needed.

## Reference(s):

- [Skill Memory reference data](references/memory.json)
- [ClawHub skill page](https://clawhub.ai/systiger/skills/skill-memory)
- [Publisher profile](https://clawhub.ai/user/systiger)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration, JSON]

**Output Format:** [Markdown guidance with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May persist task types, parameters, scenarios, timestamps, and usage counts in references/memory.json.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
