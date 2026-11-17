## Description:

Persistent memory for AI agents to store, search, and recall user context via the Smara Memory API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[parallelromb](https://clawhub.ai/user/parallelromb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give agents persistent user memory through Smara, including storing facts, semantic search, full-context retrieval, and memory deletion.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Selected conversation facts and lookup queries may be sent to Smara and stored across sessions.

Mitigation: Configure clear user opt-in and avoid storing secrets or sensitive personal information.

Risk: Full-context retrieval can expose more stored user information than the task needs.

Mitigation: Prefer narrow memory searches before retrieving full user context.

Risk: Memory deletion changes persisted user context.

Mitigation: Confirm destructive deletes before calling the delete endpoint.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/parallelromb/skills/smara-memory)
- [Smara website](https://smara.io)
- [Smara API documentation](https://api.smara.io/docs/)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline bash code blocks and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SMARA_API_KEY; API calls may store or retrieve user context in Smara.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
