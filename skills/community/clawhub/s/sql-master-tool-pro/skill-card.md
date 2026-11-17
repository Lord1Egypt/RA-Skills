## Description:

SQL大师工具(专业版) helps developers, DBAs, and operations teams plan database migrations, incremental backups, schema comparison and synchronization, high availability, read/write splitting, monitoring, and disaster recovery workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, DBAs, and operations teams use this skill to create database operations guidance, configuration examples, migration and backup workflows, schema synchronization plans, high-availability setup guidance, and recovery procedures for team and production environments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Database administration guidance can lead to destructive changes or availability impact when applied directly to a real database.

Mitigation: Require dry runs, verified backups, explicit target-environment naming, least-privilege credentials, and human approval before migrations, sync scripts, failover, recovery, or backup synchronization.

Risk: The skill has broad database-operations scope and incomplete safety gating.

Mitigation: Review the generated plan and commands carefully before use, and enable the skill only when database administration assistance is intentionally needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/sql-master-tool-pro)
- [ClawHub publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration]

**Output Format:** [Markdown guidance with code blocks and JSON-style status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include database operation logs, migration plans, backup settings, synchronization scripts, and troubleshooting steps.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
