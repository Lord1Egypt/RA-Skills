## Description:

Task Notifier helps agents guide users through installing, configuring, verifying, troubleshooting, updating, or removing desktop notifications for completed OpenClaw agent tasks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wdgame](https://clawhub.ai/user/wdgame)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to manage Task Notifier setup and operations so they can receive desktop notifications when long-running main-agent or subagent tasks finish. It also provides consent, verification, configuration, and rollback guidance for the separate runtime plugin.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installing Task Notifier requires an unsafe-install bypass for a separate persistent runtime plugin with OpenClaw lifecycle access that was not included for review.

Mitigation: Install only after explicit user consent, prefer a reviewed and pinned runtime version or source bundle, and use the documented disable, uninstall, and state-cleanup steps if removing it.

Risk: The runtime plugin can inspect active foreground window titles, run local notification commands, and write per-run state files in active workspaces.

Mitigation: Review the requested permissions before installation, keep agent filters and active-window matching narrowly configured, and run the documented doctor check after setup.

## Reference(s):

- [Task Notifier ClawHub Page](https://clawhub.ai/wdgame/skills/task-notifier)
- [Task Notifier Reference README](references/README.md)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown guidance with bash command blocks and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides install, verification, debugging, configuration, and rollback guidance; desktop notification behavior depends on a separate runtime plugin.]

## Skill Version(s):

1.1.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
