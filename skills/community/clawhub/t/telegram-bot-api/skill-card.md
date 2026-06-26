## Description: <br>
Build Telegram bots with correct API calls, message formatting, keyboards, and webhook setup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation builders use this skill to create and operate Telegram bots, including Bot API requests, message formatting, keyboards, media handling, and webhook or polling setup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Telegram bot tokens and bot-sent data are sensitive and are included in Bot API requests. <br>
Mitigation: Use test bots first, keep ~/telegram-bot-api/ private, avoid plaintext production tokens where possible, and rotate any token that is exposed. <br>
Risk: Bot actions such as sending media, changing webhooks, deleting messages, banning users, requesting contact or location data, or using drop_pending_updates can affect users or discard updates. <br>
Mitigation: Review these commands before execution and confirm the target bot, chat, webhook URL, and update-handling behavior. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/telegram-bot-api) <br>
- [Skill Homepage](https://clawic.com/skills/telegram-bot-api) <br>
- [Setup Process](setup.md) <br>
- [All API Methods](methods.md) <br>
- [Message Formatting](formatting.md) <br>
- [Keyboards and Buttons](keyboards.md) <br>
- [Webhooks and Polling](webhooks.md) <br>
- [Media Handling](media.md) <br>
- [Error Codes](errors.md) <br>
- [Memory Template](memory-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration, API calls] <br>
**Output Format:** [Markdown with inline shell commands, JSON examples, and code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May propose local bot configuration files under ~/telegram-bot-api/ and curl requests to the Telegram Bot API.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
