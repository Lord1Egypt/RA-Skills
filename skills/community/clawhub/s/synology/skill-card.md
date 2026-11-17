## Description:

Plan, harden, and recover Synology NAS and DSM setups with storage design, backup discipline, remote access, and Container Manager workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and administrators use this skill to plan and triage Synology DSM and NAS work involving storage layout, backups, remote access, package health, Container Manager, upgrades, migrations, and incident recovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synology NAS administration can affect sensitive storage, backups, permissions, packages, restore paths, and internet exposure.

Mitigation: Start with read-only inventory, confirm backups and rollback paths, and require explicit confirmation before destructive, mutating, restore, migration, package removal, or exposure-changing actions.

Risk: Optional continuity notes under ~/synology/ could retain sensitive operational context if used carelessly.

Mitigation: Use local memory only with user approval and do not store passwords, OTP codes, private keys, serial numbers, copied support bundles, or other secrets.

Risk: Synology account, QuickConnect, and documentation lookups may send request, session, or connection metadata to Synology-owned services.

Mitigation: Use external Synology services only for approved documentation, account, package, or remote-access tasks, and get explicit approval before involving third-party backup, VPN, DNS, or monitoring services.

## Reference(s):

- [ClawHub skill release page](https://clawhub.ai/ivangdavila/skills/synology)
- [Synology official site](https://www.synology.com)
- [Synology Knowledge Center](https://kb.synology.com)
- [Synology Account](https://account.synology.com)
- [Synology QuickConnect](https://quickconnect.to)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, checklists, and concise execution records]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local notes under ~/synology/ when the user wants continuity; requires explicit confirmation before destructive, restore, permission, package removal, migration, or internet-exposure changes.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
