## Description:

Guides agents to restore project context across sessions and workspaces using memory files and a semantic-memory fallback.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoxinghua09-cell](https://clawhub.ai/user/zhaoxinghua09-cell)

### License/Terms of Use:

MIT-0

## Use Case:

AI agents and their operators use this protocol to resume work across sessions without repeatedly asking for settled project facts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The protocol loads memory across workspaces without clear opt-in.

Mitigation: Require explicit confirmation before loading prior memory and limit reads to the current workspace unless broader access is needed.

Risk: Persisted memory may retain secrets or sensitive operational details.

Mitigation: Exclude secrets and sensitive operational details before updating memory files or semantic memory.

Risk: Declared file permissions do not match the protocol's memory reads and writes.

Mitigation: Align declared permissions with the access the skill needs before deployment.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/zhaoxinghua09-cell/skills/session-continuity-protocol)

## Skill Output:

**Output Type(s):** [Guidance, Text]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Session-opening checklist and updated memory records when new facts are confirmed.]

## Skill Version(s):

1.0.1 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
