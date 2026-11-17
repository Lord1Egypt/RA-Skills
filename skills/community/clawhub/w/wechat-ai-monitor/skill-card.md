## Description:

Monitors configured WeChat-related RSS feeds for AI and technology articles, filters recent items by keywords, and generates Markdown monitoring reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pyh-pan](https://clawhub.ai/user/pyh-pan)

### License/Terms of Use:

MIT

## Use Case:

Developers, analysts, and content monitoring users can use this skill to watch selected RSS feeds for AI and technology content from the last 24 hours and produce a daily Markdown report. It is useful for lightweight tracking of configured sources where the user controls the feed list.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts each enabled RSS URL from the user's machine.

Mitigation: Configure only trusted HTTPS feeds and keep accounts.json under user control.

Risk: Generated reports may include titles, summaries, and links from untrusted feeds.

Mitigation: Treat report content from untrusted feeds as untrusted Markdown before sharing or rendering it.

Risk: Reports are written to the user's local configuration directory.

Mitigation: Review the configured output location and local file permissions before routine use.

## Reference(s):

- [WeChat AI Monitor on ClawHub](https://clawhub.ai/pyh-pan/skills/wechat-ai-monitor)

## Skill Output:

**Output Type(s):** [Markdown, Text, Files, Configuration]

**Output Format:** [Markdown report files with terminal status text and JSON-based feed configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes reports under ~/.config/wechat-monitor/reports and reads feed settings from ~/.config/wechat-monitor/accounts.json.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
