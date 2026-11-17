## Description:

Installs and enrolls the Wazuh agent inside Windows VMs hosted on Proxmox VE through QEMU guest agent execution, without requiring WinRM, SSH, RDP, GPO, or AD credentials.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT

## Use Case:

Developers and infrastructure operators use this skill to enroll Windows Proxmox guests into a Wazuh manager through QEMU guest agent commands, including group preparation, silent MSI installation, service restart, and manager-side verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Guest execution runs with very high Windows privileges and can install software on live servers.

Mitigation: Limit use to trusted operators, require explicit confirmation of the target VM and change window, and verify the manager address, agent group, and intended action before running guest commands.

Risk: Installer and Proxmox API-token handling can become unsafe if TLS verification is disabled or installer integrity is not checked.

Mitigation: Do not use curl -k with Proxmox API tokens, and pin and verify the Wazuh MSI hash and publisher signature before installation.

Risk: The Wazuh registration password could be exposed through command lines, logs, or chat.

Mitigation: Pass the registration password through QGA stdin or a short-lived in-guest file that is deleted immediately, and keep the value out of logs and chat.

## Reference(s):

- [QGA execution - running the install in a Windows guest](references/qga-exec.md)
- [Wazuh agent enrollment on a Windows Proxmox VM (via QGA)](references/wazuh-agent-enroll.md)
- [Project homepage](https://github.com/eddygk/proxmox-wazuh-enroll)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell, PowerShell, batch, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces operational guidance for state-changing Wazuh enrollment through Proxmox QEMU guest agent execution.]

## Skill Version(s):

1.0.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
