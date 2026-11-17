## Description:

Use when a user is trying to discover an installable or reusable skill or workflow, especially when they ask for a skill for a task, want to compare nearby skill categories, or need help narrowing discovery results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[littledinoc](https://clawhub.ai/user/littledinoc)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to discover, compare, and narrow installable or reusable skills for a stated task. It supports a short recommendation flow with optional clarification and feedback capture.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User queries, clarification details, selected skill IDs, and final feedback may be sent to a third-party service.

Mitigation: Install only if that telemetry is acceptable, and avoid entering secrets or private project details into requests handled by this skill.

Risk: Recommended install commands may reference unpinned packages or repositories.

Mitigation: Verify repository ownership and contents before running generated commands, and prefer pinned package versions and commit hashes.

## Reference(s):

- [Skill Grep on ClawHub](https://clawhub.ai/littledinoc/skills/skill-grep)
- [Skill Grep service endpoint](https://skills.megatechai.com/)

## Skill Output:

**Output Type(s):** [guidance, markdown, API calls]

**Output Format:** [Markdown recommendation summaries with structured retrieval and feedback payloads handled by the agent]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May transmit skill-discovery queries, clarification details, selected skill IDs, and final feedback to an external service.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
