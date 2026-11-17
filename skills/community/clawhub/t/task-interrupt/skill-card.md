## Description:

任务打断机制 helps OpenClaw agents interrupt long-running or stalled tasks through stop signals, polling checks, checkpointing, and cleanup guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guyxlouspg](https://clawhub.ai/user/guyxlouspg)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent integrators use this skill to add task interruption behavior to OpenClaw agents and subagents, including user-triggered stopping, checkpoint saving, and resource cleanup for long-running work.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The interrupt mechanism can grant process-control and filesystem mutation authority with unsafe scoping.

Mitigation: Review and harden the mechanism before installation, including strict session ID allowlists and validated session-to-PID ownership before sending SIGINT or deleting files.

Risk: Stop flags and state files may be exposed or altered if stored in broadly shared temporary paths.

Mitigation: Store flags in a private 0700 directory, create files atomically without following links, encode JSON values safely, and avoid shell exec for script invocation.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guyxlouspg/skills/task-interrupt)
- [OpenClaw 官方文档](https://openclaw.org/docs)
- [AgentSkill 规范](https://clawhub.com/specs/agent-skill)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline JavaScript and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes task-interruption workflow guidance, stop-flag script usage, checkpointing patterns, and cleanup recommendations.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
