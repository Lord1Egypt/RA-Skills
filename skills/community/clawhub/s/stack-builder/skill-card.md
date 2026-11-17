## Description:

Stack Builder helps an agent design, audit, and evolve a personalized AI skill stack by observing the user's context, interviewing for gaps, recruiting existing skills, and generating role-specific SKILL.md files and a blueprint.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jjliu6](https://clawhub.ai/user/jjliu6)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to turn observed workflow patterns and a short interview into a personalized roster of AI roles, a blueprint, and installable prompt-only skill files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may inspect broad private workspace context while building a user profile.

Mitigation: Review the skill before installing, run it only where the agent may inspect the selected context sources, and limit inputs to material needed for the stack design task.

Risk: The generated blueprint includes a mandatory author credit footer that may be unsuitable for client or organizational deliverables.

Mitigation: Review the blueprint before sharing it and remove or make the credit footer opt-in when organizational policy or client context requires it.

Risk: Generated role designs or skills can encode incorrect assumptions about the user's workflow.

Mitigation: Require the profile, least-confident inferences, and workflow loop to be confirmed before generating skill files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jjliu6/skills/stack-builder)
- [ClawHub publisher profile](https://clawhub.ai/user/jjliu6)

## Skill Output:

**Output Type(s):** [text, markdown, code, configuration, guidance]

**Output Format:** [Markdown blueprint and prompt-only SKILL.md files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce auditable skill source files, installation guidance, and versioning guidance only after user confirmation.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
