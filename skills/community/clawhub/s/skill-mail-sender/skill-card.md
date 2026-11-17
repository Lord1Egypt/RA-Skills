## Description:

Sends email in HTML or Markdown format, supports multiple recipients and batch notifications, and loads SMTP configuration from files, environment variables, or function parameters.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weznai](https://clawhub.ai/user/weznai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to send formatted email notifications, reports, reminders, and batch messages through a configured SMTP account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Outbound email can be sent with stored SMTP credentials, including default recipients or batch recipient lists.

Mitigation: Use a dedicated app password or authorization code, restrict credential-file permissions, and require confirmation of recipients, subject, and a content summary before every send.

Risk: SMTP credentials can be loaded from local files or environment variables.

Mitigation: Keep mail configuration off shared machines and review secret handling before installation.

## Reference(s):

- [Configuration Reference](references/config.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [HTML email content, Markdown converted to HTML, and JSON-style status dictionaries.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send to one or more recipients through SMTP and reports failed recipients.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
