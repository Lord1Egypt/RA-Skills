## Description:

MCP Database Server 是一个为AI助手和基于LLM的工具提供安全数据库访问的服务，支持SQLite、PostgreSQL、MySQL和MariaDB，具有查询验证、审计日志和安全控制功能。

This skill is ready for commercial/non-commercial use.

## Publisher:

[cainingnk](https://clawhub.ai/user/cainingnk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and AI assistant operators use this skill to inspect database tables, describe schemas, execute SQL statements, and request query plans through the XiaoBenYang database service.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database connection strings, SQL statements, query parameters, and query results may be sent to the XiaoBenYang service.

Mitigation: Use narrowly scoped read-only database credentials by default and avoid production database URLs or high-privilege accounts unless the external data flow, retention, and access controls are acceptable.

Risk: The XBY API key can be stored in plaintext in a local .env file.

Mitigation: Use a dedicated key for testing, restrict access to the local environment, and rotate or remove the key after evaluation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cainingnk/skills/xby-db)
- [XiaoBenYang](https://xiaobenyang.com)
- [XiaoBenYang MCP service](https://mcp.xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, configuration, guidance]

**Output Format:** [Markdown summaries with structured tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY API key and may return database metadata, query results, or explain-plan details.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
