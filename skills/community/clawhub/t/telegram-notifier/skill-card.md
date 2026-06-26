## Description: <br>
Send any agent report, alert, or message to a Telegram chat using your bot token. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[infectit007](https://clawhub.ai/user/infectit007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill to send findings, briefings, alerts, and task-completion messages to a configured Telegram chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agent-generated reports may unintentionally send secrets or private information to the configured Telegram chat. <br>
Mitigation: Review or redact sensitive report content before sending and use a dedicated bot and chat for these notifications. <br>
Risk: A bot token can be misused if it is exposed in prompts, logs, or shared code snippets. <br>
Mitigation: Keep TELEGRAM_BOT_TOKEN secret and provide it through the runtime environment rather than hard-coding it. <br>
Risk: The cron example can create recurring outbound notifications if enabled unintentionally. <br>
Mitigation: Add the cron schedule only when recurring notifications are intended and review the prompt before deployment. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/infectit007/telegram-notifier) <br>
- [Publisher Profile](https://clawhub.ai/user/infectit007) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Telegram User Info Bot](https://t.me/userinfobot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown with Python and bash snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Telegram messages are limited to 4096 characters; long reports should be truncated or split.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
