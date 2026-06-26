## Description: <br>
Manage Proxmox VE nodes, VMs, and containers by listing hardware stats and resources, controlling power states, and managing snapshots. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[robnew](https://clawhub.ai/user/robnew) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to monitor Proxmox VE clusters, inspect node and VM/container status, control VM/LXC power states, and manage snapshots through approved actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A broad Proxmox API token could allow cluster-wide infrastructure changes. <br>
Mitigation: Install with a dedicated least-privilege Proxmox API token and prefer VM- or path-specific permissions over cluster-wide '/' access. <br>
Risk: Power actions and snapshot rollback or deletion can interrupt services, discard changes, or remove recovery points. <br>
Mitigation: Keep approval prompts enabled and verify the node, VM/container ID, action, and snapshot name before approving these operations. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/robnew/proxmox-skill) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, JSON, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON command results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires PVE_HOST, PVE_TOKEN_ID, and PVE_TOKEN_SECRET.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
