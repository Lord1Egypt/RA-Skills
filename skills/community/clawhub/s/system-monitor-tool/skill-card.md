## Description:

System resource monitoring (CPU, memory, disk, network). Use when user asks "system status", "CPU usage", "memory usage", "disk space", or wants to monitor system resources.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yushimohuang](https://clawhub.ai/user/yushimohuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and external users use this skill to ask an agent for local system status, CPU, memory, disk, network, process, uptime, and temperature summaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: User-controlled process count or monitoring interval values may trigger unintended command execution through argument handling.

Mitigation: Review and fix argument validation before allowing user-controlled values; accept only bounded numeric values for counts and intervals.

Risk: The skill can expose local host telemetry, process details, network status, disk usage, and home directory size summaries.

Mitigation: Use only in environments where exposing local system details is acceptable, and avoid running it on sensitive shared hosts without review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yushimohuang/skills/system-monitor-tool)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summaries with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May expose local host telemetry, process details, network status, and disk usage.]

## Skill Version(s):

1.0.0 (source: server release metadata and script header)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
