## Description:

Direct SmartThings hub control via the official SmartThings CLI. List devices, read device status, and execute capability commands without going through Home Assistant.

This skill is ready for commercial/non-commercial use.

## Publisher:

[keenranger](https://clawhub.ai/user/keenranger)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to let an agent list SmartThings devices, inspect status, and issue direct SmartThings CLI commands for devices and scenes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can give an agent broad, persistent authority to directly control real SmartThings devices.

Mitigation: Install only when direct SmartThings control is intended, keep CLI credentials private, revoke tokens when no longer needed, and require explicit confirmation before consequential device or scene actions.

Risk: Personal access tokens can grant broad device, location, and scene scopes.

Mitigation: Prefer browser OAuth where possible, avoid broad PAT use for casual read-only tasks, and use short-lived or revoked PATs when they are no longer required.

Risk: Commands affecting scenes, HVAC, locks, security devices, or other consequential devices can have real-world effects.

Mitigation: Confirm the target device or scene, check status before acting when practical, and re-read status after consequential commands.

## Reference(s):

- [SmartThings CLI](https://github.com/SmartThingsCommunity/smartthings-cli)
- [SmartThings Personal Access Tokens](https://account.smartthings.com/tokens)
- [ClawHub skill listing](https://clawhub.ai/keenranger/skills/smartthings-direct)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown with inline shell commands and optional JSON CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires the SmartThings CLI and an authenticated SmartThings account.]

## Skill Version(s):

0.1.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
