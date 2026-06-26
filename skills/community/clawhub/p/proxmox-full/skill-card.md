## Description: <br>
Provides Proxmox VE management guidance for creating, cloning, starting, stopping, snapshotting, backing up, and managing VMs, LXC containers, storage, and templates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mSarheed](https://clawhub.ai/user/mSarheed) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and infrastructure administrators use this skill to ask an agent for Proxmox VE REST API commands and setup guidance for VM, container, storage, snapshot, backup, and task operations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide broad Proxmox infrastructure actions through an API token. <br>
Mitigation: Use a dedicated least-privilege token scoped to only the required nodes, pools, or VMs, and keep privilege separation enabled where possible. <br>
Risk: The documented operations include destructive or disruptive actions such as stop, rollback, delete, purge, restore, clone, and template conversion. <br>
Mitigation: Require explicit human confirmation before executing disruptive commands and verify node names, VMIDs, storage targets, and backup archives. <br>
Risk: Example curl commands use certificate bypass for self-signed Proxmox endpoints. <br>
Mitigation: Trust the Proxmox certificate in the execution environment and avoid using -k once TLS validation is configured. <br>


## Reference(s): <br>
- [Proxmox](https://www.proxmox.com/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and Proxmox API endpoint examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, PVE_URL, and PVE_TOKEN; commands should be reviewed before execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
