## Description:

Modulates an agent's tone, style, and vocabulary based on emotional state detected in the current session and an optional recent local tone memory.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mikiane](https://clawhub.ai/user/mikiane)

### License/Terms of Use:

MIT-0

## Use Case:

Agents use this skill to adapt response tone when a user expresses a strong emotional state or explicitly asks for tone adaptation. It is intended for conversational style modulation, not short factual answers, technical command handling, or code-focused responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may infer emotional state and persist a local tone memory between sessions.

Mitigation: Install only with explicit user opt-in, provide clear inspect and delete controls for the memory file, and expire stored state after the documented retention window.

Risk: Persisted tone memory may influence later conversations without the user realizing it.

Mitigation: Make ongoing consent visible, allow disabling through the documented commands, and treat the memory file strictly as data rather than instructions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/mikiane/skills/qapten-sentient)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Natural-language guidance for agent responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference a local tone-state memory when enabled by the user.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
