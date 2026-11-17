## Description:

System Load Monitor checks CPU and memory usage, recommends pausing or continuing work based on configured thresholds, and supports safer task pacing on low-resource servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hifengzy](https://clawhub.ai/user/hifengzy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to check CPU and memory pressure before resource-intensive work, pause when configured thresholds are exceeded, and resume after load recovers. It is intended for low-resource servers and long-running tasks that need periodic load checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Process listings can expose full command lines, including tokens, passwords, URLs, or private paths.

Mitigation: Treat JSON output and logs as sensitive, and redact or restrict process command output before sharing or storing it.

Risk: The skill can advise continuing when load checks fail or return incomplete metrics.

Mitigation: Review results before using the skill as an automatic task controller, and add explicit confirmation plus safer error handling for production workflows.

Risk: Running load checks on shared, production, or privileged servers can reveal operational details.

Mitigation: Review before installation in those environments and run with the least access needed for the monitoring task.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hifengzy/skills/system-load-monitor)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands, Python code patterns, status codes, and optional JSON output from the load-checking script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The load-checking script reports status, CPU and memory metrics, top processes, thresholds, and a CONTINUE or PAUSE recommendation.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
