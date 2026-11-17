## Description:

Give an AI agent a real inbox and outbound email using Robotomail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[johnjoubert](https://clawhub.ai/user/johnjoubert)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to let an agent send, receive, read, reply to, and react to email through Robotomail mailboxes, webhooks, and SSE.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide an agent through actions that use a real mailbox, including sending mail, reading threads, creating listeners, and deleting resources.

Mitigation: Use a mailbox-scoped API key where possible and require explicit user confirmation before sending email, reading sensitive threads, creating webhooks or SSE listeners, or deleting resources.

Risk: Email contents, recipient lists, webhook secrets, and presigned attachment URLs may expose sensitive data.

Mitigation: Treat message bodies, recipient lists, webhook secrets, and attachment URLs as sensitive; avoid logging or sharing them unless the user explicitly requests it.

Risk: Webhook receivers can be abused if signatures are mishandled or replayed.

Mitigation: Verify Robotomail webhook signatures with timing-safe comparison, add replay protection, and handle malformed signatures robustly.

## Reference(s):

- [Robotomail API Reference](references/api-reference.md)
- [Webhook Signature Verification](references/webhook-verification.md)
- [Robotomail Website](https://robotomail.com)
- [Robotomail ClawHub Skill Page](https://clawhub.ai/johnjoubert/skills/robotomail)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with HTTP endpoints, JSON examples, curl-compatible commands, and webhook verification code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Robotomail API key in ROBOTOMAIL_API_KEY; may guide actions that affect real mailbox data and outbound email.]

## Skill Version(s):

1.0.6 (source: release evidence and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
