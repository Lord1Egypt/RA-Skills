## Description: <br>
Twilio API integration with managed OAuth for SMS, voice calls, phone numbers, and communications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byungkyu](https://clawhub.ai/user/byungkyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and external users use this skill to have an agent work with Twilio accounts, messages, voice calls, phone numbers, applications, queues, addresses, and usage records through Maton's managed OAuth proxy. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can access sensitive Twilio account data and perform account-changing actions through the connected account. <br>
Mitigation: Review each request before execution and require explicit confirmation for sending messages, placing calls, changing webhooks, deleting resources, or reading communications history. <br>
Risk: The MATON_API_KEY grants access through Maton's proxy and could expose the connected Twilio account if leaked. <br>
Mitigation: Keep MATON_API_KEY private, store it as a secret, and avoid commands or logs that print the key. <br>
Risk: Users with multiple Twilio connections could target the wrong account. <br>
Mitigation: Specify the intended connection with the Maton-Connection header when more than one Twilio connection exists. <br>
Risk: Messages and calls can reach external recipients and may create compliance, privacy, or billing impact. <br>
Mitigation: Confirm recipients, sender numbers, message or call content, and authorization before creating communication actions. <br>


## Reference(s): <br>
- [ClawHub Twilio Skill Page](https://clawhub.ai/byungkyu/twilio-api) <br>
- [Twilio API Overview](https://www.twilio.com/docs/usage/api) <br>
- [Twilio Messages API](https://www.twilio.com/docs/messaging/api/message-resource) <br>
- [Twilio Calls API](https://www.twilio.com/docs/voice/api/call-resource) <br>
- [Twilio Incoming Phone Numbers API](https://www.twilio.com/docs/phone-numbers/api/incomingphonenumber-resource) <br>
- [Twilio Applications API](https://www.twilio.com/docs/usage/api/applications) <br>
- [Twilio Usage Records API](https://www.twilio.com/docs/usage/api/usage-record) <br>


## Skill Output: <br>
**Output Type(s):** [API Calls, Code, Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline HTTP, bash, Python, JavaScript, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and a connected Twilio account; write operations require explicit user approval.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter metadata.version is 1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
