## Description:

Monitors ClawHub skill metrics and alerts when download growth exceeds configured thresholds, downloads or stars cross configured totals, or new top 10 skills appear.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gabriel-kaufman](https://clawhub.ai/user/gabriel-kaufman)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to watch ClawHub popularity signals, identify fast-moving skills, and surface relevant surge alerts through an agent with shell access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill contacts clawhub.ai to fetch skill popularity data.

Mitigation: Install and run it only in environments where outbound requests to clawhub.ai are acceptable.

Risk: The skill creates local state, configuration, profile, and optional cron log files under ~/.skill-surge-notifier by default.

Mitigation: Review the configured paths before use, override them with environment variables when needed, and add a cron entry only when periodic background checks are desired.

## Reference(s):

- [Trending Skill Finder on ClawHub](https://clawhub.ai/gabriel-kaufman/skills/skill-surge-notifier)
- [Publisher profile](https://clawhub.ai/user/gabriel-kaufman)
- [ClawHub skills directory](https://clawhub.ai/skills)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration]

**Output Format:** [Plain text and markdown-style CLI output with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Surge alerts include skill names, summaries, relevance scores when a profile is configured, download and star counts, trigger reasons, and install commands.]

## Skill Version(s):

1.0.9 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
