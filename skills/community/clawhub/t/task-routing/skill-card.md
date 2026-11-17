## Description:

A lightweight task routing engine for intelligent task assignment based on change type, size, risk, and urgency.

This skill is ready for commercial/non-commercial use.

## Publisher:

[terr123123](https://clawhub.ai/user/terr123123)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent builders use this skill to route development tasks, assign workflows or teams, and rank work based on change type, size, risk, urgency, and custom routing rules.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Custom routing rules can change which task metadata fields are compared and which workflow or team labels are returned.

Mitigation: Review rule data before loading it and restrict trusted rule sources for production routing.

Risk: Routing and priority decisions can be incorrect when task metadata is incomplete or stale.

Mitigation: Review the returned target, confidence, alternatives, and priority ranking before acting on high-risk or urgent work.

## Reference(s):

- [Task Routing ClawHub release](https://clawhub.ai/terr123123/skills/task-routing)

## Skill Output:

**Output Type(s):** [Code, Configuration, Guidance]

**Output Format:** [Markdown with Python examples and JSON-compatible routing data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces routing decisions, confidence values, alternatives, priority rankings, and serialized routing rules.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
