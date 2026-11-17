## Description:

Manage temporary email addresses and messages using the chat-tempmail.com API. Use when the user wants to create disposable emails, check inbox messages, or manage webhooks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[selenium39](https://clawhub.ai/user/selenium39)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to create disposable email addresses, inspect temporary inbox messages, and manage message notification webhooks through the chat-tempmail.com API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends an API key and temporary mailbox contents to chat-tempmail.com.

Mitigation: Install only when the user trusts chat-tempmail.com with the API key and mailbox contents, and keep TEMP_EMAIL_API_KEY scoped to trusted environments.

Risk: Configured webhooks may forward future message contents to the supplied URL.

Mitigation: Treat webhook URLs as sensitive, confirm the destination before enabling a webhook, and disable webhooks when message forwarding is no longer needed.

Risk: Deletion operations and user-supplied URL path values can affect emails or messages if IDs are wrong or unsafe.

Mitigation: Require confirmation of exact email and message IDs before deletion, and safely encode or validate user-provided values before building curl requests.

## Reference(s):

- [chat-tempmail.com API Reference](artifact/reference.md)
- [Temporary Email on ClawHub](https://clawhub.ai/selenium39/skills/temp-email)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline curl commands and readable summaries of JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TEMP_EMAIL_API_KEY for authenticated chat-tempmail.com API calls.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
