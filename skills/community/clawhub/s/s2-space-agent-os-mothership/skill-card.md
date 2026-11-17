## Description:

A spatial logic framework for Openclaw that provides local state compression and coordinate management while operating in user space.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and advanced Openclaw users use this skill to add spatial state, coordinate allocation, local memory compression, and smart-home command validation around local agents. It is intended for environments where the operator explicitly reviews network, credential, and actuation access before enabling real device control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes smart-home actuation, LAN discovery, root-agent integration, and persistent agent-behavior changes.

Mitigation: Review the artifact manually and test in an isolated environment before installing it into a real home, LAN, or agent runtime.

Risk: Providing HA, Tuya, or Mijia credentials can allow the skill to interact with physical devices.

Mitigation: Do not provide real smart-home credentials until the operator has reviewed the code paths and explicitly intends to grant device access.

Risk: Enabling real actuation, Docker host networking, or root-agent privileges can expand access to the local network and physical devices.

Mitigation: Keep S2_ENABLE_REAL_ACTUATION disabled and avoid host networking or elevated privileges unless those capabilities are required and accepted.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/spacesq/skills/s2-space-agent-os-mothership)
- [Project Homepage](https://github.com/SpaceSQ/s2-os-core)
- [Skill Manifest](artifact/SKILL.md)
- [Deployment and Network Topology Guide](artifact/S2_DEPLOYMENT_&_NETWORK_TOPOLOGY.md)
- [Full Architecture Guide](artifact/S2_FULL_ARCHITECTURE_GUIDE.md)
- [OpenClaw 3.22 Heartbeat Configuration](artifact/openclaw_322_support/HEARTBEAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline code, command examples, and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Python execution, SQLite-backed state files, network configuration, and optional smart-home adapter setup.]

## Skill Version(s):

1.1.3 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
