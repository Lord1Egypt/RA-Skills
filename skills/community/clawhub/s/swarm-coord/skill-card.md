## Description:

Swarm Coord helps an agent decompose compound tasks, dispatch parallel sub-agent sessions, monitor progress, and aggregate the results.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wavmson](https://clawhub.ai/user/wavmson)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to coordinate multi-domain tasks by splitting work into parallel subtasks, assigning them to specialized agents, monitoring progress, and producing a unified final report.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Coordinated sub-agents may perform side effects such as modifying files, sending messages, pushing code, or persisting task state.

Mitigation: Review the swarm plan before execution, including assigned sub-agents, touched files or services, and any proposed external or persistent action.

Risk: Parallel subtasks can fail, time out, or produce partial results that affect the final aggregate report.

Mitigation: Track each subtask status, mark failed or skipped work explicitly, and review the unified report before acting on its conclusions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/wavmson/skills/swarm-coord)
- [OpenClaw](https://github.com/openclaw/openclaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown guidance with task plans, sub-agent instructions, progress updates, and aggregated reports]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include session-spawning steps and status summaries for delegated subtasks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
