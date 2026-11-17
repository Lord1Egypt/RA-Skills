## Description:

Configure WireGuard VPN tunnels with secure routing and key management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and network administrators use this skill to reason about WireGuard VPN tunnel configuration, routing, key handling, and troubleshooting before applying changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: WireGuard configuration changes can affect all network traffic.

Mitigation: Review generated configs before applying them.

Risk: Private keys and wg0.conf can expose VPN access if shared or stored with loose permissions.

Mitigation: Keep private keys and wg0.conf secret and use restrictive file permissions.

## Reference(s):

- [WireGuard Skill on ClawHub](https://clawhub.ai/ivangdavila/skills/wireguard)

## Skill Output:

**Output Type(s):** [guidance, configuration, shell commands]

**Output Format:** [Markdown]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include WireGuard configuration review notes and command suggestions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
