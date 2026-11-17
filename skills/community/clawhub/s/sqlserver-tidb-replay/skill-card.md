## Description:

Replay SQL Server slow query logs on TiDB to verify compatibility, compare performance, and generate syntax conversion reports during migration.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongdong-bryant](https://clawhub.ai/user/dongdong-bryant)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and database migration engineers use this skill to convert SQL Server slow-query exports into replayable TiDB workloads, run compatibility and performance checks in a test TiDB environment, and review generated migration reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The replay workflow can execute captured SQL against a target TiDB database and may change or damage data if used on a shared or production environment.

Mitigation: Run replay only against an isolated disposable test database, inspect replay JSON before execution, and use a dedicated least-privileged TiDB account instead of root.

Risk: Captured SQL logs, intermediate JSON, CSV files, and HTML reports may contain sensitive production data.

Mitigation: Treat all generated artifacts as sensitive, restrict access, and redact data before sharing reports or logs.

Risk: The security evidence notes weak safety controls and a published root-password example.

Mitigation: Remove the hardcoded password example, avoid root credentials, and provide connection secrets through controlled environment or runtime configuration.

Risk: Remote database replay can expose credentials or query contents if transport security is not enforced.

Mitigation: Require TLS for remote TiDB connections and run replay from a controlled network environment.

Risk: Reports generated from untrusted inputs may expose sensitive content or unsafe rendered data.

Mitigation: Do not open reports generated from untrusted inputs, and sanitize or redact report content before review or distribution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongdong-bryant/skills/sqlserver-tidb-replay)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, JSON, HTML]

**Output Format:** [Markdown guidance with shell commands plus generated CSV, JSON, and HTML report files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The workflow uses Python scripts to normalize CSV input, produce replay JSON, execute SQL against TiDB, and generate compatibility and performance reports.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
