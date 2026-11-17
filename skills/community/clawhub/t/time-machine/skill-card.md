## Description:

TimeMachine creates, lists, cleans up, and restores incremental snapshots of OpenClaw configuration, credentials, workspace, and memory files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chaceli](https://clawhub.ai/user/chaceli)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to create restore points before configuration changes, inspect available snapshots, roll back state, and manage snapshot retention.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Snapshots may persist copies of OpenClaw credentials, .env files, configuration, skills, and workspace data without the encryption claimed by the skill text.

Mitigation: Treat snapshots as sensitive local secret material, restrict filesystem access, and avoid syncing or sharing the snapshot directory.

Risk: Restoring from a snapshot can overwrite OpenClaw configuration, workspace, and memory state, especially if the snapshot location was modified by another process or person.

Mitigation: Review rollback previews, restore only the needed file or category where possible, and restore only from snapshot locations you control.

## Reference(s):

- [TimeMachine ClawHub release](https://clawhub.ai/chaceli/skills/time-machine)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell commands, JSON configuration examples, and text status output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates and restores local snapshot files under the OpenClaw snapshot directory.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
