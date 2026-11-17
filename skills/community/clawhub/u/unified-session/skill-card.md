## Description:

Unifies direct-message channels for a personal OpenClaw agent into one shared session so conversations can continue across devices without losing context.

This skill is ready for commercial/non-commercial use.

## Publisher:

[1052326311](https://clawhub.ai/user/1052326311)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and individual OpenClaw operators use this skill to diagnose and configure a single shared direct-message session for a personal agent across multiple chat channels.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Using a shared direct-message session for a bot that multiple people can DM can expose shared conversation context across users.

Mitigation: Install only for a personal or single-user OpenClaw agent; keep or revert dmScope to per-channel-peer for multi-user bots.

Risk: Session configuration changes can route future direct messages into one shared context until changed back.

Mitigation: Review the generated configuration before applying it, restart the gateway, verify session behavior, and use the documented rollback to restore isolated sessions when needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/1052326311/skills/unified-session)
- [README](artifact/README.md)
- [Skill source](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands and JSON configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Provides diagnostic, setup, restart, verification, troubleshooting, and rollback guidance for OpenClaw session configuration.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
