## Description:

Use this skill when you need to query, insert, update, or delete records in a configured MySQL, PostgreSQL, or SQLite database and you know the target table name and approximate schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to perform targeted CRUD operations and audit-log review against configured relational databases when a specific table or intent is known. It is suitable for local development and controlled database workflows that require explicit schema and configuration boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database access controls and credential handling are weaker than the skill's security claims.

Mitigation: Install only for local development or tightly controlled databases, use a least-privilege database account, and keep read-only mode enabled until write access is explicitly needed.

Risk: Generated or configured credentials can be exposed when local configuration and environment values are available to the agent in the same trust boundary.

Mitigation: Prefer a proper secret manager over the generated dbpw_key and environment setup, and enable explicit credential approval before credential-backed connections.

Risk: Table allowlists and extra table configuration should not be treated as a hard security boundary.

Mitigation: Restrict database permissions at the database account level and review requested SQL operations before execution, especially INSERT, UPDATE, and DELETE.

## Reference(s):

- [sql-linker ClawHub page](https://clawhub.ai/cloudcode-hans/skills/sql-linker)
- [sql-linker-cli production alternative](https://clawhub.ai/cloudcode-hans/skills/sql-linker-cli)

## Skill Output:

**Output Type(s):** [text, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline code, shell commands, configuration examples, and returned query or audit data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local configuration files and return database rows, affected-row counts, audit records, or setup guidance depending on the requested operation.]

## Skill Version(s):

1.3.2 (source: server release metadata; artifact frontmatter says 1.3.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
