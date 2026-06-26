## Description: <br>
Task Dispatcher coordinates multi-step user, scheduled, or heartbeat-triggered work by analyzing requirements, breaking tasks into subagent assignments, monitoring progress, reporting status, and handling fallback when work fails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ThomasChangX](https://clawhub.ai/user/ThomasChangX) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent users use this skill to plan, delegate, monitor, review, and close out multi-step work across specialized subagents. It is suited to direct user tasks, scheduled or heartbeat-triggered work, and workflows that need structured task breakdown, confirmation, progress reporting, and fallback handling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The dispatcher can share task context with subagents during orchestration. <br>
Mitigation: Review task context before dispatch and avoid sending secrets or unnecessary sensitive data to subagents. <br>
Risk: Bundled cleanup rules can automatically delete broad local file patterns without sufficient user control. <br>
Mitigation: Disable automatic cleanup, enable dry-run, require confirmation, remove .env and media patterns, and restrict deletion to explicitly approved task-created temporary paths. <br>


## Reference(s): <br>
- [Supplementary Design](references/SUPPLEMENTARY_DESIGN.md) <br>
- [Agent Configuration](references/config/agents.yaml) <br>
- [Budget Configuration](references/config/budget.yaml) <br>
- [Cleanup Configuration](references/config/cleanup.yaml) <br>
- [Pipeline Configuration](references/config/pipelines.yaml) <br>
- [Review Configuration](references/config/review.yaml) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown task plans, progress updates, completion summaries, subagent dispatch command examples, and configuration-oriented guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May share task context with subagents and may produce cleanup or orchestration guidance that should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
