## Description:

Guides agents in using a connected WhatsApp Business account to send messages, manage templates and media, and handle customer conversations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[byungkyu](https://clawhub.ai/user/byungkyu)

### License/Terms of Use:

MIT-0

## Use Case:

Business operators and developers use this skill to guide approved WhatsApp Business messaging, template management, and account interactions through their connected account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Sending messages to unintended recipients can have business, privacy, or reputation impacts.

Mitigation: Confirm the recipient and each write action before sending.

Risk: Broad or persistent automation can repeatedly act on the connected business account.

Mitigation: Enable automation only when explicitly requested and review its scope before use.

Risk: Exposed Maton or provider credentials can enable unauthorized account activity.

Mitigation: Do not place credentials in files, logs, headers, or prompts.

## Reference(s):

- [WhatsApp Business skill on ClawHub](https://clawhub.ai/byungkyu/skills/whatsapp-business)
- [Maton](https://maton.ai)
- [Maton documentation](https://docs.maton.ai)
- [WhatsApp Business API overview](https://developers.facebook.com/docs/whatsapp/cloud-api/overview)
- [WhatsApp send messages guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-messages)
- [WhatsApp message templates guide](https://developers.facebook.com/docs/whatsapp/cloud-api/guides/send-message-templates)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration instructions]

**Output Format:** [Markdown with command and API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Actions use the permissions of the connected account.]

## Skill Version(s):

1.2.9 (source: server-resolved ClawHub release)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
