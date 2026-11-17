## Description:

Manage Proxmox VE clusters via REST API, including listing, starting, stopping, restarting, snapshotting, viewing tasks, and checking node or storage status for VMs and LXC containers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pratiknarola](https://clawhub.ai/user/pratiknarola)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, platform engineers, and infrastructure operators use this skill to manage Proxmox VE clusters through authenticated REST API calls and a helper shell script.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can perform authenticated administrative actions that change infrastructure state.

Mitigation: Require explicit confirmation before stop, reboot, rollback, delete, backup, or similar state-changing actions.

Risk: The skill handles Proxmox API tokens and supports a sourced credentials file.

Mitigation: Use a narrowly scoped, revocable API token and prefer environment-based secret handling over a persistent credentials file.

Risk: The documented curl commands and helper script use -k or -ks, which skip TLS certificate verification.

Mitigation: Use verified TLS certificates and avoid the default -k/-ks behavior on untrusted networks.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash and curl commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Proxmox API credentials and access to a reachable Proxmox VE API endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
