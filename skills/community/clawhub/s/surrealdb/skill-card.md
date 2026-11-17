## Description:

SurrealDB 3 helps coding agents design, query, secure, deploy, and tune SurrealDB projects with SurrealQL, multi-model schemas, SDK integrations, MCP, and ecosystem tooling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[24601](https://clawhub.ai/user/24601)

### License/Terms of Use:

MIT

## Use Case:

Developers and engineers use this skill to get SurrealDB 3 architecture guidance, SurrealQL examples, schema design patterns, security and deployment recommendations, performance tuning help, SDK and MCP integration guidance, and diagnostics or schema introspection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Global installation and helper scripts can affect an agent setup across projects.

Mitigation: Prefer a project-scoped or pinned installation and review the skill before installing it globally.

Risk: The skill can work with live SurrealDB credentials and database endpoints.

Mitigation: Use read-only or least-privilege credentials, avoid production root credentials, and review generated queries or commands before execution.

Risk: Interactive setup may create local environment files containing sensitive values.

Mitigation: Avoid writing real passwords to .env files unless file permissions and git ignores are verified.

Risk: Auto-confirmed installation commands can bypass normal review prompts.

Mitigation: Avoid auto-confirmed npx commands and inspect package, install scope, and requested changes before proceeding.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/24601/skills/surrealdb)
- [SurrealDB Skills Repository](https://github.com/24601/surreal-skills)
- [SurrealDB Documentation](https://surrealdb.com/docs)
- [SurrealDB Installation Documentation](https://surrealdb.com/docs/surrealdb/installation)
- [uv Installation Documentation](https://docs.astral.sh/uv/getting-started/installation/)
- [Online Docs Reference](references/online_docs.md)
- [SurrealQL Cheatsheet](references/surrealql_cheatsheet.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline code blocks, shell commands, configuration snippets, and optional JSON or schema outputs from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose database queries, installation commands, environment variables, and schema inspection commands that should be reviewed before execution.]

## Skill Version(s):

1.7.1 (source: frontmatter, changelog released 2026-06-17, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
