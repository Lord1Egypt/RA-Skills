## Description:

绿联NAS OpenClaw Docker部署的备份与恢复工具 / Ugreen NAS OpenClaw Docker deployment backup and restore tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zh40](https://clawhub.ai/user/zh40)

### License/Terms of Use:

MIT-0

## Use Case:

External users and operators use this skill to back up and restore Ugreen NAS OpenClaw Docker deployments when the App Center deployment path prevents Docker clone or export workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may expose sensitive OpenClaw configuration, workspace, and skill data.

Mitigation: Store backup archives in a private protected location and consider encrypting them.

Risk: Restoring an archive can overwrite existing OpenClaw configuration and data.

Mitigation: Confirm the selected restore point, stop OpenClaw before restore, and keep a fresh rollback backup.

Risk: Root-level archive extraction without validation can restore untrusted or unexpected archive contents.

Mitigation: Inspect the archive first, validate that all entries stay under .openclaw, and stage extraction in a temporary directory before replacing live data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/zh40/skills/ugreen-nas-openclaw-backup)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup and restore guidance for OpenClaw data using tar archives and user-confirmed backup locations.]

## Skill Version(s):

1.0.4 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
