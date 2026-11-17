## Description:

Guides agents and users through Tailscale setup and secure virtual networking for remote access, home office use, server management, and encrypted device-to-device connectivity.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smseow001](https://clawhub.ai/user/smseow001)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, administrators, and technical users use this skill to install Tailscale clients, connect devices into a private WireGuard-based network, configure ACLs, and apply subnet routing or exit-node patterns for remote access.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installer and privileged networking commands can change software or network state on a real workstation or server.

Mitigation: Prefer official signed package-manager installation steps, review commands before execution, and run sudo commands only on the intended host.

Risk: Broad ACLs, subnet routes, exit nodes, or shared access can unintentionally expose devices or networks.

Mitigation: Scope ACLs, advertised routes, exit nodes, and shared access narrowly, and verify access in the Tailscale admin console.

## Reference(s):

- [Tailscale](https://tailscale.com)
- [Tailscale Login](https://login.tailscale.com)
- [Tailscale for Windows](https://tailscale.com/download/windows)
- [Tailscale Linux Install Script](https://tailscale.com/install.sh)
- [Tailscale ACL Admin](https://login.tailscale.com/admin/acls)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, PowerShell, and JSON code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes privileged networking and installer commands that require local review before execution.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
