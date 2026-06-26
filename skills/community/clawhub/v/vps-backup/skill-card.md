## Description: <br>
Automated daily VPS backup using restic for encrypted incremental snapshots of OpenClaw workspace data, SSH keys, project code, and optional session transcripts, with retention policies and optional offsite sync through rclone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codaire](https://clawhub.ai/user/codaire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to configure, run, verify, and restore encrypted restic backups for VPS environments that contain OpenClaw state, project code, SSH keys, and related tooling. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include sensitive SSH keys, OpenClaw memory, session data, chat transcripts, and project code. <br>
Mitigation: Review BACKUP_PATHS and exclusions before scheduling the backup, and install only when this level of VPS backup coverage is intended. <br>
Risk: The restic password file protects access to encrypted backup contents. <br>
Mitigation: Store the password in ~/.backup-password with restrictive permissions and avoid exposing it in logs or shared shell history. <br>
Risk: Downloaded tools or optional session archiver scripts can affect backup behavior if they are replaced upstream. <br>
Mitigation: Verify or pin downloaded tools and scripts where possible before using them in scheduled backups. <br>
Risk: Offsite sync can copy sensitive backups to an unintended storage destination. <br>
Mitigation: Set RCLONE_DEST only to a trusted storage location and verify the configured remote before enabling scheduled sync. <br>


## Reference(s): <br>
- [Skill page](https://clawhub.ai/codaire/vps-backup) <br>
- [restic](https://restic.net) <br>
- [restic install documentation](https://restic.net/install/) <br>
- [rclone downloads](https://downloads.rclone.org/rclone-current-linux-amd64.zip) <br>
- [OpenClaw session archiver](https://github.com/codaire/openclaw-session-archiver) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration instructions, Code, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks and shell script configuration] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces setup, backup, verification, restore, retention, and optional offsite-sync guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
