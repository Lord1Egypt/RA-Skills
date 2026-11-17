## Description:

Lightweight system health monitoring for macOS that checks CPU, memory, disk usage, network status, cron job status, and generates health reports with Discord notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sunnyhot](https://clawhub.ai/user/sunnyhot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to monitor local macOS system health and OpenClaw cron-job status, calculate a health score, and produce actionable reports. It can run manually or on a schedule and can post summarized reports to Discord.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may send local system health and cron-job status data to an embedded Discord webhook unless the destination is explicitly overridden.

Mitigation: Review the skill before running it, remove or revoke the fallback webhook, and configure SYSTEM_HEALTH_WEBHOOK to a destination controlled by the user.

## Reference(s):

- [Sunny Health Monitor ClawHub page](https://clawhub.ai/sunnyhot/skills/sunny-health-monitor)
- [sunnyhot publisher profile](https://clawhub.ai/user/sunnyhot)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown health report, JSON status file, and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports may be truncated before Discord delivery.]

## Skill Version(s):

1.0.0 (source: server release metadata, frontmatter, package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
