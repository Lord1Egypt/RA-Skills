## Description:

Helps agents search local OpenClaw documentation and use embedded configuration patterns before changing openclaw.json.

This skill is ready for commercial/non-commercial use.

## Publisher:

[karmanverma](https://clawhub.ai/user/karmanverma)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to find the right OpenClaw documentation and apply safer patterns for bindings, channels, sessions, cron jobs, heartbeats, and configuration troubleshooting.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents toward OpenClaw configuration changes such as config.patch, restarts, cron jobs, heartbeat updates, or restores.

Mitigation: Review proposed configuration and operational actions before execution, then verify gateway status and behavior after the change.

Risk: Search output includes local file paths and suggested cat commands, which may be unsafe if the local documentation index is untrusted.

Mitigation: Build the index only from trusted OpenClaw documentation and read returned paths through a trusted file API or safely quoted command.

Risk: Setup depends on local Node.js execution and the better-sqlite3 package dependency.

Mitigation: Install only when the local OpenClaw docs tree and package dependency resolution are trusted.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/karmanverma/skills/search-openclaw-docs)
- [OpenClaw Docs Search Homepage](https://github.com/karmanverma/search-openclaw-docs)
- [Best Practices: OpenClaw Configuration](references/best-practices-config.md)
- [Config Pattern: Agent Bindings](references/config-bindings.md)
- [Config Pattern: Channel Management](references/config-channel-management.md)
- [Config Pattern: Cron Jobs](references/config-cron.md)
- [Config Pattern: Heartbeat](references/config-heartbeat.md)
- [Config Pattern: Session Reset](references/config-session-reset.md)
- [Migration: OpenClaw 2026.2.9 Changes](references/migration-2026-2-9.md)
- [Troubleshooting: Config Breaks After Changes](references/troubleshooting-config-breaks.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and optional JSON search results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Offline local documentation search that returns file paths for the agent to read before acting.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
