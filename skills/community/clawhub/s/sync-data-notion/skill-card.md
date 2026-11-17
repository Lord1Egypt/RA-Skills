## Description:

Syncs CSV, JSON, or REST API data with a Notion database, including schema validation, dry-run previews, incremental updates, reverse export, and structured per-record reporting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operations teams use this skill to keep external CSV, JSON, or REST API records synchronized with a Notion database. It supports initial full syncs, recurring incremental syncs, dry-run previews before writes, and Notion-to-external reverse export.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can modify Notion database records and can export Notion content through reverse sync.

Mitigation: Use a least-privilege Notion integration token, run dry-run mode against a test database first, require explicit approval for production data, and only reverse sync to trusted destinations.

Risk: Persistence of last-run state and under-scoped documentation can make sync state harder to audit.

Mitigation: Review the stored last-run path, keep operation logs with timestamps and record counts, and verify each run's structured summary before scheduling recurring syncs.

Risk: Unsupported Notion property types, validation errors, or rate limits can cause partial sync results.

Mitigation: Validate the source schema against the Notion database schema before writes, report every skipped or failed record with a reason, and retry rate-limited requests according to the API response.

## Reference(s):

- [Sync Data Notion reference index](references/index.md)
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/sync-data-notion)
- [Metadata source: MiniMax-AI/skills](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, API calls, JSON]

**Output Format:** [Markdown guidance with API request examples and structured JSON summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include dry-run change previews, field-mapping tables, per-record failure reports, and last-run timestamp guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata lists 1.0.1 and changelog lists 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
