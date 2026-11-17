## Description:

快速识别并立即中断当前执行任务，清理相关资源，节省 token 和时间，准备执行新任务。

This skill is ready for commercial/non-commercial use.

## Publisher:

[shiker1996](https://clawhub.ai/user/shiker1996)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users and developers use this skill to stop an active task when the direction is wrong, requirements change, or continued execution would waste time and tokens. It provides interruption language, cleanup expectations, and examples for resuming with a new task.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger phrases can stop active work unexpectedly.

Mitigation: Prefer explicit slash commands for destructive interruption, and confirm ambiguous stop requests before killing sessions.

Risk: Cleanup behavior can terminate visible subagents and process sessions without reliable scoping.

Mitigation: Limit cleanup to resources created by the current task and show a preview of affected sessions before termination.

Risk: Temporary-file cleanup may remove useful in-progress work.

Mitigation: Keep temporary-file cleanup opt-in and preserve an interruption record so the user can restart with context.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/shiker1996/skills/task-killer)
- [Publisher profile](https://clawhub.ai/user/shiker1996)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands]

**Output Format:** [Markdown guidance with command examples and JavaScript snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include cleanup summaries for stopped subagents, background processes, and temporary files.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
