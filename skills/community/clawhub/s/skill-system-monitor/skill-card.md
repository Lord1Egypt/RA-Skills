## Description:

System Monitor helps an agent run local host checks for disk, memory, CPU, network, Docker, service status, saved history, trend comparison, and threshold alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[weznai](https://clawhub.ai/user/weznai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill for manual or scheduled health checks of server environments, reviewing resource usage, service state, alerts, and changes across saved snapshots.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Scheduled monitoring collects and retains host telemetry such as uptime, resource usage, network counters, Docker counts, service status, and top process names.

Mitigation: Run as an unprivileged user, restrict access to the history directory, and deploy only where local telemetry retention is acceptable.

Risk: Trend reports can expose disk and memory history through generated QuickChart links.

Mitigation: Open or share generated chart links only when sending that history to quickchart.io is acceptable.

Risk: The security summary flags ineffective disable settings, cleanup handling concerns, and configuration-handling issues.

Mitigation: Review or fix cleanup and configuration behavior before use on shared or production systems.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/weznai/skills/skill-system-monitor)
- [QuickChart chart endpoint used by trend reports](https://quickchart.io/chart?w=500&h=300&c={encoded})

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Plain-text monitoring reports with JSON history files and optional chart URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores local host telemetry history for trend comparison.]

## Skill Version(s):

1.0.1 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
