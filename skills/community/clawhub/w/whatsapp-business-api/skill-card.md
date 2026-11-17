## Description:

Complete WhatsApp Business Cloud API for messages, templates, media, webhooks, flows, and business profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to guide WhatsApp Business Cloud API work, including message sending, template management, media handling, webhook processing, flows, and business profile administration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide actions against a real WhatsApp Business account, including sending messages and changing account settings.

Mitigation: Require explicit approval before sending messages, deleting templates or media, or changing two-step verification.

Risk: The skill handles customer phone numbers, message content, account context, and local memory that may contain sensitive business data.

Mitigation: Avoid storing customer or account details in plaintext memory unless the user intentionally opts in and controls file access.

Risk: Unverified webhook events can lead to fake event processing or misleading automation.

Mitigation: Verify webhook signatures with the app secret before processing events.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/ivangdavila/skills/whatsapp-business-api)
- [Skill homepage](https://clawic.com/skills/whatsapp-business-api)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance with JSON examples and curl command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WhatsApp Business Cloud API request examples and local setup guidance.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
