## Description: <br>
Send images to Telegram via direct Bot API using curl, bypassing OpenClaw's broken image delivery pipeline issue #63137. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niccoreyes](https://clawhub.ai/user/niccoreyes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, engineers, and agent users use this skill to send selected images or files directly to Telegram chats with curl when the native OpenClaw Telegram image path is unsuitable. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected images or files may contain sensitive, confidential, or regulated data before they are sent to Telegram. <br>
Mitigation: Verify the target chat ID and file path before sending, and avoid sending sensitive screenshots or regulated data unless the user is authorized to share them through Telegram. <br>
Risk: Telegram bot tokens stored in .env files or shell startup files can be exposed or reused outside the intended session. <br>
Mitigation: Use a dedicated bot token, restrict .env file permissions, avoid committing secrets, and prefer per-session credential loading over global shell startup files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/niccoreyes/telegram-direct-send) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Telegram User Info Bot](https://t.me/userinfobot) <br>
- [Telegram Raw Data Bot](https://t.me/RawDataBot) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and curl command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus Telegram bot token and chat ID environment variables; commands send user-selected files through Telegram Bot API when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
