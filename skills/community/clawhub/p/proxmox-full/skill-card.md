## Description:

Complete Proxmox VE management - create/clone/start/stop VMs and LXC containers, manage snapshots, backups, storage, and templates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[msarheed](https://clawhub.ai/user/msarheed)

### License/Terms of Use:


## Use Case:

Developers and infrastructure operators use this skill to generate Proxmox VE REST API commands for managing clusters, nodes, virtual machines, LXC containers, snapshots, backups, storage, templates, tasks, and destructive lifecycle operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill provides commands that can stop, roll back, restore, delete, or purge Proxmox resources.

Mitigation: Require explicit human confirmation and verify node, VMID, storage, snapshot, and backup identifiers before executing destructive or disruptive operations.

Risk: The examples use broad Proxmox API access and a token environment variable.

Mitigation: Use a dedicated, least-privilege Proxmox token scoped only to the nodes and actions needed, and keep the token out of logs and shared shell history.

Risk: The artifact demonstrates curl with TLS verification disabled and an example root password for LXC creation.

Mitigation: Keep TLS verification enabled with a trusted CA, and replace password-based container setup with SSH keys or generated secrets.

## Reference(s):

- [Proxmox homepage](https://www.proxmox.com/)
- [ClawHub skill page](https://clawhub.ai/msarheed/skills/proxmox-full)
- [Publisher profile](https://clawhub.ai/user/msarheed)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and Proxmox API examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires curl, jq, PVE_URL, and a PVE_TOKEN for the target Proxmox VE environment.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
