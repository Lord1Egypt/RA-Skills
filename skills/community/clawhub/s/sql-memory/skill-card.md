## Description: <br>
SQL Memory gives OpenClaw agents durable SQL-backed memory, task queues, activity logs, todos, and knowledge search. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oblio-falootin](https://clawhub.ai/user/oblio-falootin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to persist agent memories, coordinate queued work, record audit activity, manage todos, and search stored knowledge in a SQL Server-backed memory database. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives agents durable access to SQL-backed memory, which can retain sensitive, stale, or unnecessary data. <br>
Mitigation: Use a dedicated memory database, avoid storing secrets or unnecessary personal data, and define retention and deletion rules before deployment. <br>
Risk: Broad database mutation behavior can affect stored memories, queues, logs, knowledge records, and todos. <br>
Mitigation: Use least-privilege SQL credentials, avoid production or shared databases, and review the configured schema and permissions before enabling autonomous use. <br>
Risk: Legacy raw SQL passthrough increases the impact of agent mistakes in autonomous or multi-agent workflows. <br>
Mitigation: Restrict or remove raw SQL passthrough and prefer the parameterized memory APIs for normal agent operations. <br>


## Reference(s): <br>
- [ClawHub SQL Memory release page](https://clawhub.ai/oblio-falootin/sql-memory) <br>
- [Getting Started](GETTING_STARTED.md) <br>
- [Skill Reference](SKILL_REFERENCE.md) <br>
- [SQL Connector dependency](https://github.com/High-Falootin/clawbot-sql-connector) <br>


## Skill Output: <br>
**Output Type(s):** [text, code, configuration, shell commands, guidance] <br>
**Output Format:** [Python API results, SQL-backed records, and Markdown setup guidance with inline commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires sql-connector, SQL Server schema setup, and configured SQL credentials.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
