## Description: <br>
Capture website screenshots and send to Telegram via direct API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[niccoreyes](https://clawhub.ai/user/niccoreyes) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture screenshots of approved web pages and send them to a configured Telegram chat through direct API calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Target URLs, screenshots, and captions are sent to the Snap screenshot service and Telegram. <br>
Mitigation: Use only approved public or non-sensitive pages, and avoid internal, authenticated, personal, or regulated content unless approved. <br>
Risk: Telegram bot tokens, chat IDs, and Snap API keys are sensitive credentials. <br>
Mitigation: Use a dedicated Telegram bot and limited chat, verify the chat ID, and keep .env private with restrictive permissions. <br>
Risk: Shell-profile loading or cron automation can persist credentials or schedule screenshot posting. <br>
Mitigation: Enable persistent loading or scheduled posting only when needed and reviewed. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/niccoreyes/screenshot-telegram-direct) <br>
- [Telegram BotFather](https://t.me/BotFather) <br>
- [Telegram user info bot](https://t.me/userinfobot) <br>
- [Snap API registration endpoint](https://snap.llm.kaveenk.com/api/register) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl plus TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, and SNAP_API_KEY environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
