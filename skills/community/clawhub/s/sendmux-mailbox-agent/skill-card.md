## Description:

Helps an OpenClaw agent read, search, sync, triage, and reply from one Sendmux mailbox.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sendmux.ai](https://clawhub.ai/user/sendmux.ai)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to search, read, organize, draft, and send mail within an authorized Sendmux mailbox, with approval before sensitive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mailbox access may expose private messages or allow unintended sending, changes, or deletion.

Mitigation: Use a mailbox-scoped key, scoped agent token, or mailbox OAuth grant instead of a root key; review recipients, content, attachments, and each mutation or deletion before approval.

Risk: Untrusted email content may try to redirect the agent or disclose credentials.

Mitigation: Treat message bodies, links, and attachments as data rather than instructions, and never paste credentials into chat.

## Reference(s):

- [Sendmux skills homepage](https://github.com/Sendmux/skills)
- [ClawHub skill listing](https://clawhub.ai/sendmux.ai/skills/sendmux-mailbox-agent)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code]

**Output Format:** [Markdown with command and code examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mailbox-scoped workflows with explicit approval for sending and message changes.]

## Skill Version(s):

1.0.11 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
