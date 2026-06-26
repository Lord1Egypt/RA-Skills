## Description: <br>
Automatic interrupted-task resume workflow with queueing and recovery. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[RichardSun700](https://clawhub.ai/user/RichardSun700) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and OpenClaw agent operators use this skill to preserve interrupted task state, queue unfinished work, and resume older tasks after the current task completes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently stores cross-session task context, which may capture sensitive task details if users include secrets in titles, context, acceptance criteria, or recovered logs. <br>
Mitigation: Avoid storing secrets in task fields or recovered logs, and inspect or clear memory/task-resume-queue.json regularly. <br>
Risk: Automatic resume, watchdog, and cron-style continuation can continue work beyond the user’s intended scope if enabled without clear limits. <br>
Mitigation: Enable watchdog or cron behavior only with explicit scope, time limits, and a clear stop condition. <br>
Risk: Log-based recovery can import session-log content into the task queue. <br>
Mitigation: Restrict recovery to real OpenClaw session logs and review recovered context before resuming. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/RichardSun700/task-resume) <br>
- [Artifact README](README.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON command output from the helper script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The helper script writes and reads a workspace-global task queue at memory/task-resume-queue.json.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
