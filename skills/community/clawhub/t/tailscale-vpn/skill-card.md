## Description: <br>
Provides Chinese-language guidance for installing and using Tailscale, a WireGuard-based VPN for secure remote access, device networking, subnet routing, exit nodes, and ACLs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smseow001](https://clawhub.ai/user/smseow001) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, IT administrators, and remote workers use this skill to set up Tailscale clients and configure secure access to devices, servers, and private networks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Tailscale installation and setup changes system networking, can require administrator privileges, and may run a background service. <br>
Mitigation: Verify official Tailscale sources before installing and prefer a trusted package manager when available. <br>
Risk: Subnet routes, sharing, and exit nodes can expose or route network access if configured too broadly. <br>
Mitigation: Review ACLs, route approvals, sharing settings, and exit-node configuration before enabling broad network access. <br>


## Reference(s): <br>
- [Tailscale official site](https://tailscale.com) <br>
- [Tailscale Windows download](https://tailscale.com/download/windows) <br>
- [Tailscale Linux install script](https://tailscale.com/install.sh) <br>
- [Tailscale ACL admin page](https://login.tailscale.com/admin/acls) <br>
- [ClawHub skill page](https://clawhub.ai/smseow001/tailscale-vpn) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with command snippets and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language setup and troubleshooting guidance for Tailscale VPN usage.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
