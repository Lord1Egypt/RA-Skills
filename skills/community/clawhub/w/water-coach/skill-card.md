## Description:

Hydration tracking and coaching skill. Use when user wants to track water intake, get reminders to drink water, log body metrics, or get analytics on hydration habits.

This skill is ready for commercial/non-commercial use.

## Publisher:

[oristides](https://clawhub.ai/user/oristides)

### License/Terms of Use:


## Use Case:

External users and their agents use this skill to set up hydration goals, log water intake and body metrics, schedule reminders, and generate hydration status or analytics reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Water logging can inspect assistant session transcript files to capture message identifiers.

Mitigation: Review transcript access before installation and remove or isolate audit transcript access when message-level proof is not required.

Risk: The package bundles an unrelated MCP utility with network, local process, authentication, configuration, and daemon capabilities.

Mitigation: Install only after reviewing that bundled utility, or remove or isolate the mcporter skill before use.

Risk: The skill stores health-tracking data locally in the agent workspace.

Mitigation: Use it only in workspaces where local hydration and body-metric files are acceptable, and apply normal workspace privacy and backup controls.

## Reference(s):

- [Water Coach ClawHub Skill Page](https://clawhub.ai/oristides/skills/water-coach)
- [Water Coach Setup](references/setup.md)
- [Water Coach Log Formats](references/log_format.md)
- [Dynamic Scheduling](references/dynamic.md)
- [Water Coach Agent Evaluation](evaluation/AGENT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with CLI commands and JSON or CSV-backed status and analytics output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Stores hydration logs, body metrics, reminder configuration, and message audit identifiers in local workspace data files.]

## Skill Version(s):

1.7.0 (source: server release metadata and changelog, released 2026-02-22)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
