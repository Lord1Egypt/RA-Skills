## Description: <br>
Monitors subagent failures, abnormal exec exits, and stale tasks, then notifies the active session when attention is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmlgit](https://clawhub.ai/user/zmlgit) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this plugin to surface failed subagents, abnormal shell command exits, and stale long-running tasks without repeatedly checking task state manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The plugin auto-starts, runs periodic watchdog checks, and can inject notifications into active sessions. <br>
Mitigation: Enable it only in workspaces where automatic task monitoring is desired, and review the timerPatrol, heartbeatPatrol, timerPatrolIntervalMs, and staleThresholdMs settings before use. <br>
Risk: The reviewed artifacts reference runtime code at ./dist/index.mjs that was not included in the evidence bundle. <br>
Mitigation: Verify the installed npm package contents, especially ./dist/index.mjs, before enabling the plugin. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zmlgit/task-watchdog-plugin) <br>
- [Publisher profile](https://clawhub.ai/user/zmlgit) <br>
- [README](README.md) <br>
- [OpenClaw plugin manifest](openclaw.plugin.json) <br>
- [Package manifest](package.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Session notifications and heartbeat prompt contributions with JSON configuration options.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Notifications are driven by configured subagent outcomes, exec abnormal exits, and stale-task timing thresholds.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata, package.json, README changelog) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
