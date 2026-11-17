## Description:

Synchronize files and directories between local, remote, and cloud storage reliably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[macdesire](https://clawhub.ai/user/macdesire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to plan and review file synchronization workflows across local disks, SSH remotes, and cloud storage with dry-run, exclusion, verification, and logging practices.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Mirror or delete-style synchronization can remove destination files or create an unexpected directory layout when paths are wrong.

Mitigation: Confirm source and destination paths, pay attention to trailing slashes, and run dry-run checks before using destructive sync options.

Risk: Cloud remotes and SSH-based backups can expose credentials if secrets are embedded in reusable commands or scripts.

Mitigation: Configure credentials outside reusable scripts and use established tools such as rclone config or SSH key management.

Risk: Syncing to an unavailable mounted drive can write into a local folder instead of the intended mount point.

Mitigation: Verify that the destination mount is available before running the sync.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/macdesire/skills/sync-backup)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either rsync or rclone; supports Linux, macOS, and Windows per release metadata.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
