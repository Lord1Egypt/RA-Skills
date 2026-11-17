## Description:

Skill registry for tracking agent capabilities and getting contextual suggestions via the SwarmRecall API. Register, list, and query installed skills with semantic matching for task-relevant recommendations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[waydelyle](https://clawhub.ai/user/waydelyle)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to register installed capabilities with SwarmRecall, list stored skills, and request semantic suggestions for task-relevant skills.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Skill metadata and task descriptions may be sent to the external SwarmRecall service.

Mitigation: Use the skill only with user consent for external storage and avoid sending secrets or sensitive project details as task context.

Risk: The skill uses a bearer token and supports a configurable API endpoint.

Mitigation: Store SWARMRECALL_API_KEY only in the environment and keep SWARMRECALL_API_URL unset unless it points to a trusted SwarmRecall deployment.

Risk: Registry writes and deletes can change stored skill records.

Mitigation: Require explicit confirmation before deleting registry entries or storing user-provided content.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/waydelyle/skills/swarmrecall-skills)
- [SwarmRecall Homepage](https://www.swarmrecall.ai)
- [SwarmRecall API Base URL](https://swarmrecall-api.onrender.com)

## Skill Output:

**Output Type(s):** [Guidance, JSON, Configuration]

**Output Format:** [Markdown guidance with JSON API request and response examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SWARMRECALL_API_KEY for authenticated calls; SWARMRECALL_API_URL may override the default API endpoint.]

## Skill Version(s):

1.1.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
