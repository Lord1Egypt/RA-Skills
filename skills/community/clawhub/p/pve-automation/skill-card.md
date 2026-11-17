## Description:

Automate Proxmox VE (PVE) virtual machine and container management tasks including VM lifecycle operations, template management, cloud-init configuration, plugin installation, and cluster operations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lichas](https://clawhub.ai/user/lichas)

### License/Terms of Use:


## Use Case:

Developers and infrastructure engineers use this skill to manage Proxmox VE clusters, virtual machines, LXC containers, templates, cloud-init settings, storage, snapshots, and cluster operations through API-backed workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill assists with privileged Proxmox administration and handles infrastructure credentials.

Mitigation: Use a least-privilege non-root API token and avoid passing secrets on the command line.

Risk: The security evidence flags unsafe TLS defaults for the Proxmox client.

Mitigation: Enable proper TLS certificate verification before real use.

Risk: Documented workflows include disruptive actions such as deletes, rollbacks, storage or IAM changes, upgrades, and other administrative operations.

Mitigation: Require explicit human confirmation, pre-flight checks, and dry-run review before executing disruptive operations.

## Reference(s):

- [Proxmox VE API Documentation](https://pve.proxmox.com/wiki/Proxmox_VE_API)
- [Proxmox VE API Explorer](https://pve.proxmox.com/pve-docs/api-viewer/)
- [pvesh Manual Page](https://pve.proxmox.com/pve-docs/pvesh.1.html)
- [Proxmox VE High Availability](https://pve.proxmox.com/wiki/High_Availability)
- [Proxmox VE PCI Passthrough](https://pve.proxmox.com/wiki/PCI_Passthrough)
- [Proxmox VE Backup and Restore](https://pve.proxmox.com/wiki/Backup_and_Restore)
- [Proxmox VE Firewall](https://pve.proxmox.com/wiki/Firewall)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with Python and bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Proxmox API operations and JSON-shaped responses; privileged actions should be reviewed before execution.]

## Skill Version(s):

0.1.0 (source: release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
