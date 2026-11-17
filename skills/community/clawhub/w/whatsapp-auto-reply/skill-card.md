## Description:

Automatically sends WhatsApp responses through an external messaging API using a target phone number and message content supplied by the agent.

This skill is ready for commercial/non-commercial use.

## Publisher:

[iqbalpak](https://clawhub.ai/user/iqbalpak)

### License/Terms of Use:

MIT-0

## Use Case:

External users, support teams, and personal assistant agents can use this skill to send WhatsApp replies when they already have a recipient phone number and approved message text. It is best treated as a message-sending workflow rather than a local reply-drafting helper.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send private phone numbers and message content to an external messaging service.

Mitigation: Require explicit user confirmation before each send and document the external provider and data shared.

Risk: Messages may be sent to an unintended recipient if the supplied phone number is wrong or unvalidated.

Mitigation: Validate recipient phone numbers and show the resolved recipient before sending.

Risk: The configured endpoint and unpinned dependencies may change behavior or expose data unexpectedly.

Mitigation: Use a trusted configurable endpoint, handle network failures, and pin or remove dependencies before deployment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/iqbalpak/skills/whatsapp-auto-reply)
- [Publisher Profile](https://clawhub.ai/user/iqbalpak)

## Skill Output:

**Output Type(s):** [API Calls, JSON, Text]

**Output Format:** [JSON object containing send status and external API response details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires message text, target phone number, and a WhatsApp API key available in the execution environment.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
