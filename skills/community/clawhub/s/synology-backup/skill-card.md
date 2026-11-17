## Description:

Backup and restore OpenClaw workspace, configs, and agent data to a Synology NAS via SMB or SSH/rsync.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and operators use this skill to configure and run Synology NAS backups for OpenClaw workspaces, inspect backup health, verify snapshots, and restore from dated backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The security summary reports that backups can copy secrets to the NAS outside the documented opt-in boundary.

Mitigation: Keep .env and other secrets out of backupPaths unless the NAS share is restricted and encrypted; review restore behavior before restoring configuration files.

Risk: The security summary reports that rsync can follow symlinks out of approved folders.

Mitigation: Remove rsync --copy-links or enforce canonical symlink containment before relying on automated backups.

Risk: Backup data can be exposed if NAS credentials, shares, or network access are too broad.

Mitigation: Use a dedicated low-privilege NAS user, restrict the backup share, avoid public SMB exposure, run a dry run first, and pre-provision SSH host keys when using SSH transport.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/pfrederiksen/skills/synology-backup)
- [Publisher profile](https://clawhub.ai/user/pfrederiksen)
- [OpenClaw](https://openclaw.ai)
- [Tailscale](https://tailscale.com)
- [Tailscale install guide](https://tailscale.com/download)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JSON configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires rsync and jq; SMB transport also requires cifs-utils and a chmod 600 credentials file.]

## Skill Version(s):

2.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
