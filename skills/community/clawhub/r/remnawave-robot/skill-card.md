## Description:

Automates the Remnawave account lifecycle, including configuration, account creation, group synchronization, account lookup, deletion, and email notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[uepuer](https://clawhub.ai/user/uepuer)

### License/Terms of Use:

MIT-0

## Use Case:

Operators and developers use this skill to manage Remnawave user accounts and internal groups from shell commands, then send account-opening or follow-up email notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Remnawave credentials, SMTP credentials, and subscription links unsafely.

Mitigation: Review the configuration before installation, store secrets outside committed files, rotate exposed credentials or subscription URLs, and restrict access to generated configuration and logs.

Risk: Test and email scripts can send access information to fixed or prefilled recipients.

Mitigation: Remove hard-coded recipients and subscription URLs, require explicit recipient input, and disable test email sending before use with real accounts.

Risk: The artifact includes behavior that can disable TLS certificate validation.

Mitigation: Use valid TLS certificates for Remnawave and SMTP endpoints and require certificate validation in production.

Risk: Console output and logs can expose account details and subscription URLs.

Mitigation: Redact sensitive values from logs, limit log retention, and restrict log file permissions to responsible administrators.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/uepuer/skills/remnawave-robot)
- [Artifact README](artifact/README.md)
- [Artifact Skill Documentation](artifact/SKILL.md)
- [Artifact Publish Summary](artifact/PUBLISH-SUMMARY.md)
- [Package Manifest](artifact/package.json)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples and generated local configuration or log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Scripts may also perform Remnawave API calls and send SMTP email when executed by the user.]

## Skill Version(s):

1.0.6 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
