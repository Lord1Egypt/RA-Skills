## Description: <br>
Provides DMS client data management guidance for instance management, SQL queries, workorder creation, team management, and user management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18108851659-yzh](https://clawhub.ai/user/18108851659-yzh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to plan DMS client commands and API-oriented workflows for database instance administration, SQL execution, workorders, teams, and users. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide high-impact database administration, account-management, team, workorder, and permission changes. <br>
Mitigation: Require explicit human confirmation before any write, delete, team or user change, workorder action, or permission change, and use least-privilege accounts. <br>
Risk: Unsafe examples or inconsistent PostgreSQL database-selection guidance could cause operations to run against the wrong database. <br>
Mitigation: For PostgreSQL, verify the login database with current_database() and specify the target database at login with --db-name rather than relying on --database, --db-id, or --schema-id to switch databases. <br>
Risk: Database credentials, tokens, and JWT cookies may be exposed through chat, command history, or logs. <br>
Mitigation: Handle secrets outside chat and shell history, use a trusted version-pinned DMS CLI, and rotate credentials or tokens if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18108851659-yzh/test000-my-skill) <br>
- [Publisher profile](https://clawhub.ai/user/18108851659-yzh) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, API Calls, Configuration] <br>
**Output Format:** [Markdown with inline shell commands and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include high-impact database, account-management, team, workorder, and permission-change instructions that require human confirmation.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
