## Description: <br>
Synchronize files and directories between local, remote, and cloud storage reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to plan reliable one-way or cloud file synchronization with rsync and rclone, including exclusions, dry runs, verification, remote transfers, and bidirectional-sync caveats. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sync commands can overwrite or delete destination files when mirroring a source, especially with --delete or rclone sync. <br>
Mitigation: Confirm source and destination paths and run a dry run before executing destructive syncs. <br>
Risk: Remote or cloud sync can target the wrong location or expose credentials if configuration is hardcoded or misselected. <br>
Mitigation: Use interactive rclone configuration or SSH key-based authentication, avoid hardcoding credentials, and verify the selected remote before transfer. <br>
Risk: Critical syncs can silently diverge because of clock skew, mounted-drive issues, or incomplete transfers. <br>
Mitigation: Verify mounts first and use checksum validation such as rsync -avzc or rclone check after important syncs. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/sync) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires rsync or rclone for the suggested sync workflows; the skill itself provides guidance rather than generating files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
