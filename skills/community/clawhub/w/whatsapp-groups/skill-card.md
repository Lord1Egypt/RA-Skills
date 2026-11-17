## Description:

Discover, list, and search WhatsApp groups from Baileys session data.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marcosrippel](https://clawhub.ai/user/marcosrippel)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw operators use this skill to inspect WhatsApp groups visible in local Baileys session files, search for group names or IDs, and optionally sync newly discovered groups into OpenClaw configuration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads local WhatsApp Baileys session-derived files that may expose group names and IDs.

Mitigation: Install and run it only in environments where access to local WhatsApp session data is intended, and review command output before sharing it.

Risk: The sync command can modify openclaw.json by adding newly discovered groups.

Mitigation: Run sync only when configuration changes are desired, then review openclaw.json before enabling any added groups.

## Reference(s):

- [WhatsApp Groups on ClawHub](https://clawhub.ai/marcosrippel/skills/whatsapp-groups)
- [Publisher profile: marcosrippel](https://clawhub.ai/user/marcosrippel)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [JSON printed by Node.js CLI commands, with command guidance in Markdown.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Group listings include group IDs, display names when available, and active status from OpenClaw configuration.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
