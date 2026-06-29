## Description: <br>
SQL-Linker CLI provides multi-database CRUD for MySQL, PostgreSQL, and SQLite with bootstrap configuration generation, credential management, cloud audit sync to SQL-Linker, API key introspection, and a per-invocation approval flag for credential access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and database operators use this skill to bootstrap configuration and run audited CRUD workflows across MySQL, PostgreSQL, and SQLite from an agent-assisted CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on a configured cloud endpoint for API key introspection and audit synchronization. <br>
Mitigation: Install only if the publisher and endpoint are trusted; review audit_config.json and keep cloud_audit_url pinned to the intended service. <br>
Risk: The query command should not be assumed to be read-only because it accepts arbitrary SQL text. <br>
Mitigation: Review SQL before execution and use a least-privilege or read-only database account where possible. <br>
Risk: Credential and SQL controls require operator review before installation. <br>
Mitigation: Verify the credential approval gate, API key configuration, and database permissions before use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cloudcode-hans/skills/sql-linker-cli) <br>
- [SQL-Linker API key portal](https://sqllinker.agentpower.hk.cn/) <br>
- [Cloud API key introspection endpoint](https://sqllinker.agentpower.hk.cn/api/user/api-keys/by-key) <br>
- [Cloud audit log endpoint](https://sqllinker.agentpower.hk.cn/api/audit/logs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands, SQL examples, and JSON/YAML configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide creation of local database configuration, audit configuration, table dictionary, and environment setup files when the CLI is executed.] <br>

## Skill Version(s): <br>
2.0.3 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
