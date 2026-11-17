## Description:

查询客流数据，输出 JSON，适合直接导入 Bitable 或其它数据可视化工具。

This skill is ready for commercial/non-commercial use.

## Publisher:

[z1chengge](https://clawhub.ai/user/z1chengge)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations users can use this skill to query passenger-flow data for a specified date range from a SQL Server database and export the result as JSON for Bitable or other visualization tools.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill uses SQL Server credentials and database network access.

Mitigation: Use a dedicated least-privileged SQL account limited to the required stored procedure and store credentials in a protected environment rather than shared shell profiles.

Risk: Database connections may not enforce verified encrypted transport.

Mitigation: Restrict network access to the intended SQL Server, require a modern ODBC driver with verified TLS, and rotate the password if it was used over an untrusted network.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/z1chengge/skills/python-ysddata-keliu)
- [Publisher profile](https://clawhub.ai/user/z1chengge)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON object with status, columns, and rows fields]

**Output Parameters:** [1D date-range query with start and end dates]

**Other Properties Related to Output:** [Requires SQL Server connection settings through environment variables.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
