## Description:

Reframe helps an agent strip noise, compress context, and redefine a stuck or overgrown problem from a simpler angle.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maochen1980](https://clawhub.ai/user/maochen1980)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill when a task is becoming too complex, repetitive, or noisy and the agent needs to restate the core problem before choosing the next step.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow stores compressed conversation context in a shared fixed temporary file.

Mitigation: Use in-memory handling or a secure per-session temporary file and clean it up after use.

Risk: The skill includes self-update instructions through a skill manager when verification fails.

Mitigation: Require explicit user approval before loading update tooling or modifying installed skill behavior.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maochen1980/skills/reframe)
- [Publisher profile](https://clawhub.ai/user/maochen1980)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summary and analysis guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and read a temporary Markdown summary as part of the workflow.]

## Skill Version(s):

1.0.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
