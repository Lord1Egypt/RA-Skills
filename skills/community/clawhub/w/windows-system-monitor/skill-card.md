## Description:

Windows system status monitoring that checks CPU, memory, disk, network, process, and Windows event log health and notifies when issues are detected.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and Windows administrators use this skill to request system-health checks and receive status reports or alerts about resource pressure, abnormal processes, network issues, and relevant event-log problems.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Configured Feishu alerts may send host, process, network, or log status details outside the local machine.

Mitigation: Before enabling Feishu alerts or recurring checks, confirm the recipient, webhook or app configuration, and the exact details included in notifications.

Risk: System-health findings may be incomplete or stale if checks are not run at the intended frequency.

Mitigation: Use the documented daily, weekly, and monthly check cadence and review generated reports before taking operational action.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/jirboy/skills/windows-system-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with status summaries and inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference JSON health reports and Feishu, popup, or log notifications when configured.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
