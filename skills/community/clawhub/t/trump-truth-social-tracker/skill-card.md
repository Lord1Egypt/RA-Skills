## Description:

Tracks Donald Trump's Truth Social posts by fetching CNN's public archive, syncing posts with content into a local SQLite database, and supporting queries, statistics, and market-impact keyword alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[laigen](https://clawhub.ai/user/laigen)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to maintain a local searchable archive of Trump Truth Social posts, inspect engagement statistics, and generate keyword-based market-impact alerts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill fetches public social-media archive content and can include post excerpts in generated reports.

Mitigation: Treat report excerpts as untrusted public content and review them before using them in decisions or downstream automation.

Risk: Using a custom JSON source can change the data being stored and analyzed.

Mitigation: Use the default CNN archive unless the replacement --json-url source is trusted.

Risk: The --write-report option creates durable markdown alert files in the local workspace.

Mitigation: Enable --write-report only when persistent alert records are intended.

## Reference(s):

- [CNN Truth Social Archive](https://ix.cnn.io/data/truth-social/truth_archive.json)
- [ClawHub Skill Page](https://clawhub.ai/laigen/skills/trump-truth-social-tracker)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, SQL snippets, optional JSON command output, and optional markdown alert reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates or updates a local SQLite database and can append keyword alert summaries to a markdown report when requested.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
