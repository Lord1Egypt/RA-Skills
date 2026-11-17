## Description:

WhatsApp Business API integration with managed OAuth. Send messages, manage templates, and handle conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[raidan-ai](https://clawhub.ai/user/raidan-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to connect agents to WhatsApp Business through Maton-managed OAuth, send customer messages, manage templates and media, and administer business profile or connection workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Live WhatsApp sends, template changes, profile changes, media deletion, or connection deletion can affect production customer accounts.

Mitigation: Use the skill only with authorized WhatsApp Business accounts and require explicit human approval before these actions are executed.

Risk: The MATON_API_KEY can grant access to connected business accounts if exposed in terminal output, logs, or support materials.

Mitigation: Verify only that the key is set, redact logs, never print or share the key, and rotate it if exposure is suspected.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/raidan-ai/skills/whatsapp-business-1-0-3)
- [WhatsApp Business API Overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)
- [Send Messages](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages)
- [Message Templates](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)
- [Media](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/media)
- [Phone Numbers](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/phone-numbers)
- [Business Profiles](https://developers.facebook.com/docs/whatsapp/cloud-api/reference/business-profiles)
- [Webhooks](https://developers.facebook.com/docs/whatsapp/cloud-api/webhooks)
- [Error Codes](https://developers.facebook.com/docs/whatsapp/cloud-api/support/error-codes)
- [Maton](https://maton.ai)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline HTTP, Python, JavaScript, and shell examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and authorized WhatsApp Business connections.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
