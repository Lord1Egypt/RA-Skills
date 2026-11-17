## Description:

WhatsApp Business API integration with managed OAuth for sending messages, managing templates, and handling conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[notrellz](https://clawhub.ai/user/notrellz)

### License/Terms of Use:

MIT

## Use Case:

Developers and agents use this skill to interact with WhatsApp Business through Maton's managed OAuth gateway, including customer messaging, media handling, template management, and business profile operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can send real customer WhatsApp messages and perform destructive WhatsApp Business actions through a Maton-connected account.

Mitigation: Use a least-privilege Maton key, specify the intended Maton connection when multiple accounts exist, and require explicit confirmation before sending messages or updating or deleting profiles, connections, media, or templates.

Risk: MATON_API_KEY grants access to the connected account if it is exposed in logs, shared prompts, or shell output.

Mitigation: Store MATON_API_KEY as a secret or environment variable, avoid printing or sharing it, and rotate the key if exposure is suspected.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/notrellz/skills/whatsaoo)
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

**Output Format:** [Markdown with API examples and shell or code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires network access, MATON_API_KEY, and an active WhatsApp Business connection.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
