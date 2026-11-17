## Description:

Automate Slack messaging, channels, and search with Block Kit. Use when sending scheduled messages, syncing channels, monitoring chats, notifying teams.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xueyetianya](https://clawhub.ai/user/xueyetianya)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use Slack Automator to configure Slack Incoming Webhooks and send, format, schedule, template, and review team notifications from shell workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe input handling can make untrusted command arguments risky before the script is reviewed or fixed.

Mitigation: Review or fix the script before installation, and only pass trusted command arguments until the heredoc injection and template path traversal issues are fixed.

Risk: A Slack webhook URL grants posting access and is stored locally by the skill.

Mitigation: Treat the webhook URL as a password, restrict access to ~/.slack-automator, and rotate the webhook if it may have been exposed.

Risk: Local history, templates, schedules, and exports may contain sensitive Slack message content.

Mitigation: Avoid storing sensitive messages in history, templates, schedules, or exports, and review local file permissions before use.

## Reference(s):

- [Slack Automator on ClawHub](https://clawhub.ai/xueyetianya/skills/slack-automator)
- [xueyetianya publisher profile](https://clawhub.ai/user/xueyetianya)
- [BytesAgain homepage](https://bytesagain.com)
- [Slack Apps](https://api.slack.com/apps)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [When commands are run, the skill may create or update local Slack Automator configuration, templates, schedules, history, and exports under ~/.slack-automator.]

## Skill Version(s):

4.0.0 (source: server release evidence and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
