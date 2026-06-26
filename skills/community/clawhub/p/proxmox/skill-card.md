## Description: <br>
Manage Proxmox VE clusters via REST API. Use when user asks to list, start, stop, restart VMs or LXC containers, check node status, create snapshots, view tasks, or manage Proxmox infrastructure. Requires API token or credentials configured. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weird-aftertaste](https://clawhub.ai/user/weird-aftertaste) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to inspect and operate Proxmox VE clusters, including VM and LXC status, lifecycle actions, snapshots, tasks, storage, and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Powerful Proxmox credentials can permit disruptive infrastructure actions such as stop, reboot, rollback, delete, or backup operations. <br>
Mitigation: Use a dedicated least-privilege API token and require explicit user confirmation before disruptive operations. <br>
Risk: Credentials stored in ~/.proxmox-credentials can expose cluster access if the file is not protected. <br>
Mitigation: Protect the credentials file with restrictive permissions and avoid sharing token secrets. <br>
Risk: The examples use curl -k, which skips TLS certificate verification for self-signed certificates. <br>
Mitigation: Prefer valid TLS certificates and avoid curl -k where possible. <br>


## Reference(s): <br>
- [ClawHub Proxmox skill page](https://clawhub.ai/weird-aftertaste/proxmox) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user-supplied Proxmox API credentials and target resource identifiers.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
