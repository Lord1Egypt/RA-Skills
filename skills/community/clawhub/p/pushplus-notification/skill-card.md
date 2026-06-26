## Description: <br>
Send push notifications via the PushPlus HTTP API to WeChat, email, webhook, SMS, and other channels using a PUSHPLUS_TOKEN and shell/curl access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pcstx](https://clawhub.ai/user/pcstx) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and agents use this skill to send user-approved PushPlus notifications for alerts, reminders, task completion messages, reports, and logs across supported channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Notifications are transmitted through the third-party PushPlus service and can expose sensitive or confidential message content. <br>
Mitigation: Review the title, content, channel, recipient, webhook, and callback destination before approving each send; avoid transmitting passwords, API keys, personal data, or confidential logs unless explicitly accepted. <br>
Risk: The PUSHPLUS_TOKEN is a credential required to send messages. <br>
Mitigation: Do not display, log, store, or write the full token; mask it in any user-facing output and read only the PUSHPLUS_TOKEN line when using a .env file. <br>
Risk: The skill can send external notifications from an agent workflow. <br>
Mitigation: Require explicit user confirmation before each send and provide a concise summary of the message and delivery settings before executing the request. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pcstx/pushplus-notification) <br>
- [PushPlus official site](https://www.pushplus.plus) <br>
- [PushPlus single-send endpoint](https://www.pushplus.plus/send) <br>
- [PushPlus batch-send endpoint](https://www.pushplus.plus/batchSend) <br>
- [pushplus MCP server](https://www.npmjs.com/package/@perk-net/pushplus-mcp-server) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, API calls, guidance] <br>
**Output Format:** [Markdown with inline shell commands and JSON request examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a user-provided PUSHPLUS_TOKEN and user confirmation before sending each message.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact metadata reports 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
