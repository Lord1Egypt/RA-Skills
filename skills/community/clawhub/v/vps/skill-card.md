## Description:

Guides agents through VPS selection, provisioning, access recovery, backups, resizing, networking, incidents, migrations, cost review, and safe teardown for rented virtual private servers.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, operators, and technical users use this skill to plan and operate rented virtual private servers, including provider choice, first boot, access recovery, security posture, backups, resizing, migrations, incidents, and cost control.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may maintain local infrastructure records under ~/Clawic/data, including shared server, domain, and finance inventories.

Mitigation: Review proposed file writes before accepting them, especially changes to shared inventories and spend records.

Risk: Real VPS operations can be destructive or irreversible, including rebuilds, destroys, disk growth, address release, and snapshot deletion.

Mitigation: Require explicit confirmation, a stated blast radius, and a fallback path before executing those actions.

Risk: Raw secrets such as private keys, provider API tokens, root passwords, and backup passphrases could be exposed if pasted or saved directly.

Mitigation: Store only secret pointers such as keychain, password-manager, environment-variable, or file references.

Risk: Provider-account compromise can affect servers and provider-held snapshots.

Mitigation: Use provider-account 2FA, scoped and rotated API tokens, offline recovery codes, and backups restorable outside the provider account.

## Reference(s):

- [ClawHub VPS Skill Page](https://clawhub.ai/ivangdavila/skills/vps)
- [Clawic VPS Skill Page](https://clawic.com/skills/vps)
- [VPS Skill Definition](artifact/SKILL.md)
- [Access and Recovery Guidance](artifact/access.md)
- [Backups and Restore Guidance](artifact/backups.md)
- [Firewall Guidance](artifact/firewall.md)
- [Security and Abuse Response Guidance](artifact/security.md)
- [Provisioning Guidance](artifact/provisioning.md)
- [Migration and Teardown Guidance](artifact/migration.md)
- [Operations Guidance](artifact/operations.md)
- [Cost Guidance](artifact/costs.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with command snippets, configuration paths, and runbook or inventory update instructions.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose local Clawic data file updates and requires explicit confirmation before destructive or irreversible infrastructure actions.]

## Skill Version(s):

1.0.2 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
