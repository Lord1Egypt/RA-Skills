## Description: <br>
Send short status descriptions in chat for long-running tasks, including manual updates, periodic monitoring, completion notices, and failure notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Mightyprime1](https://clawhub.ai/user/Mightyprime1) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to send concise progress, success, warning, or error updates during long-running tasks. It can be used manually from shell commands or through a monitor that emits periodic status messages. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Status text may be sent to Telegram through local Clawdbot credentials, including a default recipient if TELEGRAM_TARGET is not set. <br>
Mitigation: Set TELEGRAM_TARGET explicitly, verify the recipient before running the scripts, and confirm the gateway token is scoped appropriately. <br>
Risk: Status messages and logging behavior can expose secrets, sensitive filenames, or task details. <br>
Mitigation: Keep secrets and sensitive paths out of status messages, and remove generated logs and state files after the task completes. <br>
Risk: Periodic monitors or scheduled jobs can continue sending updates after the original task is finished. <br>
Mitigation: Stop or cancel monitors when work completes, and clean up any related cron jobs or monitor state. <br>


## Reference(s): <br>
- [Task Status Usage Guide](references/usage.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Mightyprime1/task-status) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, code, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell and Python examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Status messages are intended to be short and may be sent through Telegram via local Clawdbot credentials.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
