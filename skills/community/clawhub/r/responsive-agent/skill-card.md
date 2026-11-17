## Description:

Responsive Agent guides OpenClaw agents to keep the main session responsive by spawning subagents for long, remote, state-changing, or uncertain work and using exec plus yieldMs controls inside subagents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guytogay](https://clawhub.ai/user/guytogay)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to keep OpenClaw sessions responsive while dispatching long, remote, state-changing, or uncertain work to subagents. It provides practical guidance for spawn decisions, timeout and yield settings, queueing, cancellation, logging, and result handoff.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Background subagents can run broad user-requested work with limited foreground visibility.

Mitigation: Install only where background subagent execution is acceptable, keep concurrency limits and cancellation handling in place, and require subagents to report completion or failure back to the parent session.

Risk: Persistent task and error logs may capture secrets or private command output.

Mitigation: Redact secrets and private output before logging, bound retention, and review archive or cleanup policy for task and error logs before deployment.

Risk: Rate-limit waits may be converted into shell sleep commands.

Mitigation: Validate retry and wait values as numeric bounded durations before using them in shell commands.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/guytogay/skills/responsive-agent)
- [ClawHub publisher profile](https://clawhub.ai/user/guytogay)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline command examples and decision tables]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes operational thresholds for subagent spawning, timeout selection, queueing, cancellation, logging, and cleanup.]

## Skill Version(s):

1.8.1 (source: server release metadata; artifact frontmatter states 1.8.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
