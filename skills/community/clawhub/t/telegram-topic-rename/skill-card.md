## Description: <br>
Renames Telegram forum topics and optionally changes topic icons through the Telegram Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wwjjhh1995](https://clawhub.ai/user/wwjjhh1995) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and chat administrators use this skill to rename Telegram forum topics and select matching topic icons from an agent workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The Telegram bot token grants access to make real changes in chats where the bot has permissions. <br>
Mitigation: Use a dedicated bot with minimal permissions and keep TELEGRAM_BOT_TOKEN out of logs and shared files. <br>
Risk: Supplying the wrong chat_id or thread_id can rename the wrong Telegram topic. <br>
Mitigation: Verify the target chat and thread identifiers before running the rename script. <br>


## Reference(s): <br>
- [Telegram topic icons reference](references/icons.md) <br>
- [ClawHub release page](https://clawhub.ai/wwjjhh1995/telegram-topic-rename) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and environment configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TELEGRAM_BOT_TOKEN plus Telegram chat and thread identifiers.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
