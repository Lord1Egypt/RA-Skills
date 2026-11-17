## Description:

Read and send email via IMAP/SMTP. Check for new/unread messages, fetch content, search mailboxes, mark as read/unread, and send emails with attachments. Works with any IMAP/SMTP server including Gmail, Outlook, 163.com, and other standard email providers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cjboy007](https://clawhub.ai/user/cjboy007)

### License/Terms of Use:

MIT-0

## Use Case:

Sales teams and agents use this skill to monitor sales mailboxes, search and fetch messages, prepare personalized replies, and send complete customer emails with attachments through configured IMAP/SMTP providers. Optional workflows can sync customer context to OKKI CRM and route generated drafts to Discord for review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell command execution can create command injection risk when mailbox or customer data reaches shell commands.

Mitigation: Replace execSync-style shell construction with argument-safe APIs before using the skill on production mailboxes.

Risk: Live workflows can process real email and send data to CRM, Discord, and external AI services.

Mitigation: Require explicit opt-in for each external integration and make dry-run behavior the default for tests and review workflows.

Risk: Local archives, drafts, and logs may contain sensitive customer communications or credentials.

Mitigation: Store generated files with restrictive permissions, define retention limits, and rotate mail, Discord, OpenRouter, and CRM credentials after suspected exposure.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cjboy007/skills/sales-email-automation)
- [Publisher profile](https://clawhub.ai/user/cjboy007)
- [Skill instructions](artifact/SKILL.md)
- [Integration guide](artifact/INTEGRATION.md)
- [Workflow checklist](artifact/WORKFLOW_CHECKLIST.md)
- [Workflow test report](artifact/WORKFLOW_TEST_REPORT.md)
- [Google App Passwords](https://myaccount.google.com/apppasswords)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON or configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce local mail archives, downloaded attachments, reply drafts, and review records when connected to configured services.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
