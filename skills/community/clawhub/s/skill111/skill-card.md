## Description:

WhatsApp Business API integration with managed OAuth for sending messages, managing templates, and handling conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kenhee350-a11y](https://clawhub.ai/user/kenhee350-a11y)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to guide agents through WhatsApp Business API tasks such as sending customer messages, managing message templates, handling media, maintaining phone numbers, and updating business profiles through Maton-managed OAuth.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Agents can send customer messages or change WhatsApp Business resources through the Maton gateway.

Mitigation: Require explicit user confirmation, validate recipients and resource identifiers, and review message content before executing write or send actions.

Risk: The skill includes troubleshooting that can reveal whether MATON_API_KEY is set.

Mitigation: Do not print, log, paste, or share MATON_API_KEY; store it in a secret manager or protected environment variable.

Risk: Connection, media, template, and profile operations can delete or alter business resources.

Mitigation: Use least-privilege Maton credentials and require confirmation before delete or update operations.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/kenhee350-a11y/skills/skill111)
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages)
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- [Phone Numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers)
- [Business Profiles](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles)
- [Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)
- [Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash, Python, JavaScript, JSON, and HTTP examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access and a valid MATON_API_KEY.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
