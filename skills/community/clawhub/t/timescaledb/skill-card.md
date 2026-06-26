## Description: <br>
Store and query time-series data with hypertables, compression, and continuous aggregates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and database engineers use this skill for quick TimescaleDB guidance on hypertables, chunk intervals, continuous aggregates, compression, retention, indexing, inserts, and query patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: SQL examples can alter database structure, create policies, compress chunks, or delete old data when run against a live database. <br>
Mitigation: Confirm the target database, table names, permissions, backup status, retention interval, and expected operational impact before executing generated SQL. <br>
Risk: The skill is documentation-only and does not validate whether examples match a specific TimescaleDB deployment. <br>
Mitigation: Review examples against the installed TimescaleDB version, schema, and workload before applying them. <br>


## Reference(s): <br>
- [ClawHub TimescaleDB skill page](https://clawhub.ai/ivangdavila/timescaledb) <br>
- [Publisher profile: ivangdavila](https://clawhub.ai/user/ivangdavila) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands] <br>
**Output Format:** [Markdown with inline SQL and command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires psql for database command execution; examples should be reviewed before use against a live database.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
