## Description:

Ops-focused Proxmox VE management via REST API — monitor, control, provision, and troubleshoot VMs and LXC containers with operational patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[eddygk](https://clawhub.ai/user/eddygk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and infrastructure operators use this skill to monitor and manage Proxmox VE clusters, virtual machines, and LXC containers through the REST API. It provides shell commands and operational guidance for provisioning, snapshots, storage, backups, guest networking, and safe handling of disruptive changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security review is partial and reports potential token exposure, unconfirmed force-stop behavior, extra network activity, and a CLAUDE.md change.

Mitigation: Review the skill and its changes before installation. Use a least-privilege API token, keep credential files mode 600, rotate any exposed token, restrict network access to intended Proxmox hosts, and confirm the target before disruptive operations.

Risk: The helper uses curl with TLS verification disabled, which weakens protection against an intercepted connection.

Mitigation: Use a trusted Proxmox certificate and remove the insecure curl option where possible; otherwise limit connections to the intended Proxmox host and understand the certificate risk.

## Reference(s):

- [Setup and API token guidance](references/setup.md)
- [Common Proxmox API operations](references/api-operations.md)
- [Guest types and inventory coverage](references/guest-types.md)
- [Provisioning reference](references/provisioning.md)
- [Proxmox VE certificate management](https://pve.proxmox.com/wiki/Certificate_Management)
- [Proxmox API token documentation](https://pve.proxmox.com/wiki/User_Management#pveum_tokens)
- [Skill homepage](https://github.com/eddygk/proxmox-ops-skill)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, Configuration]

**Output Format:** [Markdown with inline Bash and curl examples, JSON API responses, and configuration instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Examples use user-supplied Proxmox host, API token, node, and guest identifiers. Requires curl and jq.]

## Skill Version(s):

1.2.1 (source: release evidence and CHANGELOG.md, released 2026-10-10)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
