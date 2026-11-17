## Description:

Monitors configured Xiaohongshu bloggers for new posts and sends Feishu notifications while maintaining local snapshots to avoid duplicate alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kmknkk](https://clawhub.ai/user/kmknkk)

### License/Terms of Use:

MIT-0

## Use Case:

Users who monitor Xiaohongshu accounts use this skill to run recurring checks for new posts, compare snapshots, and receive Feishu notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that notifications are sent to a hard-coded Feishu recipient.

Mitigation: Review, replace, or remove the configured Feishu recipient before installing or running the monitor.

Risk: The security guidance flags an overbroad cron removal command.

Mitigation: Avoid using crontab -r unless all cron jobs for the current user should be deleted; prefer editing only the monitor's scheduled entries.

Risk: The security guidance notes that the script uses the OpenClaw browser profile and saved Xiaohongshu login state.

Mitigation: Run it only with an intended browser profile and account session, and review access implications before repeated monitoring.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/kmknkk/skills/xiaohongshu-monitor)
- [Configured Xiaohongshu profile](https://www.xiaohongshu.com/user/profile/5b6150c56b58b741e26b8c7f)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and configuration notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces monitoring guidance and uses local snapshots, logs, and Feishu notifications when the script is run.]

## Skill Version(s):

1.0.2 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
