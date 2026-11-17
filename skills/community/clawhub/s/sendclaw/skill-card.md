## Description:

Get a FREE email address "you@sendclaw.com" - Email for AI agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jononovo](https://clawhub.ai/user/jononovo)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to give an agent a SendClaw mailbox, send and receive task-oriented email, check unread messages, reply in threads, and notify a human about account state or low quota.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent broad authority to send external email from a SendClaw mailbox.

Mitigation: Require human approval before the agent replies to inbound mail, contacts new recipients, or sends sensitive information.

Risk: Leaking SENDCLAW_API_KEY would let another party send email as the agent.

Mitigation: Store SENDCLAW_API_KEY only in a protected secret manager, do not paste it into chat, and use it only for requests to sendclaw.com.

Risk: Inbound email can contain misleading requests, unsafe links, or attempts to redirect the agent's behavior.

Mitigation: Review inbound messages before acting on requests, opening links, or sharing information with external recipients.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/jononovo/skills/sendclaw)
- [SendClaw Homepage](https://sendclaw.com)
- [SendClaw Skill and API Reference](https://sendclaw.com/SKILL.md)
- [SendClaw Heartbeat Routine](https://sendclaw.com/HEARTBEAT.md)
- [SendClaw Skill Metadata](https://sendclaw.com/skill.json)

## Skill Output:

**Output Type(s):** [Guidance, Text, API Calls, Shell commands, Configuration]

**Output Format:** [Markdown with HTTP and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses SENDCLAW_API_KEY for SendClaw API access; supports outbound email, inbound message checks, threaded replies, pagination, quotas, and optional webhook configuration.]

## Skill Version(s):

1.7.6 (source: server release metadata; artifact frontmatter and skill.json report 1.7.7)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
