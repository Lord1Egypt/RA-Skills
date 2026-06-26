## Description: <br>
Safe OpenClaw gateway restart workflow with doctor precheck, checkpoint, restart-health-resume chain, task continuation, reconcile, and user-visible notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[who-ohw](https://clawhub.ai/user/who-ohw) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators responsible for OpenClaw gateway availability use this skill to plan, validate, execute, and recover restart workflows with prechecks, checkpoints, resume actions, notifications, reconciliation, and diagnostics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run plan-supplied shell commands and scripts during restart recovery. <br>
Mitigation: Install only for trusted agents and operators, review queued actions before running, keep ACTION_ALLOWLIST_FILE narrow, and avoid command or script actions from untrusted plans. <br>
Risk: Detached restart or acceptance runs can continue outside the calling session. <br>
Mitigation: Monitor ./state/restart logs and reports after detached runs, and use report or diagnose commands to confirm completion before treating a restart as done. <br>
Risk: Gateway restarts can interrupt service if prerequisites or recovery actions fail. <br>
Mitigation: Use the built-in doctor precheck, checkpoint, health check, resume status, notification gates, and reconcile workflow before closing the task. <br>


## Reference(s): <br>
- [OpenClaw restart-safe SOP](references/restart-safe-sop.md) <br>
- [ClawHub skill page](https://clawhub.ai/who-ohw/restart-safe-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, JSON status reports, notifications] <br>
**Output Format:** [Markdown guidance with bash commands and JSON state or report outputs] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses task IDs, optional notification settings, action allowlists, retry/backoff environment variables, and state files under ./state/restart.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
