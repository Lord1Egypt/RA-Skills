## Description:

High-performance SpacetimeDB memory integration for OpenClaw that replaces static file memory with a local SpacetimeDB-backed memory system with CRUD, legacy import, and consolidation support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kennethrajsimon](https://clawhub.ai/user/kennethrajsimon)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to store, search, update, delete, and migrate long-term agent memories in a SpacetimeDB instance. It is most appropriate when the user controls the database endpoint and wants memory operations exposed through OpenClaw tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist and reveal sensitive long-term memory content through its SpacetimeDB-backed tools.

Mitigation: Use only with a SpacetimeDB endpoint you control, preferably local loopback, and review stored memory content before sharing outputs.

Risk: Setting SPACETIMEDB_URL to a remote or plaintext server can send memory content and imported files to that endpoint.

Mitigation: Keep SPACETIMEDB_URL on a trusted local or secured endpoint unless remote transfer is intentional.

Risk: The legacy import flow can migrate sensitive files and overwrite originals after creating backups.

Mitigation: Avoid legacy-import unless backups exist, the database is confirmed working, and the user has explicitly approved the import.

Risk: The tools can update or delete stored memories by ID.

Mitigation: Review edit and delete requests before execution and keep recoverable backups for important memory content.

## Reference(s):

- [SpacetimeDB](https://spacetimedb.com/)
- [ClawHub Skill Page](https://clawhub.ai/kennethrajsimon/skills/spacetime-memory)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Configuration]

**Output Format:** [Tool JSON responses and Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Operates against a configured SpacetimeDB endpoint and may read, persist, update, delete, or migrate memory content.]

## Skill Version(s):

1.1.7 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
