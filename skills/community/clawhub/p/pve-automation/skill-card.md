## Description: <br>
Automate Proxmox VE virtual machine and container management tasks, including VM lifecycle operations, template management, cloud-init configuration, plugin installation, and cluster operations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Lichas](https://clawhub.ai/user/Lichas) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to manage Proxmox VE VMs, LXC containers, storage, snapshots, and cluster tasks through API guidance and a Python CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide or execute broad infrastructure administration actions, including delete, rollback, ACL, firewall, certificate, storage, and host-maintenance operations. <br>
Mitigation: Use least-privilege Proxmox API tokens and require explicit target confirmation before destructive or privileged actions. <br>
Risk: The bundled Python client disables TLS certificate verification by default, which can expose privileged API tokens on untrusted networks. <br>
Mitigation: Use valid certificates and enable TLS verification before real use. <br>
Risk: Over-privileged root automation tokens increase blast radius if credentials are leaked or commands target the wrong resource. <br>
Mitigation: Avoid root@pam automation tokens, scope token permissions to the required nodes and operations, and store credentials outside shared logs or committed files. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Lichas/pve-automation) <br>
- [Proxmox VE API Documentation](https://pve.proxmox.com/wiki/Proxmox_VE_API) <br>
- [Proxmox VE API Explorer](https://pve.proxmox.com/pve-docs/api-viewer/) <br>
- [pvesh Manual](https://pve.proxmox.com/pve-docs/pvesh.1.html) <br>
- [Proxmox VE High Availability](https://pve.proxmox.com/wiki/High_Availability) <br>
- [Proxmox VE PCI Passthrough](https://pve.proxmox.com/wiki/PCI_Passthrough) <br>
- [Proxmox VE Backup and Restore](https://pve.proxmox.com/wiki/Backup_and_Restore) <br>
- [Proxmox VE Firewall](https://pve.proxmox.com/wiki/Firewall) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell, Python, and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce or adapt Proxmox API calls and CLI commands that require user-supplied Proxmox credentials and target details.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
