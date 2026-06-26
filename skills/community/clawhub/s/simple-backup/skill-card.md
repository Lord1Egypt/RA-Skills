## Description: <br>
Backs up agent workspace, state, and skill directories to encrypted local archives and can optionally sync them to cloud storage with rclone. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[VACInc](https://clawhub.ai/user/VACInc) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create encrypted backups of agent workspaces, OpenClaw state, and installed skills. It supports local retention and optional rclone synchronization for teams that need recoverable agent state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill backs up broad OpenClaw workspace, state, and skills data that may contain sensitive information. <br>
Mitigation: Use a dedicated backup folder, protect encrypted archives, and keep the backup password out of shared configuration where possible. <br>
Risk: Retention cleanup deletes older daily and hourly backup archives automatically. <br>
Mitigation: Review and configure maxDays and hourlyRetentionHours before relying on the backup set for recovery. <br>
Risk: Optional cloud synchronization can copy encrypted backups to an external rclone destination. <br>
Mitigation: Confirm the rclone remote and destination before enabling remoteDest. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/VACInc/simple-backup) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, files] <br>
**Output Format:** [Plain text command output, configuration values, and encrypted .tgz.gpg backup archives] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires tar, gpg, rclone, jq, and rsync; cloud sync is optional and depends on configured rclone remotes.] <br>

## Skill Version(s): <br>
2.2.0 (source: evidence release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
