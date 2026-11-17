## Description:

Store and query time-series data with hypertables, compression, and continuous aggregates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and database engineers use this skill as a concise TimescaleDB reference for hypertables, chunk intervals, time_bucket queries, continuous aggregates, compression, retention, indexing, insert performance, query patterns, and distributed hypertables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Retention-policy examples can delete older historical data from the target database.

Mitigation: Confirm the target table, retention interval, backup requirements, and acceptability of data loss before applying retention-policy SQL.

Risk: Manual SQL examples may be applied to the wrong database object or workload.

Mitigation: Review commands against the intended schema and operational requirements before running them with psql.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/timescaledb)
- [Publisher profile](https://clawhub.ai/user/ivangdavila)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown with inline SQL examples and command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires psql when applying examples to a database; supports linux, darwin, and win32 according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
