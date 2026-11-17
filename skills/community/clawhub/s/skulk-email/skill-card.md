## Description:

Skulk Email lets agents read inboxes, send email, and search messages through DreamHost Roundcube over HTTPS, with optional shared Gmail inbox access through IMAP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[adainthelab](https://clawhub.ai/user/adainthelab)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to configure mailbox credentials, read DreamHost or optional Gmail inboxes, search messages, and send email from environments where SMTP may be blocked.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill gives an agent mailbox read access and outbound sending authority.

Mitigation: Use a dedicated mailbox or app-specific password, restrict the credential file to the intended user, and require review for recipients, subject lines, and message bodies before sending.

Risk: Reusable mailbox credentials can create account-compromise risk if the host is shared or compromised.

Mitigation: Keep credentials in a local file with 700 directory and 600 file permissions, avoid shared hosts, rotate credentials if exposure is suspected, and limit mailbox privileges where possible.

Risk: Credential handling and temporary webmail cookies may expose secrets locally.

Mitigation: Harden the script before sensitive deployments so secrets are not passed in process arguments and webmail cookies are created with mktemp-style restricted temporary files.

## Reference(s):

- [Skulk Email on ClawHub](https://clawhub.ai/adainthelab/skills/skulk-email)
- [The Human Pattern Lab](https://thehumanpatternlab.com)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and command-line text output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local DreamHost mailbox credentials and host dependencies python3, curl, and jq.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
