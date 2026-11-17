## Description:

Connects a running agent runtime to XMTP messaging so people can DM it, stream incoming text messages, route them through the agent backend, and send replies back through XMTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[saulmc](https://clawhub.ai/user/saulmc)

### License/Terms of Use:


## Use Case:

Developers and agent operators use this skill to expose an existing agent over XMTP for continuous two-way conversations. It provides setup guidance, bridge-script patterns, backend routing examples, and owner-versus-public session handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead to a continuously reachable public XMTP agent bridge.

Mitigation: Require explicit owner approval before starting or deploying the long-running bridge, and install it only when continuous XMTP reachability is intended.

Risk: Public messages may reach an agent backend, and prompt-only restrictions are not a strong access-control boundary.

Mitigation: Route public users to a separate restricted agent or isolated process with filesystem, shell, secrets, and owner memory disabled.

Risk: XMTP setup creates wallet and encryption key material that must remain protected.

Mitigation: Use a pinned or local XMTP CLI install and protect generated wallet and encryption keys.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/saulmc/skills/xmtp-agents)

## Skill Output:

**Output Type(s):** [markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Bash, JSON, and Python snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes long-running bridge patterns for XMTP CLI, OpenClaw, Claude Code, and custom stdin/stdout agent backends.]

## Skill Version(s):

0.0.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
