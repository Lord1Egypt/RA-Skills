## Description:

Build Telegram bots with correct API calls, message formatting, keyboards, and webhook setup.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and automation builders use this skill to create and operate Telegram bots, including sending messages, handling updates, configuring keyboards, working with media, and choosing webhook or polling patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Telegram bot tokens may be stored in local Markdown configuration files or exposed in logs, messages, or webhook URLs.

Mitigation: Store tokens in environment variables, an OS keychain, or a secret manager; never display tokens to users; avoid putting tokens in webhook URLs.

Risk: Webhook handlers can accept spoofed requests if they do not verify Telegram's secret-token header.

Mitigation: Set a webhook secret token and validate the X-Telegram-Bot-Api-Secret-Token header for every webhook request.

Risk: Full update payload logging can capture message content, contacts, locations, media metadata, or other user data.

Mitigation: Redact sensitive payload fields, minimize logs, and define consent and retention rules before collecting personal data.

Risk: Unreviewed generated API calls can send messages, media, or commands to Telegram chats using the configured bot token.

Mitigation: Review generated requests and target chat IDs before execution, and test with a low-privilege bot or private chat first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ivangdavila/skills/telegram-bot-api)
- [Clawic skill homepage](https://clawic.com/skills/telegram-bot-api)
- [Telegram Bot API endpoint pattern](https://api.telegram.org/bot{TOKEN}/{METHOD})
- [Setup guidance](artifact/setup.md)
- [API methods](artifact/methods.md)
- [Message formatting](artifact/formatting.md)
- [Keyboards and buttons](artifact/keyboards.md)
- [Webhooks and polling](artifact/webhooks.md)
- [Media handling](artifact/media.md)
- [Error codes](artifact/errors.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with API examples, JSON payloads, shell commands, and configuration snippets.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Telegram Bot API calls and local bot configuration guidance; users should protect bot tokens and review requests before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
