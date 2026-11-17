## Description:

Backup agent brain (workspace) and body (state) to local folder and optionally sync to cloud via rclone.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vacinc](https://clawhub.ai/user/vacinc)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw users use this skill to create encrypted local backups of agent workspace, state, and skills directories, with optional rclone sync to a configured cloud destination.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive local workspace, state, credentials, and backup destination data.

Mitigation: Confirm exactly which directories and rclone destination will be included before installation or scheduled use.

Risk: The security summary identifies password-handling and temporary-file risks that require manual review.

Mitigation: Use a safer password channel such as a file descriptor or agent, add cleanup traps, and apply restrictive permissions to temporary files.

Risk: The security guidance flags unnecessary or unpinned npm dependencies.

Mitigation: Remove package dependencies that are not needed by npm installation or pin dependencies before release.

Risk: Retention settings affect deletion of local backup files.

Mitigation: Validate retention settings as decimal integers and test pruning behavior on non-critical backup data first.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vacinc/skills/simple-backup)
- [ClawHub publisher profile](https://clawhub.ai/user/vacinc)

## Skill Output:

**Output Type(s):** [Files, Shell commands, Configuration instructions]

**Output Format:** [Encrypted .tgz.gpg backup archives with console status text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires tar, gpg, rclone, and jq; uses configured local paths, retention settings, and optional rclone destination.]

## Skill Version(s):

2.2.0 (source: package.json and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
