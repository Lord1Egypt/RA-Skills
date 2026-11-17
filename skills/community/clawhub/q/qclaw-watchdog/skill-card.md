## Description:

QClaw Watchdog monitors QClaw health, restarts QClaw when issues are detected, and uses Feishu for status alerts and remote commands.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kf-liu](https://clawhub.ai/user/kf-liu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and QClaw users use this skill to install and operate a local watchdog that checks QClaw Gateway health, sends Feishu notifications, and starts or restarts QClaw when configured checks fail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes real-looking Feishu credentials in config.json.

Mitigation: Replace and rotate the bundled Feishu credentials before use, and remove config.json from redistributed copies.

Risk: Remote Feishu messages can trigger local QClaw start, restart, and quit actions without an in-code sender check.

Mitigation: Restrict accepted senders or groups, limit bot permissions, and require confirmation for restart and quit commands.

Risk: Process control uses broad QClaw process matching during restart.

Mitigation: Review and narrow the process matching before deployment so unrelated processes are not stopped.

Risk: The watchdog can run persistently and send routine status reports.

Mitigation: Decide explicitly whether persistent startup and scheduled reporting fit the deployment environment.

## Reference(s):

- [QClaw Watchdog on ClawHub](https://clawhub.ai/kf-liu/skills/qclaw-watchdog)
- [Feishu Developer Console](https://open.feishu.cn/)
- [Feishu Message API Explorer](https://open.feishu.cn/api-explorer/cli_a9333bca0c78dceb?apiName=create&project=im&resource=message&version=v1)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces setup, operation, and troubleshooting guidance for a local Node.js watchdog.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/version.txt)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
