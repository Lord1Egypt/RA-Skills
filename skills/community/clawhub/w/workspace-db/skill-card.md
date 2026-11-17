## Description:

Workspace Documentation and Tree Database Manager. SQLite-based indexing for all documentation, files, and directory structures with CSV/JSON export capabilities.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and workspace maintainers use this skill to index OpenClaw workspace documentation, skill metadata, symlinks, and directory trees into local SQLite databases with CSV and JSON exports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Workspace indexing can create or update local database and export files that summarize documentation, paths, skills, and symlinks.

Mitigation: Install only in workspaces where local indexing and generated CSV, JSON, and SQLite files are acceptable.

Risk: The optional maintainer setup references an updater package that creates a recurring cron job.

Mitigation: Review and pin the maintainer package separately, understand the scheduled command, and confirm how to remove the cron job before enabling it.

## Reference(s):

- [Workspace Database Manager ClawHub page](https://clawhub.ai/kikikari/skills/workspace-db)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands and SQL examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may lead to local SQLite database files and CSV or JSON export files being created or updated in the workspace.]

## Skill Version(s):

1.0.0 (source: package.json and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
