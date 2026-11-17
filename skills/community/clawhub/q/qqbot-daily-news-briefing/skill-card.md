## Description:

Generates and delivers automated daily tech and finance news briefings with AI commentary via QQ, Telegram, or Discord using Baidu API or DuckDuckGo search.

This skill is ready for commercial/non-commercial use.

## Publisher:

[propn](https://clawhub.ai/user/propn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to generate scheduled daily technology and finance news briefings, add commentary, and deliver reports through OpenClaw-supported messaging channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Delivery scripts may send generated reports to a hardcoded QQ recipient instead of the user-configured recipient.

Mitigation: Review and change the delivery scripts before installation; require an explicit user-controlled recipient and fail delivery when no recipient is configured.

Risk: Automated cron delivery can repeatedly send briefings to an unintended destination.

Mitigation: Keep cron disabled until a manual dry run confirms the exact destination, channel, content, and logs.

Risk: Attachment delivery may send the wrong local report if the file path is not validated.

Mitigation: Validate the generated briefing path before sending and restrict delivery to the expected daily report location.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/propn/skills/qqbot-daily-news-briefing)
- [Configuration Guide](references/CONFIGURATION.md)

## Skill Output:

**Output Type(s):** [markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown briefing files with command and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Briefings include categorized article summaries, source links, commentary, and delivery message previews.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
