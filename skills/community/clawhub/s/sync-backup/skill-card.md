## Description: <br>
Synchronize files and directories between local, remote, and cloud storage reliably. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[macdesire](https://clawhub.ai/user/macdesire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and technical users use this skill to plan safer file synchronization across local paths, SSH destinations, mounted drives, and cloud storage remotes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Mirror or delete operations can remove destination files when rsync --delete or rclone sync is used unintentionally. <br>
Mitigation: Verify source and destination paths, run dry runs before destructive operations, and use copy-style commands when exact mirroring is not intended. <br>
Risk: Remote synchronization can expose SSH keys or rclone credentials if they are hardcoded or mishandled. <br>
Mitigation: Use interactive rclone configuration, avoid embedding credentials in scripts, and protect SSH and cloud storage secrets. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/macdesire/sync-backup) <br>
- [Publisher profile](https://clawhub.ai/user/macdesire) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes dry-run, exclusion, verification, credential-handling, and delete/mirror cautions for rsync, rclone, and related sync tools.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
