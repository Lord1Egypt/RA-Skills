## Description:

Restore Advantage HPE operational intelligence systems. Use when systems are down, missing alerts, broken scheduling, or data source issues. Covers LaunchD services, cron jobs, API fixes, and service restoration for zero revenue alerts, morning pulse, live nudges, and material truth reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[stephen550](https://clawhub.ai/user/stephen550)

### License/Terms of Use:

MIT-0

## Use Case:

Operations staff and developers use this skill to diagnose and restore Advantage HPE operational intelligence automations, including Slack alerts, scheduled reports, LaunchD services, cron jobs, and data-source repairs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can re-enable scheduled business automations and Slack posting.

Mitigation: Require explicit approval before overwriting scripts, creating cron jobs, or loading LaunchAgents; verify each plist target, script ownership, permissions, and expected hash before enabling scheduled execution.

Risk: An included data-source script may publish fixed mock records as if they were live data.

Mitigation: Do not deploy the mock browser data-source functions into production reporting; validate data source freshness and accuracy before reconnecting reports or alerts.

Risk: The skill identifies a local Slack token location as part of the restoration workflow.

Mitigation: Treat the Slack token path as sensitive secret material and avoid exposing token contents in logs, prompts, or generated documentation.

Risk: The restoration workflow is specific to a named macOS account and business systems.

Mitigation: Only install or use the skill in environments that control the named account and systems, and adjust paths and service identifiers only after owner review.

## Reference(s):

- [LaunchD Service Templates](references/launchd-service-templates.md)
- [Slack Channel IDs](references/channel-ids.md)
- [System Restoration Troubleshooting Checklist](references/troubleshooting-checklist.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, code]

**Output Format:** [Markdown with inline shell commands and code snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose filesystem, LaunchD, cron, and Slack-posting restoration steps that require review before execution.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
