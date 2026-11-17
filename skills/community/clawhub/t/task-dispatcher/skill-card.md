## Description:

Task Dispatcher analyzes user, cron, or heartbeat-triggered work, breaks it into steps, routes subtasks to appropriate subagents, monitors progress, reports status, and falls back when delegated work fails.

This skill is ready for commercial/non-commercial use.

## Publisher:

[thomaschangx](https://clawhub.ai/user/thomaschangx)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to coordinate multi-step work across specialized subagents, including planning, code work, review, testing, documentation, scheduling, and cleanup.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Automatic cleanup rules can move broad classes of project or user files to trash without confirmation.

Mitigation: Disable cleanup by default or restrict it to explicit task-owned directories; require dry-run and user confirmation before moving files to trash.

Risk: Broad task routing and cron-style behavior can delegate or schedule work beyond the user's immediate intent.

Mitigation: Require confirmation of task plans, scope, agent assignments, risk level, and scheduled actions before execution.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/thomaschangx/skills/task-dispatcher)
- [Supplementary Design](references/SUPPLEMENTARY_DESIGN.md)
- [Agent Mapping Configuration](references/config/agents.yaml)
- [Budget Configuration](references/config/budget.yaml)
- [Cleanup Configuration](references/config/cleanup.yaml)
- [Pipeline Configuration](references/config/pipelines.yaml)
- [Review Configuration](references/config/review.yaml)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown task plans, progress reports, review summaries, and inline command or configuration examples.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include task routing tables, risk levels, retry decisions, status checklists, YAML-style configuration, and cleanup guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
