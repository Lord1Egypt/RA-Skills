## Description:

Task decomposition and execution framework for Claude that breaks complex work into verified subtasks, plants context anchors to survive compaction, and keeps execution aligned with the original goal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jiajiaoy](https://clawhub.ai/user/jiajiaoy)

### License/Terms of Use:

MIT-0

## Use Case:

External developers and agent users use this skill to plan, checkpoint, and recover longer multi-step Claude or Claude Code tasks. It is intended for work that spans multiple steps or exchanges where scope drift, compaction, or missed verification could cause rework.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill deliberately adds planning, confirmation, checkpointing, and recovery steps, which can slow short or single-step tasks.

Mitigation: Use it for multi-step work and skip it for quick lookups, single-response tasks, or tasks that do not need checkpointing.

Risk: Strict scope discipline can require explicit plan updates when requirements change mid-task.

Mitigation: Pause to update the plan and confirm the revised scope before continuing.

## Reference(s):

- [Task Pilot on ClawHub](https://clawhub.ai/skills/task-pilot)
- [Task Pilot release page](https://clawhub.ai/jiajiaoy/skills/task-pilot)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with structured task plans, checkpoints, context anchors, recovery notes, and completion summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No executable code, tool calls, credential handling, or hidden data access were identified in the release evidence.]

## Skill Version(s):

1.0.3 (source: server release evidence; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
