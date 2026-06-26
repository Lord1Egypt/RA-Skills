## Description: <br>
MANDATORY before any openclaw.json changes. Prevents config breakage via embedded anti-patterns and correct patterns. Use when configuring OpenClaw (bindings, channels, sessions, cron, heartbeat) or troubleshooting config issues. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[karmanverma](https://clawhub.ai/user/karmanverma) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and engineers use this skill before changing OpenClaw configuration to find the right embedded pattern, avoid known anti-patterns, and search the local OpenClaw documentation index when a topic is not covered by the references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Troubleshooting examples can overwrite configuration or delete old sessions if followed carelessly. <br>
Mitigation: Make a fresh backup, review diffs, and confirm retention requirements before following restore or cleanup snippets. <br>
Risk: The skill may be invoked for unrelated tasks if trigger phrases are too broad. <br>
Mitigation: Use OpenClaw-specific trigger phrases so the skill is applied only to OpenClaw setup, configuration, and troubleshooting. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/karmanverma/search-openclaw-docs) <br>
- [Homepage from ClawHub metadata](https://github.com/karmanverma/search-openclaw-docs) <br>
- [Best Practices: OpenClaw Configuration](references/best-practices-config.md) <br>
- [Config Pattern: Agent Bindings](references/config-bindings.md) <br>
- [Config Pattern: Channel Management](references/config-channel-management.md) <br>
- [Config Pattern: Cron Jobs](references/config-cron.md) <br>
- [Config Pattern: Heartbeat](references/config-heartbeat.md) <br>
- [Config Pattern: Session Reset](references/config-session-reset.md) <br>
- [Migration: OpenClaw 2026.2.9 Changes](references/migration-2026-2-9.md) <br>
- [Troubleshooting: Config Breaks After Changes](references/troubleshooting-config-breaks.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and optional JSON search results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Search results return local OpenClaw documentation paths to read; the skill requires Node.js, better-sqlite3, and a locally built OpenClaw docs index.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata; package.json reports 2.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
