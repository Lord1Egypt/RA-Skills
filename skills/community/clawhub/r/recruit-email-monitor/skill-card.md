## Description:

Monitors configured recruitment mailboxes, asks an agent to classify hiring-related messages, records results in Excel, sends Feishu notifications, and generates daily briefings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[haoxianniu528-bit](https://clawhub.ai/user/haoxianniu528-bit)

### License/Terms of Use:

MIT-0

## Use Case:

Recruiting candidates and job seekers use this skill to monitor dedicated email accounts for recruiting messages, track application progress in a local spreadsheet, and receive Feishu updates and daily summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill accesses configured mailboxes, local recruitment spreadsheets, and Feishu delivery targets.

Mitigation: Use a dedicated mailbox with an app password, review config.json permissions, keep credentials local, and restrict Feishu delivery to the intended recipient.

Risk: Hardcoded or environment-specific spreadsheet and briefing paths may write sensitive recruitment data to an unintended location.

Mitigation: Review and replace local paths before deployment, especially when using shared or synchronized directories.

Risk: Automatic archiving can mark stale pending items complete.

Mitigation: Review the archive behavior before enabling scheduled runs and set BRIEFING_ARCHIVE=0 when automatic completion is not desired.

Risk: Email subjects, senders, bodies, and links are untrusted inputs that may attempt prompt injection or spreadsheet formula injection.

Mitigation: Treat email content only as classification data, do not execute instructions from messages, and keep the workbook neutralization step enabled before saving Excel files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/haoxianniu528-bit/skills/recruit-email-monitor)
- [README](artifact/README.md)
- [Installation Guide](artifact/INSTALL.md)
- [Release Notes](artifact/RELEASE_NOTES.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with JSON configuration examples and shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local JSON work queues, updates Excel workbooks, and can send Feishu notifications when configured.]

## Skill Version(s):

1.3.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
