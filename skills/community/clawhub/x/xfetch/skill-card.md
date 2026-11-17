## Description:

Use xfetch CLI to fetch X/Twitter data including tweets, user profiles, search results, timelines, lists, DMs, notifications, and exports to CSV, JSON, JSONL, or SQLite.

This skill is ready for commercial/non-commercial use.

## Publisher:

[feiskyer](https://clawhub.ai/user/feiskyer)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to retrieve, inspect, and export X/Twitter content through the xfetch CLI after authenticated access is configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Authenticated X/Twitter cookies or tokens can expose private account data, including DMs, bookmarks, notifications, and timelines.

Mitigation: Use only with explicit user consent, prefer a pinned and audited xfetch version, and avoid placing live session tokens in command lines or chat.

Risk: Large scraping or export requests may collect more data than intended.

Mitigation: Scope commands narrowly, prefer page limits over unbounded collection, and review export destinations before execution.

Risk: The evidence does not clearly identify the exact executable package reviewed.

Mitigation: Verify and pin the xfetch executable source and version before installation or execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/feiskyer/skills/xfetch)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce commands that write JSON, JSONL, CSV, or SQLite export files when requested.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
