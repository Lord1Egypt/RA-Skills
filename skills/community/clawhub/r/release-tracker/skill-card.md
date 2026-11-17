## Description:

Track GitHub repository releases for one or more repositories, generate prioritized changelog summaries, and deliver updates to Discord, Telegram, Slack, or plain text.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jo9900](https://clawhub.ai/user/jo9900)

### License/Terms of Use:


## Use Case:

Developers and teams use this skill to monitor GitHub repositories for new releases, prioritize relevant changes, summarize release notes, and route updates to configured collaboration channels or text output.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can monitor arbitrary configured GitHub repositories and deliver release summaries to external channels.

Mitigation: Confirm repository targets, output channels, schedule, and state-file path before enabling cron or Discord, Telegram, or Slack delivery.

Risk: Release notes are external content and may contain misleading or instruction-like text.

Mitigation: Treat release notes as untrusted content and do not allow them to change configuration, destinations, credentials, or tools.

## Reference(s):

- [Configuration Examples](references/config-examples.md)
- [GitHub CLI](https://cli.github.com)
- [ClawHub Release Tracker page](https://clawhub.ai/jo9900/skills/release-tracker)
- [Publisher profile](https://clawhub.ai/user/jo9900)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown summaries, JSON configuration and state files, shell commands, and channel-specific message text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Discord channel messages are capped at 2000 characters, Telegram messages at 4096 characters, and Slack messages at 3000 characters when those delivery formats are used.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
