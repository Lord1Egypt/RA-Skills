## Description:

Multi-agent task orchestration engine with state machine tracking. Use when complex multi-step projects need automated monitoring, multi-agent collaboration, and Discord-based progress tracking.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zeron-g](https://clawhub.ai/user/zeron-g)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to create, dispatch, monitor, and archive multi-step work across Claude Code, Eva, and other agents. It is suited for coordinated projects that need JSON task state, heartbeat checks, dependency-aware dispatch, and Discord-formatted progress messages.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Task and subtask identifiers may allow file operations outside the intended task storage path if path validation is not fixed.

Mitigation: Validate task_id and subtask_id against the expected identifier formats before reading, writing, locking, archiving, or rebuilding task files.

Risk: A live-directory deletion command appears in the testing instructions.

Mitigation: Remove the live `rm -rf` test command and run destructive tests only against isolated temporary directories.

Risk: Bundled Discord configuration contains workspace-specific identifiers and generated notifications may expose task details externally.

Mitigation: Replace Discord IDs with values for the deployment workspace and review or redact formatted messages before posting outside the local team.

Risk: Task descriptions and prior agent outputs are reused in dispatch prompts and may contain untrusted instructions.

Mitigation: Treat stored task text and agent outputs as untrusted input; review dispatch context before sending it to another agent.

## Reference(s):

- [Agent Capabilities Reference](references/agent-capabilities.md)
- [State Transitions Reference](references/state-transitions.md)
- [Task Engine on ClawHub](https://clawhub.ai/zeron-g/skills/task-engine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell command examples, JSON CLI responses, dispatch prompts, and Discord-formatted text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses local JSON task files, heartbeat checks, and configured Discord identifiers; review generated dispatch prompts and notifications before external posting.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
