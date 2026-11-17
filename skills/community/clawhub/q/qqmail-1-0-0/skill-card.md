## Description:

Manage QQ Mail (QQ邮箱) via IMAP/SMTP for reading inbox messages, sending emails with attachments, searching by subject, sender, or date, and listing folders.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunyue1977](https://clawhub.ai/user/sunyue1977)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent operate a QQ Mail account through IMAP and SMTP after the user configures QQ Mail credentials and an authorization code.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read mailbox contents when QQMAIL_USER and QQMAIL_AUTH_CODE are configured.

Mitigation: Use it only with an intended QQ Mail account and avoid exposing the authorization code outside the local environment.

Risk: The skill can send email messages and attachments through QQ Mail.

Mitigation: Review recipients, subject, body, and attachment paths before allowing send commands to run.

## Reference(s):

- [Qqmail 1.0.0 ClawHub release](https://clawhub.ai/sunyue1977/skills/qqmail-1-0-0)
- [sunyue1977 ClawHub publisher profile](https://clawhub.ai/user/sunyue1977)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and text output from the QQ Mail script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3 and the QQMAIL_USER and QQMAIL_AUTH_CODE environment variables.]

## Skill Version(s):

1.0.0 (source: release evidence and artifact metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
