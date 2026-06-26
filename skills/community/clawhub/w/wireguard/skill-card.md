## Description: <br>
Configure WireGuard VPN tunnels with secure routing and key management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and network operators use this skill to review WireGuard VPN configuration choices, avoid routing and DNS mistakes, protect keys, and troubleshoot handshakes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated WireGuard commands or configurations can disrupt routing, DNS, firewall/NAT behavior, or live interfaces if applied without review. <br>
Mitigation: Review AllowedIPs, DNS, NAT/firewall changes, and live wg operations before applying changes. <br>
Risk: WireGuard private keys and wg0.conf contents can expose VPN access if shared or stored insecurely. <br>
Mitigation: Keep private keys and configuration files secret, generate keys on each machine, and restrict private key file permissions. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline configuration and command references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated commands and configuration changes should be reviewed before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
