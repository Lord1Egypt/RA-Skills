## Description:

Send emails via SMTP using the msmtp command-line tool configured in ~/.msmtp/config for authentication and server settings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hitygx](https://clawhub.ai/user/hitygx)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to configure msmtp and send plain-text or HTML emails through an SMTP account from agent-guided shell commands.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell interpolation can expose email subject, body, sender, or recipient fields to command injection or malformed message behavior.

Mitigation: Review generated commands before execution, avoid pasting untrusted email fields into a shell command string, and pass dynamic values through safer quoting or a wrapper that separates data from shell syntax.

Risk: SMTP credentials are stored persistently in ~/.msmtp/config and may be plaintext.

Mitigation: Use an app-specific SMTP password, set the config file to mode 600, and keep the file private and out of repositories, shared backups, and logs.

Risk: Agent-generated email can be sent to unintended recipients or with unintended content.

Mitigation: Confirm exact recipients, sender header, subject, and message body before sending.

## Reference(s):

- [Simple SMTP Mailer on ClawHub](https://clawhub.ai/hitygx/skills/simple-smtp-mail)
- [hitygx publisher profile](https://clawhub.ai/user/hitygx)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires msmtp and an existing ~/.msmtp/config SMTP account configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
