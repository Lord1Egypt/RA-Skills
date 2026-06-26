## Description: <br>
A WhatsApp automation skill that accepts a phone number and message and sends the message through an external WhatsApp API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[iqbalpak](https://clawhub.ai/user/iqbalpak) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agent builders can use this skill to automate WhatsApp response workflows for personal assistant and customer-support scenarios. Deployments should treat it as message-sending capable and require controls before live use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release evidence reports a mismatch between documentation that describes reply drafting and code that sends WhatsApp messages through an external API using a WhatsApp API key. <br>
Mitigation: Review the artifact as message-sending capable, verify the external API provider and key permissions, and require explicit user confirmation before sending. <br>
Risk: Automated sending to phone numbers can create unintended messages or excessive outbound traffic if the agent is not constrained. <br>
Mitigation: Enforce recipient allowlists, rate limits, and operational monitoring outside the skill before enabling live execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/iqbalpak/whatsapp-auto-reply) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, text] <br>
**Output Format:** [JSON object containing status and api_response fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger an external WhatsApp API call that sends a message to a phone number.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata; artifact manifest declares 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
