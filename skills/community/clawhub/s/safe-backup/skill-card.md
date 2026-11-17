## Description:

Backup OpenClaw state directory and workspace. Includes excluding sensitive files, packaging for backup. Triggered when user asks to backup, export, or save state.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hacksing](https://clawhub.ai/user/hacksing)

### License/Terms of Use:


## Use Case:

Developers and OpenClaw operators use this skill to create portable backups of OpenClaw state and workspace files for routine backup, migration, or disaster recovery workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups can contain sensitive OpenClaw state or workspace data even with documented exclusions.

Mitigation: Inspect archive contents before storing or transferring them, encrypt retained backups, and avoid committing raw backup archives to git.

Risk: Temporary backup files may remain exposed in local temp directories until removed.

Mitigation: Delete unencrypted temporary archives after use or harden the script's temporary-file handling before routine operation.

Risk: Remote storage examples can persist or expose sensitive content if used without additional controls.

Mitigation: Use local encrypted storage by default and expand exclusions plus encryption before any remote rsync or cloud workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/hacksing/skills/safe-backup)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline bash commands and backup workflow guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run a local backup script that produces a compressed tar archive.]

## Skill Version(s):

1.0.5 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
