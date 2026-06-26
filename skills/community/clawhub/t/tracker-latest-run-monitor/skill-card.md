## Description: <br>
Monitor the most recent run result of a configured OpenClaw cron job and send a compact Feishu private message with the latest execution time, status, and detail. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aaronstuart](https://clawhub.ai/user/aaronstuart) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to check the latest finished OpenClaw cron run and send a concise Feishu status notification for routine monitoring or alerting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Hardcoded cron-run and Feishu config paths may target the wrong local files if reused without changes. <br>
Mitigation: Confirm or update TARGET_JOB_ID, TARGET_JOB_NAME, RUNS_PATH, and CONFIG_PATH before running the script. <br>
Risk: The script uses a Feishu app secret and recipient open_id to send private messages. <br>
Mitigation: Use a Feishu app secret scoped only to the required message-sending permission and verify the intended recipient before deployment. <br>


## Reference(s): <br>
- [Configuration](references/configuration.md) <br>
- [Feishu Open Platform](https://open.feishu.cn) <br>
- [ClawHub release page](https://clawhub.ai/aaronstuart/tracker-latest-run-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Feishu text notification and JSON status log] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Notification text includes latest execution time, status, and details; the script exits quietly when no finished run exists.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
