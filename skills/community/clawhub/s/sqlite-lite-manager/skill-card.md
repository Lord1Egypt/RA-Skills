## Description:

精简版Sqlite helps agents perform lightweight local SQLite data storage, SQL queries, and basic database operations with Chinese interaction support and low resource use.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, independent builders, and automation teams use this skill to let an agent create tables, query records, and manage lightweight local SQLite data. It is not a substitute for database architecture decisions or high-risk manual judgment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unintended SQLite data modification or deletion.

Mitigation: Use the skill only on intended SQLite files, keep backups, and require explicit confirmation before update or delete operations.

Risk: Sensitive database contents or API keys may be exposed through agent or LLM integrations.

Mitigation: Limit workspace and database access, avoid broad permissions, and clarify whether any LLM or API integration can see database contents before use.

Risk: The release asks for broad database-changing capability while safeguards and data flow are unclear.

Mitigation: Review the skill before installing it in workflows that touch important or sensitive databases, and use it in a constrained environment where possible.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sqlite-lite-manager)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and shell snippets plus JSON-style status examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read from and write to local SQLite databases; confirm destructive operations before execution.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
