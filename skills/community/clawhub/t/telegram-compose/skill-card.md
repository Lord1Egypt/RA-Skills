## Description: <br>
Formats substantive Telegram replies into readable HTML messages and sends them through a configured Telegram bot. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tmchow](https://clawhub.ai/user/tmchow) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to deliver longer or structured Telegram updates, alerts, summaries, reports, and notifications through a specified configured bot account. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends content to Telegram through a configured bot token. <br>
Mitigation: Install it only when Telegram delivery is intended, and scope bot accounts and chat IDs to the intended conversations. <br>
Risk: Sensitive content included in agent output may be delivered to Telegram. <br>
Mitigation: Avoid sending secrets or private data unless that content is intended to appear in the target Telegram chat. <br>
Risk: Malformed Telegram HTML can cause message delivery to fail or require plain-text fallback. <br>
Mitigation: Escape text content before sending and use the skill's retry and fallback behavior when Telegram rejects formatting. <br>


## Reference(s): <br>
- [Telegram Compose on ClawHub](https://clawhub.ai/tmchow/telegram-compose) <br>
- [Telegram Bot API endpoint](https://api.telegram.org) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, API Calls, Guidance] <br>
**Output Format:** [Telegram HTML message delivery with a message_id or error summary returned to the caller] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires an explicit bot account, chat ID, and optional thread ID; messages over Telegram limits are split before delivery.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
