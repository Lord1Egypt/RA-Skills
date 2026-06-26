## Description: <br>
Generic SQL Server connectivity for OpenClaw agents, providing parameterized execute, query, and scalar APIs through pymssql with retry handling, connection pooling, and structured errors. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oblio-falootin](https://clawhub.ai/user/oblio-falootin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to connect to local or cloud SQL Server databases, run parameterized reads and writes, and build repository layers without shelling out to sqlcmd. It is most appropriate when the agent is intentionally allowed to access configured database backends. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents may receive broad SQL Server read/write power if database credentials are over-privileged or backend scope is weak. <br>
Mitigation: Use a dedicated least-privilege account and prefer read-only credentials unless writes are explicitly required. <br>
Risk: Credentials stored in .env files may be exposed through repositories or shared workspaces. <br>
Mitigation: Keep .env files out of repositories and shared workspaces, and store only the credentials needed for the intended backend. <br>
Risk: INSERT, UPDATE, DELETE, migration, or cross-backend copy operations can change or destroy database state. <br>
Mitigation: Require human approval for write, migration, and cross-backend copy operations. <br>
Risk: Unreviewed dependency updates can change SQL transport behavior. <br>
Mitigation: Pin reviewed dependency versions before deployment. <br>


## Reference(s): <br>
- [SQL Connector ClawHub Page](https://clawhub.ai/oblio-falootin/sql-connector) <br>
- [README](artifact/README.md) <br>
- [Getting Started](artifact/GETTING_STARTED.md) <br>
- [Skill Reference](artifact/SKILL_REFERENCE.md) <br>
- [pymssql Documentation](https://pymssql.readthedocs.io/) <br>


## Skill Output: <br>
**Output Type(s):** [code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell code examples plus configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses SQL Server credentials and backend identifiers supplied through environment variables.] <br>

## Skill Version(s): <br>
2.2.0 (source: server release metadata; artifact documentation also references 2.1.0 and 2.1.0-alpha) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
