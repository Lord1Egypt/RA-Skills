## Description:

Generate structured implementation spec documents for coding projects or features before implementation begins.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lgyanami](https://clawhub.ai/user/lgyanami)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to turn requirements, feature ideas, bug reports, or GitHub issues into structured implementation specs with objectives, user stories, technical plans, boundaries, verification criteria, and task breakdowns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may read relevant project files and referenced GitHub issues or documentation while gathering context.

Mitigation: Use it only in repositories and linked resources the agent is permitted to inspect, and review included context before relying on the resulting spec.

Risk: A generated spec can set incorrect implementation boundaries or verification criteria.

Mitigation: Review and confirm the spec boundaries, task breakdown, and verification criteria before using it to guide implementation.

## Reference(s):

- [Spec Template](references/spec-template.md)
- [ClawHub Skill Page](https://clawhub.ai/lgyanami/skills/spec-writer)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown spec document]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Default output path is SPEC.md or spec/<name>.md after user review.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
