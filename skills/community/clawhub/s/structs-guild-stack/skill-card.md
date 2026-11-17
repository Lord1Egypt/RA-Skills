## Description:

Deploys the Guild Stack Docker Compose application for local PostgreSQL access to Structs game state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[abstrct](https://clawhub.ai/user/abstrct)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and game agents use this skill to deploy and operate a local Structs Guild Stack for PostgreSQL-backed game-state reads, real-time event monitoring, raid scouting, combat analysis, and fleet intelligence workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill starts persistent local Docker-based game-state indexing services that can keep running after setup.

Mitigation: Install only when this local stack is intended, start with the recommended read-only service set, review the Compose file before launch, and tear the stack down when no longer needed.

Risk: The optional transaction signing daemon can sign transactions on behalf of a configured key.

Mitigation: Keep the signing daemon disabled unless its code has been reviewed, isolate any signing key, bind the service locally, and use only a dedicated low-balance key.

Risk: Running an unpinned upstream checkout can change which services or images run locally.

Mitigation: Pin a release tag before starting services and review the pinned Compose file before each upgrade.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/abstrct/skills/structs-guild-stack)
- [Guild Stack repository](https://github.com/playstructs/docker-structs-guild)
- [Structs safety guidance](https://structs.ai/SAFETY)
- [Structs tools documentation](https://structs.ai/TOOLS)
- [Agent security awareness](https://structs.ai/awareness/agent-security)
- [Guild Stack architecture](https://structs.ai/knowledge/infrastructure/guild-stack)
- [Database schema and query patterns](https://structs.ai/knowledge/infrastructure/database-schema)
- [Database schema catalog](https://structs.ai/schemas/database-schema)
- [Structs intelligence skill](https://structs.ai/skills/structs-intel/SKILL)
- [Structs streaming skill](https://structs.ai/skills/structs-streaming/SKILL)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown with bash, SQL, and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes Docker Compose lifecycle commands, PostgreSQL query patterns, and operational cautions for local services.]

## Skill Version(s):

1.25.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
