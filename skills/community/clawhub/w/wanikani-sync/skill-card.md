## Description:

Sync WaniKani Japanese learning progress data from the API to local storage for analysis and insights.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mart1n-xyz](https://clawhub.ai/user/mart1n-xyz)

### License/Terms of Use:


## Use Case:

External WaniKani users and developers use this skill to back up learning progress, sync API data into SQLite, and analyze reviews, assignments, levels, SRS stages, accuracy, and difficult items offline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A WaniKani API token can be exposed if passed directly on the command line or stored in shell history.

Mitigation: Use WANIKANI_API_TOKEN instead of --token and keep the token private.

Risk: The local wanikani.db database may contain sensitive account and learning history.

Mitigation: Store the database in a private data directory and protect or delete it when it is no longer needed.

## Reference(s):

- [WaniKani homepage](https://www.wanikani.com)
- [WaniKani API token settings](https://www.wanikani.com/settings/personal_access_tokens)
- [WaniKani API v2](https://api.wanikani.com/v2)
- [WaniKani API Structure Reference](references/api-structure.md)
- [WaniKani Example Queries](references/example-queries.sql)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with shell commands, SQL examples, CLI text output, and a local SQLite database file]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 and WANIKANI_API_TOKEN; writes wanikani.db in the current directory or the configured data directory.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
