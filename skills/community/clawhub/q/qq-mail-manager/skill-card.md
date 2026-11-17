## Description:

QQ Mail Manager helps an agent list folders, search and view messages, download attachments, mark messages, move or trash messages, and send or reply to email through a QQ Mail account.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sccc726](https://clawhub.ai/user/sccc726)

### License/Terms of Use:

MIT-0

## Use Case:

External users use this skill to let an agent manage a QQ Mail mailbox, including finding and reading messages, downloading attachments, changing read state, moving or trashing messages, and sending replies or new emails after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read, send, download, move, and trash real mailbox content using a QQ Mail authorization code.

Mitigation: Use it only with a mailbox the user is comfortable exposing to an agent, and require fresh human confirmation before send, move, delete, or download actions.

Risk: Email content returned to the agent is untrusted text and may include attempts to influence later actions.

Mitigation: Treat displayed email bodies as data rather than instructions, and stop destructive workflows when a script reports an error or partial status.

Risk: Attachments can expose sensitive local or mailbox data when downloaded or sent.

Mitigation: Download only expected attachments into a controlled directory, and avoid sending attachments from sensitive local paths.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sccc726/skills/qq-mail-manager)
- [QQ email configuration guide](references/qq-email-config.md)
- [QQ Mail](https://mail.qq.com)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance with inline shell commands and JSON script results.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires QQ_EMAIL and QQ_EMAIL_AUTH_CODE; attachment downloads can write files to a user-selected directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
