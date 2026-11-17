## Description:

SQL Dreamer feeds OpenClaw dream cycles with high-importance SQL memories, archives light/REM/deep dream outputs to SQL, and prunes old dream files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oblio-falootin](https://clawhub.ai/user/oblio-falootin)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to run scheduled SQL-backed memory dreaming, curate high-importance memories into the native dreamer, and durably archive dream phase outputs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled jobs access persistent memory and SQL data.

Mitigation: Use a least-privilege SQL account, limit the configured workspace path, and review scheduled job permissions before deployment.

Risk: Database credentials and Confluence tokens may be exposed if stored in committed files.

Mitigation: Keep tokens, .env files, and filled config files out of source control, and prefer environment variables such as SQL_PASSWORD and CONFLUENCE_API_TOKEN.

Risk: Old dream files can be deleted after archival.

Mitigation: Verify SQL archival and backups before enabling cleanup, and test with dry-run behavior before scheduled execution.

Risk: The SQL connection string enables TrustServerCertificate=yes.

Mitigation: Remove or override TrustServerCertificate=yes for production deployments and configure certificate validation appropriate to the SQL Server environment.

Risk: Optional Confluence publishing can expose memory-derived content outside the local workspace.

Mitigation: Enable Confluence publishing only after reviewing page permissions and redacting sensitive memory content.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/oblio-falootin/skills/sql-dreamer)
- [Artifact README](artifact/README.md)
- [Getting Started](artifact/GETTING_STARTED.md)
- [SQL Skills Reference Architecture](artifact/SKILL_REFERENCE.md)
- [OpenClaw](https://openclaw.ai)
- [sql-connector skill](https://clawhub.ai/skills/sql-connector)
- [sql-memory skill](https://clawhub.ai/skills/sql-memory)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown files, SQL records, YAML configuration, Python scripts, and CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates curated memory inputs, archives dream phase outputs, can delete old dream files after archival, and can publish selected syntheses to Confluence when enabled.]

## Skill Version(s):

0.1.0 (source: evidence release metadata and artifact/openclaw.skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
