## Description: <br>
Feeds OpenClaw dreamer with high-importance memories from SQL, archives dream outputs back to SQL, and prunes old dream files automatically. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[oblio-falootin](https://clawhub.ai/user/oblio-falootin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw operators use SQL Dreamer to feed curated SQL-backed memories into OpenClaw's native dreaming pipeline, archive light/REM/deep dream outputs to SQL, and optionally prepare outputs for Confluence publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles durable memory data and SQL credentials. <br>
Mitigation: Install only in an OpenClaw workspace and SQL database you control, store credentials in environment variables, and do not commit populated configuration files. <br>
Risk: Scheduled cleanup can delete dream output files after the configured archive window. <br>
Mitigation: Review archive_after_days and run dry-runs before enabling scheduled cleanup. <br>
Risk: Optional Confluence publishing may expose memory-derived content outside the local workspace. <br>
Mitigation: Keep Confluence disabled unless external publishing is intended and the target space, parent page, and token are approved. <br>
Risk: Dependencies are not pinned by a lockfile. <br>
Mitigation: Consider pinning dependencies or using a lockfile for repeatable installs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/oblio-falootin/sql-dreamer) <br>
- [README](README.md) <br>
- [Getting Started](GETTING_STARTED.md) <br>
- [SQL Skills Reference Architecture](SKILL_REFERENCE.md) <br>
- [Example configuration](config/example.yml) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with shell commands, YAML configuration, SQL schema notes, and Python command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup and operation guidance for SQL-backed OpenClaw dream ingestion, archival, cleanup, and optional Confluence publishing.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence and target metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
