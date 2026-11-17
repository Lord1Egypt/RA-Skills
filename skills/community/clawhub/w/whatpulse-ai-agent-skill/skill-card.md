## Description:

Query WhatPulse computer usage statistics using natural language, including keystrokes, mouse activity, application screen time, network bandwidth, website tracking, uptime, and profiles from a local read-only SQLite database.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smitmartijn](https://clawhub.ai/user/smitmartijn)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to ask natural-language questions about their own WhatPulse activity data and receive read-only SQLite-backed summaries, comparisons, and tables.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can expose detailed private activity history, including application use, website activity, input statistics, bandwidth, and work patterns.

Mitigation: Use it locally where possible, restrict database file permissions, and only install it for users who consent to agent access to their WhatPulse history.

Risk: Remote or cloud-synced database snapshots can broaden access to sensitive activity data.

Mitigation: Avoid shared cloud folders, encrypt synced snapshots, limit retention, and document how to disable scheduled sync and delete old copies.

## Reference(s):

- [WhatPulse homepage](https://whatpulse.org)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with SQL-backed summaries, tables, and read-only sqlite3 command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires sqlite3 CLI and access to a local or synced WhatPulse SQLite database.]

## Skill Version(s):

1.0.0 (source: server release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
