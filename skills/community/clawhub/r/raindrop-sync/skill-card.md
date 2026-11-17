## Description:

Sync and process bookmarks from Raindrop.io for fetching new bookmarks, analyzing saved content, and syncing bookmarks to a knowledge base.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zerone0x](https://clawhub.ai/user/zerone0x)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to fetch Raindrop.io bookmarks by time window or collection, inspect saved links, and optionally prepare bookmark data for knowledge-base updates.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Bookmark-derived web content may be written into local memory or knowledge-base files without enough review.

Mitigation: Review fetched bookmark items and extracted page content before allowing writes to memory or knowledge-base files.

Risk: Automatic cron or heartbeat syncing can create persistent updates from saved web pages without enough user control.

Mitigation: Start with manual fetches and enable scheduled syncing only after confirming token scope, destination files, and content handling.

## Reference(s):

- [Raindrop.io REST API](https://api.raindrop.io/rest/v1)
- [Raindrop.io integrations settings](https://app.raindrop.io/settings/integrations)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON bookmark output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires RAINDROP_TOKEN; optional --since, --collection, and --output parameters control the fetch.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
