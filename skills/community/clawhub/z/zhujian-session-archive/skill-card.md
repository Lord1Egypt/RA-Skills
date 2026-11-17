## Description:

Automatically saves OpenClaw conversation messages, operation records, and token usage to a local SQLite database for later querying and statistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18940111404](https://clawhub.ai/user/18940111404)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users install this plugin when they need a persistent local archive of chat messages, operation records, and model usage statistics. It is useful for auditing, querying prior sessions, and analyzing usage over time.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Full conversation history can be retained on disk in the local SQLite archive.

Mitigation: Protect the database file from other users and backups, avoid entering secrets in archived sessions, and define a deletion or retention process before deployment.

Risk: The archive may grow over time as messages, operations, and token usage are recorded.

Mitigation: Choose an appropriate database path, monitor storage use, and rotate or purge old records according to local policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/18940111404/skills/zhujian-session-archive)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)
- [openclaw.plugin.json](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [Files, Text, Configuration]

**Output Format:** [SQLite database records and configuration fields]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local SQLite archive at the configured database path.]

## Skill Version(s):

0.5.0 (source: server release evidence and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
