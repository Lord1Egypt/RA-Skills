## Description:

Send emails via SMTP with support for HTML formatting, file attachments, and email templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangyendt](https://clawhub.ai/user/wangyendt)

### License/Terms of Use:


## Use Case:

Developers, employees, and external users can use this skill to prepare and send SMTP email messages with plain text or HTML bodies, Markdown conversion, templates, and file attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles SMTP credentials and email account secrets.

Mitigation: Use a narrowly scoped app password or SMTP token through a secure secret mechanism, and avoid sharing primary account passwords.

Risk: The skill can send emails and attachments to external recipients.

Mitigation: Review recipients, subject, body content, and attachments before confirming any send.

Risk: The skill includes a built-in default sender account behavior.

Mitigation: Prefer a user-owned sender account and avoid the built-in default sender unless its use is explicitly intended.

Risk: Disabling TLS can expose sensitive email traffic and credentials.

Mitigation: Use TLS or SSL for SMTP connections and do not use unencrypted sending options.

## Reference(s):

- [SMTP Server Configurations](references/smtp-servers.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command-line invocations and SMTP configuration details]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May generate HTML email content from Markdown and attach user-specified files.]

## Skill Version(s):

0.1.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
