## Description:

Use notion, the WireCat CLI for Notion, from an agent — search a synced copy of Notion pages offline, read a page as Markdown live or from the copy, list databases and their data source ids and properties, with the owner's profile and JSON answers. Use when a task needs a Notion page or database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wirecat](https://clawhub.ai/user/wirecat)

### License/Terms of Use:

MIT-0

## Use Case:

Agents and developers use the Notion CLI to search a local copy of Notion content, read pages, inspect databases, sync content, and manage pages when authorized.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: ClawScan rates the skill suspicious because it documents page-changing Notion operations beyond its retrieval-focused description; scanner coverage is partial.

Mitigation: Confirm the write operations fit the task before use. Read pages before replacing their content, use dry runs where available, and pass the deletion authorization option only when deletion was requested.

## Reference(s):

- [Notion Cli release on ClawHub](https://clawhub.ai/wirecat/skills/wirecat-notion)
- [WireCat publisher profile](https://clawhub.ai/user/wirecat)

## Skill Output:

**Output Type(s):** [Shell commands, Markdown, JSON, Guidance]

**Output Format:** [Notion CLI commands and JSON responses; page content may be returned as Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Page reads can be truncated when blocks are unavailable; sync responses can report incomplete results.]

## Skill Version(s):

1.0.1 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
