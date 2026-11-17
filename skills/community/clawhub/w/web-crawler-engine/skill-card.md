## Description:

网页爬取工具 helps agents search and synchronize Discord archives, including channel messages, DMs, channel slices, and SQL-style counts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thcjp](https://clawhub.ai/user/thcjp)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation users can use this skill to query and synchronize Discord archive data for authorized channels, DMs, and message ranges. It is suited to archive search, freshness checks, and structured message summaries where the user has permission to access the data.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill scope is inconsistent and describes Discord archive access alongside broader web-crawling and SEO language.

Mitigation: Review the intended scope before installation and limit use to the Discord archive workflows that are actually authorized and needed.

Risk: DM archiving and message synchronization can expose private or sensitive communications.

Mitigation: Use only for accounts, servers, channels, and messages the operator is authorized to access, and avoid retaining sensitive content beyond the approved purpose.

Risk: The artifact advertises anti-bot evasion, cookie pool management, and IP rotation capabilities.

Mitigation: Avoid anti-bot, cookie-rotation, or IP-rotation workflows unless there is a clear lawful basis and explicit platform permission.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thcjp/skills/web-crawler-engine)
- [Publisher profile](https://clawhub.ai/user/thcjp)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with JSON examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return message lists, metadata, incremental sync records, SQL-style counts, and setup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
