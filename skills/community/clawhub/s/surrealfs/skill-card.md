## Description:

SurrealFS virtual filesystem for AI agents. Rust core + Python agent (Pydantic AI). Persistent file operations backed by SurrealDB. Part of the surreal-skills collection.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24601](https://clawhub.ai/user/24601)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to give agents a persistent, queryable virtual filesystem backed by SurrealDB for durable workspace storage, content search, and shared file operations across sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The documented host command execution feature can run pipe source commands on the host.

Mitigation: Install and test in an isolated development environment, allow only trusted command inputs, and review commands before execution.

Risk: Remote SurrealDB access, local HTTP serving, and telemetry can expose credentials or sensitive workspace data if configured carelessly.

Mitigation: Use least-privilege SurrealDB credentials, avoid command-line passwords for real secrets, keep HTTP binding private unless protected by authentication and TLS, and disable or audit telemetry for sensitive data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/24601/skills/surrealfs)
- [SurrealFS upstream repository](https://github.com/surrealdb/surrealfs)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown or plain text with inline code and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include virtual filesystem operation results, setup guidance, and configuration values for SurrealDB-backed storage.]

## Skill Version(s):

1.2.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
