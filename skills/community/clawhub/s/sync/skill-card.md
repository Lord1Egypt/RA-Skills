## Description:

Synchronize files and directories between local, remote, and cloud storage reliably.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers, engineers, and operators use this skill to choose safer synchronization commands and practices for local, remote, and cloud file transfers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Synchronization commands can overwrite or delete destination files when misused.

Mitigation: Review commands before execution, run dry runs first, and use destructive options such as --delete and rclone sync only when the destination should mirror the source.

Risk: Remote or cloud syncs can expose data if credentials or remotes are configured incorrectly.

Mitigation: Configure remotes interactively, avoid hardcoding credentials, and verify source and destination paths before transferring data.

## Reference(s):


## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires either rsync or rclone; supports Linux, macOS, and Windows according to ClawHub metadata.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
