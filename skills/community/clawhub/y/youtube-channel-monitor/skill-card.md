## Description:

Monitors subscribed YouTube channels for new videos, extracts Chinese or English subtitles, creates Chinese article summaries, publishes them to Telegraph, and sends Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[subwukong](https://clawhub.ai/user/subwukong)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to subscribe to YouTube channels and automatically turn new video subtitles into Chinese Telegraph articles with Telegram delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill automatically publishes generated content to external Telegraph and Telegram destinations.

Mitigation: Review the destination channel, posting behavior, and content workflow before enabling scheduled runs.

Risk: The artifact contains fixed Telegram credentials and stores local Telegraph access tokens.

Mitigation: Replace credentials with user-controlled secrets, rotate the exposed token, and limit token permissions before installation.

Risk: The workflow sends subtitle text to external services for translation and publication.

Mitigation: Confirm that public Telegraph posting and Jina translation are acceptable for the monitored content.

Risk: An hourly cron job can repeatedly run network actions and send notifications.

Mitigation: Enable the cron job only after confirming the schedule, proxy settings, dependencies, and notification target.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/subwukong/skills/youtube-channel-monitor)
- [Cron Setup](references/cron.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces Telegraph article links and Telegram notification text when new videos are processed.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
