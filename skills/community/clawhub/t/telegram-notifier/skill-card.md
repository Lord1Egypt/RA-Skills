## Description:

Send any agent report, alert, or message to a Telegram chat using your bot token; use it to deliver findings, briefings, security alerts, or task completions via Telegram with plain text or Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[infectit007](https://clawhub.ai/user/infectit007)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send selected agent reports, alerts, briefings, and task completion notices to a Telegram chat using a bot token and chat ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agent output sent through this skill leaves the local environment and is delivered to Telegram.

Mitigation: Send only selected, non-sensitive summaries; do not send secrets, credentials, personal data, regulated data, or full security reports unless that disclosure is approved.

Risk: Telegram bot tokens and chat IDs are required to send notifications.

Mitigation: Keep TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in environment variables or a secret manager, and avoid placing them in prompts, source text, logs, or notification bodies.

Risk: Long or unescaped Markdown messages may fail, truncate, or render incorrectly in Telegram.

Mitigation: Keep messages within Telegram's documented message limit, split long reports when needed, and escape Markdown special characters or use HTML formatting for content with many symbols.

## Reference(s):

- [Telegram BotFather](https://t.me/BotFather)
- [Telegram User Info Bot](https://t.me/userinfobot)
- [Telegram Bot API sendMessage endpoint](https://api.telegram.org/bot{token}/sendMessage)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Configuration]

**Output Format:** [Markdown with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides ready-to-paste snippets for Telegram sendMessage calls, environment variable setup, cron scheduling, and error handling.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
