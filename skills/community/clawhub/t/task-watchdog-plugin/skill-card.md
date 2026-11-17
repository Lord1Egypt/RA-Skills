## Description:

Task Watchdog monitors subagent failures, abnormal exec exits, and stale tasks, then injects notifications or patrol guidance into parent OpenClaw sessions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zmlgit](https://clawhub.ai/user/zmlgit)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this plugin to surface failed subagents, abnormal shell executions, and stale long-running tasks without manually polling sessions. It is intended for task supervision and operational notifications in agent workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The submitted artifact does not include the executable dist/index.mjs that the plugin manifest and package metadata load.

Mitigation: Install only a pinned, audited release that includes the executable file or matching source and provenance.

Risk: The plugin starts automatically and can inject notifications into parent sessions.

Mitigation: Review the package before installation and configure notification triggers, injection TTL, and patrol settings to match the workspace's tolerance for automated messages.

Risk: Timer-based patrol can create recurring background checks.

Mitigation: Disable timerPatrol or adjust timerPatrolIntervalMs and staleThresholdMs when recurring checks are not desired.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zmlgit/skills/task-watchdog-plugin)
- [Publisher profile](https://clawhub.ai/user/zmlgit)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown-style notifications, install commands, and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Automatically starts on gateway startup; notification, heartbeat, and timer patrol behavior are configurable.]

## Skill Version(s):

1.1.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
