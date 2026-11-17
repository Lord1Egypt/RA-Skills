## Description:

Reads server hardware, Proxmox/Linux OS information, temperatures, SMART status, ECC errors, RAID, disks, network status, services, and logs without making changes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[polumish](https://clawhub.ai/user/polumish)

### License/Terms of Use:

MIT-0

## Use Case:

Infrastructure operators and system administrators use this skill to ask an agent for read-only diagnostic command sets and audit summaries for Proxmox VE and Linux servers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill asks agents to run server diagnostics over SSH as root, which can expose sensitive host, storage, network, and log data.

Mitigation: Use a dedicated audit account or constrained sudo rules where possible, limit target hosts, and review command blocks before execution.

Risk: Audit output and optional saved reports may contain infrastructure details such as serial numbers, IP addresses, login history, service state, and disk health.

Mitigation: Confirm report destination, permissions, sanitization needs, and retention policy before saving or sharing results.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/polumish/skills/server-audit)
- [Linux Server Audit](artifact/references/linux-audit.md)
- [Proxmox Server Audit](artifact/references/proxmox-audit.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with SSH and bash command blocks plus audit-summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include sensitive infrastructure diagnostics and optional report-writing instructions.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
