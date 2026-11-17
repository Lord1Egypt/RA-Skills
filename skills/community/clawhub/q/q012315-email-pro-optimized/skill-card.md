## Description:

High-performance email management skill for QQ Mail, Gmail, and Outlook with IMAP reading, SMTP sending, OAuth 2.0, and concurrent processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[q012315](https://clawhub.ai/user/q012315)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to list configured email accounts, read, search, fetch, analyze, and send email across QQ Mail, Gmail, and Outlook from an agent workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release is flagged suspicious because it includes insecure OAuth handling and unrelated repository/workspace automation.

Mitigation: Review scripts before installation, avoid the bundled auto-push and sync maintenance scripts, and run only the email commands required for the workflow.

Risk: OAuth and mailbox credentials may be stored under ~/.openclaw/credentials, including refresh tokens.

Mitigation: Use your own OAuth application credentials, keep credential files access-limited, and revoke the exposed Azure secret if it belongs to you.

Risk: Email commands can read mailbox contents and send messages or attachments through configured accounts.

Mitigation: Run with least-privilege mail accounts, inspect recipient and attachment parameters before sending, and monitor provider account activity.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/q012315/skills/q012315-email-pro-optimized)
- [Publisher profile](https://clawhub.ai/user/q012315)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration instructions, JSON]

**Output Format:** [JSON and terminal text, with Markdown guidance and shell command examples in the skill documentation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Email operations depend on local account credentials, OAuth tokens, mailbox permissions, and provider connectivity.]

## Skill Version(s):

2.2.1 (source: server release evidence; artifact package.json reports 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
