## Description: <br>
Enables relay nodes to forward connections via SOCKS5, SSH tunnels, WireGuard proxy, HTTP proxy, or TCP bridges when direct network paths are unavailable. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kikikari](https://clawhub.ai/user/kikikari) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure relay paths for OpenClaw nodes that cannot connect directly because of missing WireGuard support, NAT, or service forwarding needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Relay and port-forwarding commands can expose network services. <br>
Mitigation: Before running relay or forwarding commands, confirm bind addresses, authentication, source allowlists, encryption, logging, and who can reach forwarded ports. <br>
Risk: Relay exposure may be broader than intended if public access is used by default. <br>
Mitigation: Prefer localhost-only or private-network exposure unless public access is explicitly approved. <br>


## Reference(s): <br>
- [Relay Node on ClawHub](https://clawhub.ai/kikikari/relay-node) <br>
- [Cluster Gateway Skill](../cluster-gateway/SKILL.md) <br>
- [Worker Node Skill](../worker-node/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash and INI code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes relay mode choices, forwarding commands, status checks, and configuration examples.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
