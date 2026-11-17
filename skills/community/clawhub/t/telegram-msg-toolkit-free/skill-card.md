## Description: <br>
Helps agents use the Telegram Bot API to send text, images, files, locations, polls, and forwarded messages, query chat information, and manage basic bot commands. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to operate a Telegram bot for deployment notifications, reports, polls, basic chat lookup, and bot command management from an AI agent. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The agent may send, edit, delete, or forward live Telegram messages if given a valid bot token and execution permission. <br>
Mitigation: Review every message body, file, target chat ID, and intended Telegram method before execution. <br>
Risk: A leaked Telegram bot token can let unauthorized users control the bot. <br>
Mitigation: Keep TELEGRAM_BOT_TOKEN in the environment rather than files, use a least-privilege bot, and rotate the token if exposure is suspected. <br>
Risk: Bot administrator permissions increase the impact of deletion and invite-link operations. <br>
Mitigation: Avoid granting administrator permissions unless deletion or invite-link management is required for the use case. <br>


## Reference(s): <br>
- [Telegram Bot API endpoint](https://api.telegram.org) <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/telegram-msg-toolkit-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline curl commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce live Telegram Bot API requests when the agent is permitted to execute shell commands and network calls.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
