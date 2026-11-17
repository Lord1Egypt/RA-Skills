## Description:

Send Telegram notifications to team members by Telegram user ID.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agohpai](https://clawhub.ai/user/agohpai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to send Telegram alerts, reminders, and task updates to one or more team members by Telegram chat ID.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Messages and chat IDs are sent to Telegram through a locally configured bot credential.

Mitigation: Install only when the OpenClaw Telegram bot setup is trusted, avoid sensitive message content, and confirm recipients before sending.

Risk: The shell snippets interpolate message and recipient values, which can be unsafe if untrusted text is inserted.

Mitigation: Prefer a small Node sender that validates chat IDs, JSON-serializes message bodies, and avoids shell interpolation.

Risk: Bulk sending can notify unintended new or multiple recipients.

Mitigation: Ask for confirmation before sending to new chat IDs or multiple recipients.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/agohpai/skills/tg-notify)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with bash and JSON snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, node, Telegram chat IDs, and a local OpenClaw Telegram bot token configuration.]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
