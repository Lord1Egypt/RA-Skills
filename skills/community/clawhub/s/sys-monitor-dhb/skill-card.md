## Description:

Monitor system metrics like CPU, memory, disk, and network.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dinghaibin](https://clawhub.ai/user/dinghaibin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Linux system health, monitor CPU, memory, disk, network, uptime, and process status, and configure threshold alerts for resource usage.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: System metrics and process output can expose local file paths, usernames, host details, or secrets passed as command-line arguments.

Mitigation: Review monitor output before sharing it and avoid publishing raw JSON or process listings publicly.

Risk: The skill reads local system metrics and process information.

Mitigation: Install and run it only in environments where that local visibility is acceptable.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/dinghaibin/skills/sys-monitor-dhb)

## Skill Output:

**Output Type(s):** [Text, JSON, Shell commands, Guidance]

**Output Format:** [Plain text or JSON status output, with Markdown guidance and bash commands when explaining usage.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local process names, usernames, file paths, host details, and resource metrics when process or JSON output is requested.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
