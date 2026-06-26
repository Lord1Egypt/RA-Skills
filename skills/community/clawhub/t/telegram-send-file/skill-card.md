## Description: <br>
Send local files, URLs, or reusable Telegram file_ids into a Telegram chat via the Bot API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangwllu](https://clawhub.ai/user/wangwllu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to deliver selected local files, URLs, or known Telegram file IDs from an agent workflow into a Telegram chat or topic. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Files can be sent to the wrong Telegram chat or topic if the target is auto-detected incorrectly. <br>
Mitigation: Verify the resolved chat_id and topic_id before sending sensitive or important material. <br>
Risk: Telegram bot tokens grant send access through the configured bot. <br>
Mitigation: Keep the bot token private, restrict bot access to intended chats, and rotate the token if exposure is suspected. <br>
Risk: Selected files, credentials, regulated data, or internal-only URLs could be disclosed through Telegram. <br>
Mitigation: Do not send secrets, regulated data, or internal-only URLs unless the destination and authorization are confirmed. <br>


## Reference(s): <br>
- [Telegram Bot API File Sending Reference](references/api_reference.md) <br>
- [Telegram Send File ClawHub Release](https://clawhub.ai/wangwllu/telegram-send-file) <br>
- [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot) <br>
- [OpenClaw](https://github.com/wangwllu/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, API Calls, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and CLI status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Sends one file or a sequential batch; reports Telegram message metadata or an error status when invoked.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
