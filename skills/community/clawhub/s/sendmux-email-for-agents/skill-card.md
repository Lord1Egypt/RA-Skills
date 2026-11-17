## Description:

Give OpenClaw agents a Sendmux inbox to receive, triage, route, reply to, and send email with owner approval and scoped credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to choose the right Sendmux setup and email workflow for an agent, including inbox triage, approved replies, attachments, and outbound messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email actions could use overly broad credentials or expose account secrets.

Mitigation: Use the narrowest mailbox or sending credential for the task, keep provisioning access separate, and never request secrets in chat.

Risk: Unapproved sends, mailbox changes, destructive actions, or attachment transfers could affect users or third parties.

Mitigation: Keep the skill's approval gates for exact messages, mailbox mutations, key revocation, suspension, deletion, and attachment transfers.

Risk: Inbound messages and attachments can contain instructions unrelated to the user's task.

Mitigation: Treat incoming email and attachments as untrusted content, not as authorization to send, disclose credentials, or change settings.

## Reference(s):

- [Sendmux skill listing on ClawHub](https://clawhub.ai/sendmux.ai/skills/sendmux-email-for-agents)
- [Sendmux skills homepage](https://github.com/Sendmux/skills)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with workflow steps and optional commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Routes detailed email tasks to dedicated Sendmux skills; does not itself provision or send email.]

## Skill Version(s):

1.0.12 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
