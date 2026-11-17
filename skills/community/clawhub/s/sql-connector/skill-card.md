## Description:

SQL Connector provides a sealed, retry-capable SQL Server connector for OpenClaw agents using pymssql, with parameterized execute, query, scalar, and ping APIs for local or cloud backends.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oblio-falootin](https://clawhub.ai/user/oblio-falootin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use SQL Connector to add reliable SQL Server access without subprocess or sqlcmd dependencies. It supports parameterized reads and writes, scalar queries, connection health checks, retries, and local or cloud backend selection through environment configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents using this skill can access and write to the configured SQL Server.

Mitigation: Install only for agents that need database access and configure a least-privileged database account instead of admin or production-wide credentials.

Risk: Credential handling can expose sensitive .env values if users paste, print, or run broad diagnostics against SQL environment variables.

Mitigation: Store .env securely, avoid printing SQL_* values, and do not use the documented grep SQL_ diagnostic with sensitive credentials.

Risk: Automatic retry around write operations can affect sensitive or non-idempotent database workflows.

Mitigation: Review the .env loading and write retry behavior before using the connector with sensitive or non-idempotent operations.

## Reference(s):

- [SQL Connector ClawHub Page](https://clawhub.ai/oblio-falootin/skills/sql-connector)
- [Getting Started](artifact/GETTING_STARTED.md)
- [Skill Reference](artifact/SKILL_REFERENCE.md)
- [pymssql Documentation](https://pymssql.readthedocs.io/)

## Skill Output:

**Output Type(s):** [Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with Python, shell, and environment configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces guidance for SQL Server connectivity and expects credentials to be supplied through environment variables or compatible configuration.]

## Skill Version(s):

2.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
