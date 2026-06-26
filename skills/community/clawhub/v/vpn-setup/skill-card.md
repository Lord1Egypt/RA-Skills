## Description: <br>
Sets up a VPN server with WireGuard or OpenVPN on supported Linux distributions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[june910](https://clawhub.ai/user/june910) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and system administrators use this skill to install and configure a WireGuard or OpenVPN VPN host, generate client configuration, and review related management commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can reconfigure a server as a VPN host and make system-level network, firewall, package, and service changes. <br>
Mitigation: Install only on a server intended to become a VPN host, review the script before execution, and run as root only with explicit intent. <br>
Risk: The OpenVPN path runs an unverified internet-downloaded installer as root. <br>
Mitigation: Prefer the WireGuard path, or pin and independently verify the OpenVPN installer before using that option. <br>
Risk: Generated client configuration files and private keys can grant VPN access if exposed. <br>
Mitigation: Protect generated client configurations and private keys, distribute them only to intended devices, and rotate credentials if they are exposed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/june910/vpn-setup) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with bash command examples and VPN configuration paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May generate VPN client configuration files and private keys on the target host.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
