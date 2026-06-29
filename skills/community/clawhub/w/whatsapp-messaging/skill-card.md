## Description: <br>
Send WhatsApp messages, manage templates, handle media, and automate WhatsApp Business messaging workflows via the WhatsApp Business API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hith3sh](https://clawhub.ai/user/hith3sh) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and business teams use this skill to connect a WhatsApp Business account through ClawLink, inspect available WhatsApp tools, manage templates and media, and send customer messages through explicit tool calls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-connected WhatsApp Business access and sensitive credentials managed through ClawLink. <br>
Mitigation: Install and invoke it only for WhatsApp Business API tasks, use the connected account intentionally, and avoid sharing production tokens in chat. <br>
Risk: WhatsApp message-sending tools can contact real customers and messages cannot be recalled. <br>
Mitigation: Preview and explicitly confirm recipients, message content, phone number IDs, and media before executing write operations. <br>
Risk: WhatsApp opt-in, template approval, and 24-hour customer service window rules can block or make messages inappropriate. <br>
Mitigation: Verify account permissions, recipient opt-in status, approved templates, and customer service window requirements before sending. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/hith3sh/whatsapp-messaging) <br>
- [WhatsApp Business API Documentation](https://developers.facebook.com/docs/whatsapp/cloud-api) <br>
- [WhatsApp Business API Reference](https://developers.facebook.com/docs/whatsapp/api/messages) <br>
- [Message Templates Guidelines](https://developers.facebook.com/docs/whatsapp/message-templates) <br>
- [ClawLink OpenClaw Docs](https://docs.claw-link.dev/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration, code, markdown] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool-call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes setup, discovery, execution, and troubleshooting guidance for WhatsApp Business API workflows through ClawLink.] <br>

## Skill Version(s): <br>
1.0.6 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
