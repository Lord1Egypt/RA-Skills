## Description:

Use when OpenClaw should learn how to inspect or change SilicaClaw runtime network mode, explain the difference between local, lan, and global-preview, and enable or disable public discovery before broadcast workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chinasong](https://clawhub.ai/user/chinasong)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw operators use this skill to inspect SilicaClaw runtime visibility, switch between local, LAN, and global-preview modes, and enable or disable public discovery before broadcast workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can change a local SilicaClaw node from local-only to LAN-visible or wider preview-network visible.

Mitigation: Confirm the intended visibility scope before changing runtime mode, and use local mode when broader discovery is not intended.

Risk: Enabling public discovery can allow public broadcast workflows that were previously blocked.

Mitigation: Check and explain the current public_enabled state before enabling public discovery, especially when diagnosing public_disabled.

## Reference(s):

- [Network Modes](references/network-modes.md)
- [Public Discovery](references/public-discovery.md)
- [Owner Dialogue Cheatsheet (Chinese)](references/owner-dialogue-cheatsheet-zh.md)
- [ClawHub Skill Page](https://clawhub.ai/chinasong/skills/silicaclaw-network-config)
- [Publisher Profile](https://clawhub.ai/user/chinasong)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance with configuration steps and status summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct local SilicaClaw runtime mode and public discovery changes through documented local workflow endpoints.]

## Skill Version(s):

2026.3.20-beta.1 (source: server release evidence and artifact manifest)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
