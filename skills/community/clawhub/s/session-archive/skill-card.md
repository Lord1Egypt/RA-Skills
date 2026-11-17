## Description:

Automatically saves conversation messages to a SQLite database with query and model usage statistics functionality.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18940111404](https://clawhub.ai/user/18940111404)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this plugin to keep a local SQLite archive of conversations, operation records, and model usage statistics for querying, auditing, or troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The plugin automatically stores full conversation contents and operational metadata in a long-lived local SQLite database.

Mitigation: Install only when local archiving is intended; choose a private database path, restrict file permissions, and define retention or deletion practices.

Risk: Archived sessions can include secrets, tool results, media paths, and usage or cost metadata.

Mitigation: Treat the database and its WAL/SHM sidecar files as sensitive, and avoid storing secrets in archived sessions.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/18940111404/skills/session-archive)
- [README](artifact/README.md)
- [Plugin Configuration Schema](artifact/openclaw.plugin.json)

## Skill Output:

**Output Type(s):** [Files, Configuration]

**Output Format:** [SQLite database records and JSON configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes messages, operations, and token usage to local SQLite tables; assembly and compaction return pass-through results.]

## Skill Version(s):

0.4.1 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
