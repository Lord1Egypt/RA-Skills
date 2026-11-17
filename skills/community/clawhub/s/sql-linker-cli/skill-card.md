## Description:

SQL-Linker CLI provides multi-database CRUD for MySQL, PostgreSQL, and SQLite with bootstrap config generation, credential management using encrypted passwords and cloud-managed dbpw_key, cloud audit sync, API key introspection, and a per-invocation approval flag for credential access.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cloudcode-hans](https://clawhub.ai/user/cloudcode-hans)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database operators use this skill to bootstrap SQL-Linker configuration, inspect API key status, and run audited database queries or CRUD operations against MySQL, PostgreSQL, or SQLite. It is suited to agent-assisted database workflows that require explicit credential approval and cloud audit records.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has administrative database capability that can affect production data.

Mitigation: Use a least-privilege database account, keep read_only enabled unless writes are intended, and review each CRUD action before execution.

Risk: Credential handling and logged output may expose cloud API keys or database passwords.

Mitigation: Do not run config or CRUD commands where output is logged, enable require_explicit_credential_approval, and rotate any cloud API key or database password that may have been printed or stored.

Risk: Cloud audit behavior depends on the configured audit endpoint and can transmit operation metadata.

Mitigation: Verify cloud_audit_url before use and ensure operators understand which write-operation metadata is synchronized.

Risk: SQL-control weaknesses may allow unintended queries or writes.

Mitigation: Use parameterized queries, table allowlists, read-only mode where possible, and explicit approval for credentialed database access.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/cloudcode-hans/skills/sql-linker-cli)
- [SQL-Linker portal](https://sqllinker.agentpower.hk.cn/)
- [SQL-Linker API key metadata endpoint](https://sqllinker.agentpower.hk.cn/api/user/api-keys/by-key)
- [SQL-Linker cloud audit endpoint](https://sqllinker.agentpower.hk.cn/api/audit/logs)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, configuration]

**Output Format:** [CLI text output, optional JSON query output, and generated YAML, JSON, PowerShell, or shell configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May perform database operations and cloud audit sync; review security guidance before use with production data.]

## Skill Version(s):

2.0.3 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
