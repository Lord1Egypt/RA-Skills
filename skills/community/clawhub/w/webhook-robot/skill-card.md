## Description: <br>
Send messages to various webhook-based bots (WeCom, DingTalk, Feishu, etc.). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[takedwind](https://clawhub.ai/user/takedwind) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to send notifications through webhook-based chat bots and push services they control, including WeCom, DingTalk, Feishu, Bark, Telegram, PushDeer, ServerChan, GoCqHttp, and Gotify. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Messages and destination identifiers may expose sensitive information if sent to the wrong webhook, chat, or group. <br>
Mitigation: Verify destination URLs, chat IDs, group IDs, and message contents before sending, and avoid sending secrets or sensitive documents. <br>
Risk: Webhook keys and bot tokens can be exposed through shared logs, command history, or copied command lines. <br>
Mitigation: Avoid exposing credentials in shared logs or shell history, and rotate any webhook key or bot token that may have been exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/takedwind/webhook-robot) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Markdown, API calls, Configuration] <br>
**Output Format:** [Shell commands that send text or markdown message payloads to webhook APIs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and user-supplied webhook URLs, keys, bot tokens, chat IDs, or group IDs for the selected service.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
