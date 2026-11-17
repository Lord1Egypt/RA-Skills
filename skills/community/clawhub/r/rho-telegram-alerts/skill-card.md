## Description:

Send formatted trading alerts, portfolio updates, and market signals via Telegram, including price alerts, stop-loss notifications, win/loss reporting, and scheduled summaries.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jamierossouw](https://clawhub.ai/user/jamierossouw)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to draft Telegram notifications for trading events, price thresholds, portfolio summaries, stop-loss warnings, win/loss streaks, and scheduled trading reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram messages may expose sensitive trading, portfolio, holdings, or trading-behavior information.

Mitigation: Send only information suitable for Telegram, restrict the bot and chat to intended recipients, and avoid unnecessary sensitive details in scheduled reports.

Risk: The Telegram bot token and chat ID can enable unauthorized message delivery if exposed.

Mitigation: Keep TELEGRAM_BOT_TOKEN private, store secrets outside committed files, and do not commit .env files.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jamierossouw/skills/rho-telegram-alerts)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown text with Telegram-ready alert content and setup guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID for Telegram delivery.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter states 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
