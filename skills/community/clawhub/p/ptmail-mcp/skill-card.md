## Description:

Helps agents manage multiple PTMail mailboxes through a logged-in Windows client, including reading and syncing mail, exporting attachments, and sending mail with user approval.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qique](https://clawhub.ai/user/qique)

### License/Terms of Use:

MIT-0

## Use Case:

People using an AI assistant with a logged-in PTMail Windows client can inspect mailboxes, read and sync messages, export attachments, and send approved messages. The skill also guides developers through connecting the separately installed local MCP runtime.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Email metadata, bodies, and exported attachments may contain sensitive information.

Mitigation: Limit access and exports to the requested mailboxes and files; do not share their contents with other services without explicit permission.

Risk: Sending mail or changing connections and local mailbox data can have unintended consequences.

Mitigation: Show the sender, recipients, subject, and body before each send; confirm the target and impact before disconnecting or clearing local data.

Risk: Entering an email app password through an AI conversation exposes it to that session.

Mitigation: Prefer entering app passwords in the PTMail client; never log, echo, or save a password supplied through the assistant.

Risk: The separately installed runtime may be substituted or outdated.

Mitigation: Obtain the official package and verify its published hash when possible before connecting it.

## Reference(s):

- [PTMail skill release](https://clawhub.ai/qique/skills/ptmail-mcp)
- [PTMail product website](https://ptmail.qique.cn/)
- [PTMail connection guide](references/setup.md)
- [PTMail MCP tools](references/tools.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration guidance]

**Output Format:** [Markdown responses and MCP tool results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Mail actions depend on the connected client and the user's authorization.]

## Skill Version(s):

0.2.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
