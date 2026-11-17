## Description:

SQL Memory provides a SQL Server-backed semantic memory layer for OpenClaw agents, including memory recall, search, task queues, activity logs, todos, knowledge indexing, and hierarchical rollups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oblio-falootin](https://clawhub.ai/user/oblio-falootin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers building OpenClaw agents use SQL Memory to persist and recall structured memories, queue work, log activity, manage todos, and index knowledge in a SQL Server database.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires SQL database credentials and can access persisted memory, task, todo, and activity data.

Mitigation: Use a dedicated, least-privileged database account and avoid production or shared credentials.

Risk: Broad database escape hatches and scheduled workflows may perform actions outside the intended high-level memory API.

Mitigation: Expose only reviewed high-level APIs to agents; restrict raw SQL methods and cron workflows unless separately reviewed.

Risk: Configuration behavior may load credentials from an unintended .env path.

Mitigation: Control the install path and exact .env location, then verify the active backend before use.

Risk: The skill depends on sql-connector for database transport.

Mitigation: Install, pin, and verify sql-connector before enabling SQL Memory.

## Reference(s):

- [SQL Memory ClawHub page](https://clawhub.ai/oblio-falootin/skills/sql-memory)
- [README](artifact/README.md)
- [Getting Started](artifact/GETTING_STARTED.md)
- [Skill Reference](artifact/SKILL_REFERENCE.md)
- [SQL Connector dependency](https://github.com/High-Falootin/clawbot-sql-connector)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with Python and shell examples; runtime API methods return strings, booleans, task IDs, and lists of records.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sql-connector and a configured least-privileged SQL Server database.]

## Skill Version(s):

2.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
