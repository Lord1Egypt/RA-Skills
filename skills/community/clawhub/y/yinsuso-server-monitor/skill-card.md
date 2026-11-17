## Description:

Monitors Linux server CPU, memory, disk, load, and network resources with native commands, threshold checks, and optional scheduled monitoring.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yinsuso](https://clawhub.ai/user/yinsuso)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect Linux server resource health, identify high CPU, memory, disk, load, network, or process conditions, and receive concise status or threshold guidance. Scheduled checks should be used only after the operator approves the exact cron or heartbeat behavior.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Recurring cron or heartbeat monitoring may persist beyond the immediate session without enough user control, cleanup, or persistence disclosure.

Mitigation: Review the exact cron or heartbeat change before installation, confirm where it runs and what notifications it sends, and document how to remove it later.

Risk: Server health commands and threshold summaries can be misleading if Linux tools, interface names, or optional utilities differ from the target host.

Mitigation: Confirm command availability and adjust interface names or thresholds for the host before acting on alerts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yinsuso/skills/yinsuso-server-monitor)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with bash command blocks and concise status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include threshold findings and scheduled-monitoring instructions when explicitly requested.]

## Skill Version(s):

1.0.0 (source: server release metadata, target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
