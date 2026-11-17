## Description:

Automates encrypted, incremental daily VPS backups with restic for OpenClaw workspace data, SSH keys, project code, session transcripts, retention policies, restore workflows, and optional offsite sync through rclone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[codaire](https://clawhub.ai/user/codaire)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to configure, run, verify, and restore encrypted restic backups for OpenClaw VPS environments, including optional offsite synchronization with rclone.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The default backup paths include SSH keys, agent state, transcripts, and source code.

Mitigation: Review and reduce BACKUP_PATHS before scheduling; remove ~/.ssh unless private-key recovery is explicitly required.

Risk: The setup flow downloads restic, rclone, and an optional session exporter from network locations.

Mitigation: Pin versions and verify checksums or signatures before installing or scheduling downloaded code.

Risk: Offsite rclone destinations may receive highly sensitive encrypted backups.

Mitigation: Use strong restic credentials, protect rclone remotes, and treat the remote bucket or drive as sensitive infrastructure.

## Reference(s):

- [VPS Backup ClawHub Page](https://clawhub.ai/codaire/skills/vps-backup)
- [restic](https://restic.net)
- [restic install documentation](https://restic.net/install/)
- [restic Linux AMD64 release download](https://github.com/restic/restic/releases/latest/download/restic_linux_amd64.tar.gz)
- [rclone Linux AMD64 download](https://downloads.rclone.org/rclone-current-linux-amd64.zip)
- [OpenClaw session archiver](https://github.com/codaire/openclaw-session-archiver)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash code blocks and shell script artifacts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces backup setup, scheduling, verification, restore, retention, and offsite sync guidance for an agent.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
