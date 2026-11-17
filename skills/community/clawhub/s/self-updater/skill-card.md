## Description:

Self Updater helps OpenClaw users check for and apply core and skill updates with cron-aware timing, idle detection, risk assessment, approvals, restart checks, and optional notifications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ghostdragon124](https://clawhub.ai/user/ghostdragon124)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to maintain OpenClaw installations by checking and applying core and skill updates while avoiding scheduled tasks and prompting on high-risk changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform unattended OpenClaw core and skill updates, and the referenced updater script is not included in the artifact.

Mitigation: Use it only where unattended updates are acceptable, verify the updater script source and integrity, and keep approval and notifications enabled for core or multi-skill updates.

Risk: The documentation includes unsafe PowerShell ExecutionPolicy Bypass examples.

Mitigation: Avoid those examples and run only trusted updater scripts under an appropriate local execution policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/ghostdragon124/skills/self-updater)
- [Project homepage](https://github.com/GhostDragon124/openclaw-self-updater#readme)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with PowerShell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes optional notification configuration for Telegram and Feishu.]

## Skill Version(s):

1.4.2 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
