## Description:

Unified mailbox AI for both Outlook and Gmail. Checks unread emails, summarizes new mail with AI, detects meeting invitations, checks calendar conflicts on both Outlook and Google Calendar, and sends Telegram notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[l1tangdingzhen](https://clawhub.ai/user/l1tangdingzhen)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to monitor configured Outlook and Gmail mailboxes, summarize unread messages, identify meeting invitations, check Outlook or Google Calendar conflicts, and send Telegram notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can access mailbox and calendar data and forward AI-generated summaries to Telegram.

Mitigation: Use only on accounts where automated summarization and Telegram delivery are approved.

Risk: The requested Microsoft Graph permissions include write-capable mailbox and calendar scopes.

Mitigation: Reduce Microsoft Graph permissions to read-only access where possible before deployment.

Risk: The installer may write shell-profile settings and install a recurring cron job.

Mitigation: Inspect existing crontab and shell-profile changes before accepting installer prompts.

Risk: The Gmail setup may rely on an empty file-keyring password for non-interactive use.

Mitigation: Avoid the empty Gmail keyring password setup unless the host and account risk are acceptable.

## Reference(s):

- [Unified Mailbox AI on ClawHub](https://clawhub.ai/l1tangdingzhen/skills/unified-mailbox-ai)
- [OpenClaw](https://openclaw.ai)
- [outlook-graph ClawHub Skill](https://clawhub.ai/byungkyu/outlook-graph)
- [gog CLI](https://gogcli.sh)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON command output and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read mailbox and calendar data, invoke an OpenClaw agent for summarization, and send Telegram notifications when auto-notify is enabled.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
