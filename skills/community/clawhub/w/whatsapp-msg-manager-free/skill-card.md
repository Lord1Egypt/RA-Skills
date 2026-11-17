## Description: <br>
Helps agents send WhatsApp text messages, look up phone numbers, and browse message templates for lightweight personal or small-team message management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and small teams use this skill to send individual WhatsApp text notifications, retrieve WhatsApp Business phone number IDs, and inspect message template status through a connector-backed workflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants outbound WhatsApp messaging authority and the security evidence notes inconsistent confirmation guidance. <br>
Mitigation: Install it only when connecting a WhatsApp Business account through the connector plugin, and require a visible preview plus explicit confirmation before every message send. <br>
Risk: The security evidence flags broad activation wording that could draw the skill into generic API, webhook, or system-integration work. <br>
Mitigation: Use it only for the documented WhatsApp connector tasks: sending text messages, listing phone numbers, and browsing template status. <br>
Risk: Messages cannot be withdrawn after sending, so an incorrect recipient or message can create user-facing harm. <br>
Mitigation: Confirm the recipient phone number, country code, and full message content before invoking the send action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/whatsapp-msg-manager-free) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Code, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON parameters, YAML configuration examples, and short code snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a connector plugin, WhatsApp Business account access, and explicit user confirmation before message sends.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
