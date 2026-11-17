## Description:

Automates waste collection reminders from user-defined JSON schedules and emits message blocks for an AI assistant to deliver through configured channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[apenklit](https://clawhub.ai/user/apenklit)

### License/Terms of Use:

MIT License

## Use Case:

External users and their AI assistants use this skill to maintain household waste pickup schedules, generate timely reminder messages, and track confirmation that containers have been put out.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configuration files may contain sensitive messaging targets, including webhook URLs.

Mitigation: Protect the config directory, avoid committing config.json or schedule.json, and treat Discord webhook URLs as secrets.

Risk: Malformed or influenced configuration could misroute automated reminder messages.

Mitigation: Review reminder targets before automated sending and prefer a version that emits structured JSON or validates recipients and channels.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/apenklit/skills/waste-reminder)
- [Skill documentation](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown setup guidance and plain text reminder blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reminder output uses SEND_TO and CHANNEL lines followed by the message body for delivery by the AI assistant.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
