## Description:

Create and manage Telegram bots for notifications, automation, customer support, group management, and interactive commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to scaffold and run Telegram bots that handle commands, messages, webhooks, polling, inline interactions, group administration, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bot script can automatically install an unpinned runtime dependency.

Mitigation: Install and pin python-telegram-bot in an isolated virtual environment or container before running the script.

Risk: Telegram bot tokens may be exposed when passed as command-line arguments.

Mitigation: Use a safer secret mechanism for tokens and avoid storing or sharing command histories that contain credentials.

Risk: Custom handler files execute trusted Python code inside the bot process.

Mitigation: Only load handler files from trusted sources after review.

Risk: Group administration examples can remove users from chats when the bot has sufficient permissions.

Mitigation: Restrict admin IDs, review group permissions, and test moderation behavior in a controlled chat before deployment.

## Reference(s):

- [Telegram Bot Examples](references/examples.md)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [python-telegram-bot](https://python-telegram-bot.org)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration instructions]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Telegram bot setup steps, handler examples, command usage, and configuration guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
