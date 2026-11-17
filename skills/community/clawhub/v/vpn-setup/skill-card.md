## Description:

Sets up a VPN server with WireGuard or OpenVPN on supported Linux distributions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[june910](https://clawhub.ai/user/june910)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and system administrators use this skill to install and configure a WireGuard or OpenVPN server, generate client configuration files, and inspect common management commands for supported Linux hosts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The OpenVPN path runs an unverified third-party installer as root.

Mitigation: Prefer the WireGuard path on a dedicated server, or pin and verify the OpenVPN installer before execution.

Risk: The installer makes high-impact system changes including firewall, routing, service, and key-file updates.

Mitigation: Review the script before installation, back up the host, and confirm those changes are acceptable for the target server.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/june910/skills/vpn-setup)
- [README.md](artifact/README.md)
- [SKILL.md](artifact/SKILL.md)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline bash commands and generated VPN configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bash and curl; writes system VPN configuration and client configuration files when executed.]

## Skill Version(s):

1.0.1 (source: server release metadata and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
