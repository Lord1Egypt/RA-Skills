## Description:

Smart Email is an AI-powered email assistant that collects messages from QQ, 126, 163, and Outlook via IMAP, archives them locally, detects urgent mail, and sends urgent alerts or digests to user-selected channels.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bu-bu-xxx](https://clawhub.ai/user/bu-bu-xxx)

### License/Terms of Use:

MIT-0

## Use Case:

External users and OpenClaw agents use Smart Email to monitor personal or work mailboxes, summarize incoming mail, identify urgent messages, and push alerts or digests to Telegram, DingTalk, WeCom, or Feishu.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Install provenance is unavailable and the evidence flags a bu-bu-xxx versus openclaw repository mismatch.

Mitigation: Review the repository source before installing, use a pinned trusted commit or release, and resolve the publisher/repository mismatch.

Risk: Mailbox authorization codes and AI provider API keys are high-value secrets.

Mitigation: Enter secrets only in local configuration, keep the environment file private, and rotate credentials if they are exposed.

Risk: Subagent-based email analysis is called out for review before use.

Mitigation: Consider avoiding the subagent provider until it is sandboxed and uses private temporary files.

Risk: Scheduled OpenClaw cron jobs can continue reading mail and dispatching messages after setup.

Mitigation: Review the installed cron jobs after setup and remove or adjust schedules that are not intended.

## Reference(s):

- [Smart Email User Guide](references/USER_GUIDE.md)
- [Smart Email Install Guide](references/INSTALL.md)
- [ClawHub Skill Page](https://clawhub.ai/bu-bu-xxx/skills/smart-email-assistant)
- [OpenClaw Platform](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files]

**Output Format:** [Markdown guidance with inline shell commands and environment variable examples; runtime notifications and digests are Markdown or text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create local mail archives, SQLite tracking data, outbox JSON messages, logs, and scheduled cron jobs when installed.]

## Skill Version(s):

2.5.2 (source: evidence.release.version and pyproject.toml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
