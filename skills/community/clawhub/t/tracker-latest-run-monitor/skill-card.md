## Description:

Monitor the most recent run result of a configured OpenClaw cron job and send a compact Feishu private message with the latest execution time, status, and detail.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaronstuart](https://clawhub.ai/user/aaronstuart)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor the latest finished OpenClaw cron run and send a compact Feishu private message with the run time, status, and detail.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill is configured for a specific OpenClaw cron job, run-log path, config path, recipient, and message labels.

Mitigation: Review and update the hard-coded job ID, run-log path, config path, recipient, and labels before running it in another environment.

Risk: Feishu app credentials and run error or summary details may be sensitive.

Mitigation: Protect the Feishu app secret, limit access to the configuration file, and review message content before sending run details externally.

Risk: Notifications can be sent to the wrong Feishu user if the configured recipient is stale or incorrect.

Mitigation: Verify feishu.notifyUserOpenId and send a controlled test notification before enabling routine monitoring.

## Reference(s):

- [Configuration](references/configuration.md)
- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell command and Feishu text notification behavior]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Sends one Feishu private message for the latest finished run and emits JSON status to stdout; exits quietly when no finished run exists.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
