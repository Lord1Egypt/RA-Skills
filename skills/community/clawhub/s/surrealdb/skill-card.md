## Description: <br>
Provides agent-facing guidance, commands, and reference material for SurrealDB 3 architecture, SurrealQL, schema design, security, deployment, performance, SDKs, MCP, and ecosystem integrations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[24601](https://clawhub.ai/user/24601) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill to design, operate, inspect, and troubleshoot SurrealDB 3 projects with agent assistance. It helps agents produce SurrealQL, schema guidance, deployment and security recommendations, SDK integration examples, shell commands, and configuration guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated SurrealQL or shell commands could change production databases if run without review. <br>
Mitigation: Review commands and queries before execution, especially against production, and prefer read-only or least-privilege credentials. <br>
Risk: SurrealDB endpoint credentials can be exposed if passwords are placed directly on command lines or written into tracked files. <br>
Mitigation: Use environment variables for credentials, avoid real passwords on command lines, and write .env files only in private workspaces excluded from version control. <br>
Risk: Default root/root credentials are unsafe outside disposable local databases. <br>
Mitigation: Use local root/root examples only for throwaway local development and create scoped users for shared or production environments. <br>


## Reference(s): <br>
- [SurrealDB 3 skill page](https://clawhub.ai/24601/surrealdb) <br>
- [Publisher profile](https://clawhub.ai/user/24601) <br>
- [Project homepage](https://github.com/24601/surreal-skills) <br>
- [SurrealDB documentation](https://surrealdb.com/docs) <br>
- [Online docs reference](references/online_docs.md) <br>
- [SurrealQL cheatsheet](references/surrealql_cheatsheet.md) <br>
- [SOURCES provenance tracker](SOURCES.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline code blocks, shell commands, configuration snippets, and occasional JSON from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose SurrealQL and shell commands for user review before execution.] <br>

## Skill Version(s): <br>
1.7.1 (source: SKILL.md frontmatter, CHANGELOG, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
