## Description: <br>
Use when upgrading OpenClaw, running an OpenClaw upgrade, changing OpenClaw versions, selecting latest vs stable OpenClaw releases, or recovering from partial OpenClaw upgrades where gateway, config, plugins, channels, agents, or runtime availability must remain reliable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[skillmelody](https://clawhub.ai/user/skillmelody) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to plan, execute, and recover OpenClaw upgrades with verified backups, release-risk review, gateway/runtime checks, and plugin compatibility validation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may inspect local OpenClaw configuration, service status, plugin versions, and logs that can expose sensitive operational details. <br>
Mitigation: Keep inspection local, avoid publishing logs or configuration, and review confirmation prompts before sharing or acting on collected evidence. <br>
Risk: Upgrade, restart, rollback, daemon, sudo, cleanup, reinstall, and configuration changes can disrupt a running OpenClaw gateway or user workflows. <br>
Mitigation: Require a verified backup and separate explicit approval for each mutation or recovery action before execution. <br>
Risk: Version-sensitive OpenClaw commands or plugin-host version skew can make an upgrade appear complete while runtime routes still fail. <br>
Mitigation: Discover current command semantics, compare CLI and running gateway versions, check official plugin versions against the host, and verify critical paths with runtime probes. <br>


## Reference(s): <br>
- [OpenClaw Verified Upgrade on ClawHub](https://clawhub.ai/skillmelody/upgrade-openclaw-safely) <br>
- [Publisher profile](https://clawhub.ai/user/skillmelody) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with confirmation prompts, evidence tables, and command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user approval before upgrade, restart, rollback, cleanup, reinstall, daemon edits, sudo, or configuration mutation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
