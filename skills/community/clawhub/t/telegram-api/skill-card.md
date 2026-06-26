## Description: <br>
Telegram Bot API integration with managed authentication for sending messages, managing chats, handling updates, and interacting with users through a connected Telegram bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to have an agent work with Telegram Bot API workflows through Maton-managed authentication. It supports bot messaging, chat and update handling, bot commands, webhook changes, and connection management. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a Maton API key and can act through the connected Telegram bot. <br>
Mitigation: Keep MATON_API_KEY private and avoid sharing terminal output or logs that expose credentials. <br>
Risk: Write operations can send, edit, delete, or reconfigure Telegram bot resources. <br>
Mitigation: Approve sends, deletes, webhook changes, command changes, or connection changes only after checking the exact target and effect. <br>
Risk: Multiple Telegram bot connections can route an action to the wrong bot if unspecified. <br>
Mitigation: Use the Maton-Connection header when multiple bots are connected. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byungkyu/telegram-api) <br>
- [Telegram Bot API Documentation](https://core.telegram.org/bots/api) <br>
- [Telegram Bot API Available Methods](https://core.telegram.org/bots/api#available-methods) <br>
- [Telegram Bot API Formatting Options](https://core.telegram.org/bots/api#formatting-options) <br>
- [Telegram Bot Commands](https://core.telegram.org/bots/api#setmycommands) <br>
- [Maton](https://maton.ai) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active Telegram connection.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
