## Description:

Use when an agent task has hit or is likely to hit a geo-related failure, or when the user explicitly asks to route a task through a specific country, by guiding the agent through X-VPN MCP tools for temporary region-specific egress.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xvpn-bot](https://clawhub.ai/user/xvpn-bot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external agent users use this skill when geography affects a web, API, or content retrieval task. It helps the agent decide whether VPN routing is appropriate, select an X-VPN location, restore the prior egress, and handle free-tier or tool-operation errors.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The installer is an unverified remote shell script that may install a daemon and modify local agent configuration.

Mitigation: Only run the installer after independently trusting the X-VPN distribution endpoint; prefer a versioned installer with checksum or signature verification.

Risk: Leaving the VPN tunnel connected after the geo-sensitive step can route unrelated user traffic through a different egress.

Mitigation: Record the starting VPN state, disconnect when finished, or reconnect to the original location if a tunnel was already active.

Risk: Free-tier users may see non-free locations that fail at connection time or may exhaust per-connection data during longer tasks.

Mitigation: Use the free location subtree for free accounts, surface upgrade or quota messages clearly, and ask before retrying long-running work.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/xvpn-bot/skills/xvpn-mcp-skill)
- [Call Patterns](references/call-patterns.md)
- [Task Integration](references/task-integration.md)
- [Locations](references/locations.md)
- [Free Tier](references/free-tier.md)
- [Error Recovery](references/error-recovery.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with MCP tool names and inline shell command blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may include VPN connection, disconnection, location-selection, error-recovery, and installer steps.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
