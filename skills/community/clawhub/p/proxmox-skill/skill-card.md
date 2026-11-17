## Description:

Manage Proxmox VE nodes, VMs, and containers. Can list hardware stats, resources, control power states (start, stop, reboot, shutdown), and manage snapshots (create, list, rollback, delete).

This skill is ready for commercial/non-commercial use.

## Publisher:

[robnew](https://clawhub.ai/user/robnew)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators, developers, and homelab administrators use this skill to inspect Proxmox VE cluster resources, monitor node health, manage VM and container power states, and manage snapshots through a configured API token.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A broadly scoped Proxmox API token could let the agent affect more nodes, VMs, containers, or snapshots than intended.

Mitigation: Use a dedicated Proxmox API token scoped only to the resources and permissions the agent should manage.

Risk: Stop, shutdown, rollback, and snapshot deletion can interrupt services or remove recovery points.

Mitigation: Require human approval for destructive operations and review the target node, resource kind, VMID, and snapshot name before execution.

Risk: Unpinned Python dependencies can change behavior over time.

Mitigation: Pin and audit proxmoxer and requests before installing this skill in stronger-control environments.

## Reference(s):

- [ClawHub Proxmox Management skill page](https://clawhub.ai/robnew/skills/proxmox-skill)

## Skill Output:

**Output Type(s):** [text, json, shell commands, configuration, guidance]

**Output Format:** [JSON command results and concise agent-facing text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Python 3, proxmoxer, requests, PVE_HOST, PVE_TOKEN_ID, and PVE_TOKEN_SECRET.]

## Skill Version(s):

1.0.2 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
