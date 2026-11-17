## Description: <br>
This skill helps agents use WhatsApp CLI to send text or file messages, list chats, search message history, and complete QR-based authentication for third-party WhatsApp communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, individual developers, and agents use this skill to send WhatsApp text or file messages, check chats, and search synced message history through wacli. It is intended for explicitly requested third-party communications, not for routine agent-user conversation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unrelated SEO trigger text could cause an agent to select this WhatsApp messaging skill for the wrong task. <br>
Mitigation: Remove the SEO invocation language before publishing or relying on automatic skill routing, and require explicit user intent to operate WhatsApp through wacli. <br>
Risk: The skill can send messages or files to unintended WhatsApp recipients if recipient, message, or path details are ambiguous. <br>
Mitigation: Confirm recipients, message content, target chats, and file paths before executing send commands. <br>
Risk: The wacli storage directory can contain WhatsApp credentials, session data, chat metadata, and synced messages. <br>
Mitigation: Protect ~/.wacli/ as sensitive account data, restrict local access, and unlink the WhatsApp device if credentials may be exposed. <br>
Risk: Chat search commands can expose private message history beyond the user's intended scope. <br>
Mitigation: Confirm the search request, chat scope, date range, and output volume before running message-history searches. <br>
Risk: Rapid or unsolicited WhatsApp sending can trigger rate limits or account enforcement. <br>
Mitigation: Throttle sends, avoid bulk or unsolicited outreach, and prefer replies to existing conversations. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and JSON-shaped command results.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may operate on local WhatsApp credentials, chat metadata, message history, and file paths through wacli.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
