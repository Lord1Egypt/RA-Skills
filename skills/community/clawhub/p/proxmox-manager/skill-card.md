## Description: <br>
Manage Proxmox VE clusters via REST API for listing, starting, stopping, restarting, snapshotting, and checking VMs, LXC containers, nodes, tasks, storage, and backups. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pratiknarola](https://clawhub.ai/user/pratiknarola) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to manage Proxmox VE clusters through API-token-authenticated REST calls and a helper shell script. It supports routine inspection and administrative actions for VMs, LXC containers, snapshots, tasks, storage, and backups. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can perform disruptive infrastructure actions when used with powerful Proxmox API credentials. <br>
Mitigation: Use a least-privilege Proxmox API token and require explicit user approval before stop, reboot, rollback, delete, or backup operations in production. <br>
Risk: Credential exposure could allow unauthorized access to Proxmox infrastructure. <br>
Mitigation: Store API tokens carefully, restrict file permissions on local credential files, and avoid sharing token values in prompts, logs, or generated output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/pratiknarola/proxmox-manager) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and helper script usage] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses Proxmox API token environment variables or a local credentials file.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
