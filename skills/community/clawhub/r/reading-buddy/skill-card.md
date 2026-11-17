## Description:

Reading Buddy is a social reading platform for registering books, creating virtual reading rooms, and sharing chat messages and reading insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[harrylabsj](https://clawhub.ai/user/harrylabsj)

### License/Terms of Use:

MIT-0

## Use Case:

Readers, facilitators, and developers use this skill to manage a local social reading workspace with book catalogs, virtual reading rooms, member participation, chat history, and exported reading discussions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Multi-user chat and room controls trust caller-supplied user IDs.

Mitigation: Use only as a local prototype unless real authentication and room membership authorization are added before shared or networked use.

Risk: Shared chat exports and deletion-capable workflows can expose or remove participant content without robust controls.

Mitigation: Add export access checks, deletion confirmations, and auditable authorization before using with multiple users.

Risk: Dependencies and deployment posture need review before service exposure.

Mitigation: Update dependencies and complete deployment hardening before exposing the app as an API, WebSocket service, or shared platform.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/harrylabsj/skills/reading-buddy)
- [Skill README](SKILL.md)
- [Design Overview](design/overview.md)
- [System Architecture](design/architecture.md)
- [Workflows](design/workflows.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [CLI text, Markdown exports, and TypeScript or JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses a local SQLite database under ~/.reading-buddy after initialization.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
