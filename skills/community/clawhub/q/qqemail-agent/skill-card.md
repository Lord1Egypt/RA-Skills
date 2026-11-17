## Description:

QQemail-agent helps agents read recent QQ Mail messages through IMAP and send QQ Mail messages through SMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cynic-joe](https://clawhub.ai/user/cynic-joe)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to configure QQ Mail access, fetch recent mailbox messages for agent-assisted review, and send outbound messages from a QQ Mail account.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Reusable QQ Mail authorization codes may be stored in plaintext configuration.

Mitigation: Store credentials outside the project or with strict permissions, ensure .env is ignored by version control, and rotate or revoke the authorization code after testing or suspected exposure.

Risk: The fetch script can read recent mailbox content broadly from the configured account.

Mitigation: Use a dedicated mailbox or folder when possible and only install the skill when recent QQ Mail read access is acceptable.

Risk: The send script can send outbound email from the configured QQ Mail account.

Mitigation: Use a dedicated account for testing and review recipient, subject, and body values before running send commands.

## Reference(s):

- [QQ Mail](https://mail.qq.com)
- [ClawHub skill page](https://clawhub.ai/cynic-joe/skills/qqemail-agent)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a local .env file and run Python scripts that read or send email.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter and changelog mention 1.1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
