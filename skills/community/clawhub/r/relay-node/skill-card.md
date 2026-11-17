## Description:

Relay Node guides agents through configuring relay nodes that forward connections through SOCKS5, SSH tunnels, WireGuard proxying, HTTP proxying, or TCP bridges when direct network paths are unavailable.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kikikari](https://clawhub.ai/user/kikikari)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan relay behavior for nodes behind NAT, nodes without WireGuard support, and file-sharing or service-forwarding scenarios where direct connectivity is unavailable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Relay configuration guidance can expose internal network services or storage paths if applied too broadly.

Mitigation: Enable relays only for specific trusted hosts and ports, restrict bind addresses and exposed directories, and avoid relaying directly to sensitive storage paths.

Risk: Relay paths can create unauthorized access if authentication, encryption, and auditing are not required.

Mitigation: Require authentication and encryption, confirm how to disable relay settings, and audit active relay connections before production use.

## Reference(s):

- [Relay Node on ClawHub](https://clawhub.ai/kikikari/skills/relay-node)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration]

**Output Format:** [Markdown with bash and INI code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes relay modes, command examples, configuration examples, and deployment scenarios.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
