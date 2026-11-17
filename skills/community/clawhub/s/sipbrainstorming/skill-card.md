## Description:

Guides agents through a design-first brainstorming workflow that explores user intent, requirements, options, and approval before implementation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[usipipo](https://clawhub.ai/user/usipipo)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to turn feature, component, or behavior-change ideas into approved designs before implementation begins.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can force a broad design-first workflow that may slow or block straightforward implementation.

Mitigation: Install it only when a strict planning gate is desired, and confirm that current user instructions still allow the workflow.

Risk: The skill can direct agents to create design files and git commits as part of the workflow.

Mitigation: Require separate confirmation before writing files or creating commits, and review generated changes before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/usipipo/skills/sipbrainstorming)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Files]

**Output Format:** [Conversational guidance and Markdown design documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires design approval before implementation and may produce a design document after approval.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
