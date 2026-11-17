## Description:

Agent-facing QQ Mail inbox management over IMAP/SMTP for OpenClaw, Hermes, and other autonomous agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[echovic](https://clawhub.ai/user/echovic)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent inspect, triage, organize, archive, mark, reply to, or clean up a QQ Mail inbox while preserving dry-run and explicit approval boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires access to a QQ Mail authorization code and mailbox contents.

Mitigation: Install only when mailbox access is acceptable, provide credentials through environment variables, and avoid printing, persisting, or committing the authorization code.

Risk: Mailbox mutations such as archive, mark read or unread, send, reply, and delete can change mailbox state or send externally visible messages.

Mitigation: Start with read-only JSON plans and dry-runs, review exact proposed actions, and require explicit approval before using --apply or non-dry-run send and reply commands.

Risk: Permanent deletion can remove email irreversibly.

Mitigation: Reserve deletion for explicit narrow requests, run a dry-run first, and require the --confirm-delete DELETE guard before deleting.

## Reference(s):

- [QQMail Organizer ClawHub skill page](https://clawhub.ai/echovic/skills/qqmail-organizer)
- [Publisher profile](https://clawhub.ai/user/echovic)
- [QQMail Organizer Rules schema](https://github.com/echoVic/qqmail-organizer/rules.schema.json)
- [JSON Schema Draft 2020-12](https://json-schema.org/draft/2020-12/schema)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands and optional JSON command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports should summarize read-only, dry-run, or applied status and avoid exposing credentials or unnecessary private email content.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
