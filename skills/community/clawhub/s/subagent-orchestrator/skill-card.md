## Description:

Orchestrates OpenClaw subagents for continuous autopilot workflows, including multi-round handoffs, task-board updates, memory preservation, and structured return rules.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hackjsw](https://clawhub.ai/user/hackjsw)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to keep OpenClaw subagent task lines moving across rounds, handoffs, validation follow-ups, memory updates, and completion checks without repeatedly restating the workflow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can continue autopilot work across rounds with less repeated prompting.

Mitigation: Use explicit task-board state, completion conditions, and blocked or need_user statuses to control when automated continuation stops.

Risk: The skill may guide agents to write project memory and task-board updates.

Mitigation: Confirm that durable memory records and task-board updates are acceptable for the project before enabling the workflow.

Risk: The skill may guide cleanup of screenshots, logs, temporary files, or intermediate outputs.

Mitigation: Preserve any evidence or artifacts needed for review before allowing cleanup.

## Reference(s):

- [SUBAGENT_RECORD_PROTOCOL](references/SUBAGENT_RECORD_PROTOCOL.md)
- [ClawHub skill page](https://clawhub.ai/hackjsw/skills/subagent-orchestrator)

## Skill Output:

**Output Type(s):** [guidance, markdown, configuration]

**Output Format:** [Markdown guidance with structured return headers and short report templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide task-board and memory-record updates during controller-managed subagent workflows.]

## Skill Version(s):

1.0.0 (source: package.json, README, server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
