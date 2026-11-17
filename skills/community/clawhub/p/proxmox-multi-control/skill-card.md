## Description:

Manage one or many Proxmox VE servers via REST API, including host overview, VM and container state, snapshots, backups, storage, and tasks across configured Proxmox hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[maikimolto](https://clawhub.ai/user/maikimolto)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and homelab administrators use this skill to let an agent inspect and manage one or more Proxmox VE hosts. It supports read-only inventory and health checks plus approval-gated VM, container, and snapshot operations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use Proxmox API credentials to control VM/container power states and snapshots.

Mitigation: Use a dedicated least-privilege Proxmox user or token for each host and manually confirm the host, node, VM/container ID, and snapshot before stop, delete_snapshot, or rollback operations.

Risk: The documented examples default to verify_ssl false for self-signed certificates.

Mitigation: Enable TLS verification or configure a trusted CA wherever possible before allowing the agent to connect to Proxmox hosts.

Risk: Credentials may be stored in ~/.openclaw/credentials/proxmox.json.

Mitigation: Keep the credentials file tightly permissioned, such as chmod 600, and avoid broad or shared Proxmox tokens.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/maikimolto/skills/proxmox-multi-control)
- [Publisher profile](https://clawhub.ai/user/maikimolto)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance, JSON]

**Output Format:** [Markdown guidance with shell commands and JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Commands return JSON objects with ok/data or ok/error fields; multi-host results include _host labels.]

## Skill Version(s):

1.6.0 (source: server release evidence; artifact frontmatter and _meta.json list 1.5.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
