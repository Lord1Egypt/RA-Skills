## Description:

Monitor and manage Gmail accounts for inbox checks, email triage, urgent-message scanning, and user-approved sending over IMAP/SMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[boris148](https://clawhub.ai/user/boris148)

### License/Terms of Use:

MIT-0

## Use Case:

Employees or agents use this skill to check configured Gmail inboxes, triage recent messages, flag urgent or security-related email, and prepare or send approved operational messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has high-impact mailbox access and can send email from configured accounts.

Mitigation: Require explicit user approval for every outbound email unless a narrow internal allowlist is implemented and enforced in code.

Risk: Account selection and send behavior require review before use.

Mitigation: Verify intended account names, lock configuration to Gmail IMAP/SMTP endpoints, and test account routing before operational use.

Risk: The skill depends on a local Gmail credential configuration file.

Mitigation: Protect the credential file with appropriate filesystem permissions and limit app-password access to the intended mailboxes.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, shell commands, configuration guidance]

**Output Format:** [Markdown with inline shell commands and concise operational guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include mailbox summaries, message metadata, search guidance, and user-approval reminders for outbound email.]

## Skill Version(s):

1.0.0 (source: frontmatter and release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
