## Description:

Curates five daily HOT items from GeekNews with emphasis on open source releases, fast-rising GitHub projects, developer tools, infrastructure, and AI/LLM topics, then formats and sends the brief to Telegram.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dongjus](https://clawhub.ai/user/dongjus)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineering teams use this skill to receive a concise daily Telegram brief of notable GeekNews posts, prioritizing open source launches, GitHub momentum, developer productivity, infrastructure, and AI/LLM stories. It can be run manually or scheduled for unattended daily delivery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Generated news briefs may be sent through Anthropic and Telegram.

Mitigation: Install only if external processing and Telegram delivery are acceptable for the intended content.

Risk: Setup uses persistent API credentials for Telegram, Anthropic, and optionally GitHub.

Mitigation: Use narrowly scoped credentials, avoid storing tokens in global shell startup files, and configure the optional GitHub token only when needed.

Risk: Scheduled execution can send messages unattended.

Mitigation: Review cron schedules and test delivery behavior before enabling automated sends.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/dongjus/skills/telegram-geeknews)
- [Telegram setup guide](references/telegram_setup.md)
- [GeekNews RSS feed](https://news.hada.io/rss)
- [GeekNews main page](https://news.hada.io/)
- [GeekNews topics](https://news.hada.io/topics)
- [Telegram BotFather](https://t.me/BotFather)
- [Anthropic Messages API](https://api.anthropic.com/v1/messages)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown brief with Telegram-compatible message text and inline shell commands for setup or scheduling]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Telegram messages should stay within the 4096 character message limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
