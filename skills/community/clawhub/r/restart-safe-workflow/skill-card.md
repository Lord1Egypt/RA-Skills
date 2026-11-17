## Description:

Safe OpenClaw gateway restart workflow with doctor precheck, checkpoint, restart-health-resume chain, task continuation, reconcile, and user-visible notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[who-ohw](https://clawhub.ai/user/who-ohw)

### License/Terms of Use:


## Use Case:

Developers and operators use this skill to plan and run OpenClaw gateway restarts with prechecks, checkpointing, health checks, resume actions, reconciliation, reports, and notifications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe shell execution could run unintended commands with the user's OpenClaw privileges.

Mitigation: Review before installing, use only in a trusted local OpenClaw environment, avoid untrusted --next values and task plan files, and prefer removing cmd:/script: execution or replacing bash -lc with strict argument-array execution.

Risk: Detached restart or acceptance runners can continue after the caller exits or after a gateway restart interrupts the session.

Mitigation: Use the workflow only where detached local execution is expected, monitor the recorded runner log and state files, and run without real restart behavior unless the environment is trusted.

Risk: Custom ACTION_ALLOWLIST_FILE, GATEWAY_RESTART_CMD, task IDs, or notification arguments can change what the workflow executes or where results are sent.

Mitigation: Keep these values controlled by trusted operators, validate task plans before running, and avoid accepting these settings from untrusted input.

## Reference(s):

- [OpenClaw Restart Safe SOP](references/restart-safe-sop.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with bash commands and JSON status or report output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes restart state under state/restart and can send OpenClaw notifications when configured.]

## Skill Version(s):

1.0.3 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
