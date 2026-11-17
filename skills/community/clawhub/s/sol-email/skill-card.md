## Description:

Read and send emails using the SolEmail automation system.

This skill is ready for commercial/non-commercial use.

## Publisher:

[amrree](https://clawhub.ai/user/amrree)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use SolEmail to let an agent check local Maildir email, read selected messages, send SMTP email, and package matching local files as email attachments.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent recurring access to private email.

Mitigation: Use a dedicated low-privilege email account or revocable app password, keep credential files locked down, and review the skill carefully before installation.

Risk: The skill can send outbound email and attachments.

Mitigation: Require explicit confirmation before sending any email or attachment, especially in automated or scheduled workflows.

Risk: File search and attachment workflows can include local files selected by glob patterns.

Mitigation: Restrict file searches to explicit safe directories and review the selected files before sending.

## Reference(s):

- [SolEmail ClawHub release](https://clawhub.ai/amrree/skills/sol-email)
- [SolEmail automation guide](https://thesolai.github.io/guides/email-automation/)
- [himalaya email client](https://github.com/soywod/himalaya)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, TOML configuration, Python scripts, and optional JSON email summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email-reading commands may expose private message content; sending and attachment workflows depend on local SMTP credentials, himalaya configuration, and filesystem paths.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
