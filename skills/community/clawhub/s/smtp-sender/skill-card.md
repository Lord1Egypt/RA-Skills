## Description:

A skill to send emails with support for markdown, HTML text, and attachments, leveraging existing SMTP configuration in `{skill~}/smtp-config.json`.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xlbbb-cn](https://clawhub.ai/user/xlbbb-cn)

### License/Terms of Use:


## Use Case:

Developers and external users can use this skill to prepare or run SMTP email-sending workflows from an agent environment, including plain text or HTML message bodies and optional file attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release security summary says the skill ships unsafe SMTP configuration defaults.

Mitigation: Replace example values before use, use a dedicated least-privileged SMTP account, require TLS, and secure the SMTP configuration file.

Risk: The release security summary says the skill can send arbitrary local files as attachments without strong guardrails.

Mitigation: Approve each recipient and attachment path before execution, and run the skill where only intended files are accessible.

Risk: The security guidance warns not to rely on documented markdown conversion, retries, or audit logs unless they are implemented later.

Mitigation: Validate generated email content and operational safeguards in the installed artifact before using those features in production workflows.

## Reference(s):


## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can send SMTP email with optional HTML body and file attachments when executed with a valid SMTP configuration.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
