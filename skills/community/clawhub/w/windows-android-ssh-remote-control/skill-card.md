## Description:

Setup and guide for full remote control of a Windows PC from an Android device over the internet via SSH tunneling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jarbcs1-prog](https://clawhub.ai/user/jarbcs1-prog)

### License/Terms of Use:

MIT-0

## Use Case:

External users and technical operators use this skill to configure Android-to-Windows remote desktop access through an SSH tunnel instead of exposing RDP directly to the internet.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote-access setup can expose a Windows PC to internet-facing SSH and credential risks.

Mitigation: Prefer Tailscale or another VPN instead of public port forwarding; use SSH keys, strong account passwords, and avoid saving Windows credentials where they are not needed.

Risk: Incorrect RDP or SSH configuration can prevent connection or weaken access controls.

Mitigation: Review Windows Remote Desktop, OpenSSH Server, firewall, and Android tunnel settings before relying on the connection.

## Reference(s):

- [Windows PC Setup for SSH and RDP](references/windows_setup.md)
- [Android Setup for SSH Tunneling and RDP](references/android_setup.md)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Configuration instructions]

**Output Format:** [Markdown with inline PowerShell commands and configuration steps]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual setup guidance only; the bundled script and template files are placeholders.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
