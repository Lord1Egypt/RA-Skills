## Description:

Ops-focused Proxmox VE management via REST API for monitoring, controlling, provisioning, and troubleshooting VMs and LXC containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to guide Proxmox VE administration through REST API calls, helper shell commands, provisioning references, and operational safety practices for VMs and LXC containers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can guide powerful Proxmox administration actions, including VM and container power operations, provisioning, resizing, rollback, and deletion.

Mitigation: Require explicit review of VMID, node, storage, backups, and operation intent before destructive or hard-to-reverse actions.

Risk: Proxmox API tokens and the optional credential file can expose infrastructure administration capability.

Mitigation: Use least-privilege tokens, prefer environment injection or a secret manager, keep credential files mode 600, and rotate exposed tokens immediately.

Risk: The helper commands use TLS verification disabled for self-signed Proxmox certificates.

Mitigation: Install a trusted certificate or CA for Proxmox, remove insecure curl flags when possible, and restrict agent network access to approved Proxmox hosts.

## Reference(s):

- [Proxmox Ops ClawHub Page](https://clawhub.ai/eddygk/skills/proxmox-ops)
- [Proxmox Ops Source Homepage](https://github.com/eddygk/proxmox-ops-skill)
- [Proxmox Provisioning Reference](references/provisioning.md)
- [Proxmox VE API Token Documentation](https://pve.proxmox.com/wiki/User_Management#pveum_tokens)
- [Proxmox Certificate Management](https://pve.proxmox.com/wiki/Certificate_Management)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes REST API endpoint patterns, helper script usage, provisioning workflows, and operational cautions.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
