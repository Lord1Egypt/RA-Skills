## Description:

Backup and restore OpenClaw agent configuration, skills, memory, and workspace files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liuyue8135](https://clawhub.ai/user/liuyue8135)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to create local restore points for agent configuration, credentials, skills, memory, and workspace files, and to restore those files on the same or a new machine.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup archives can contain sensitive OpenClaw secrets, credentials, identity files, and memory in an unencrypted archive.

Mitigation: Encrypt backup archives, restrict file permissions, and avoid shared or synced storage unless it is protected.

Risk: Restoring an archive can overwrite OpenClaw files and should be treated as a privileged recovery operation.

Mitigation: Restore only archives the user created and trusts, inspect contents before restore when practical, and keep the pre-restore backup until the recovered agent is verified.

Risk: Automatic backups can retain or move sensitive data without a clear retention and secrets-handling plan.

Mitigation: Do not enable scheduled backups until retention, deletion, storage location, and secret protection are defined.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/liuyue8135/skills/yuebao-self-backup)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown-style operational guidance with shell commands; running the bundled scripts creates tar.gz backup archives and JSON manifests.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Backup archives may contain OpenClaw credentials, identity files, memory, skills, cron jobs, and selected workspace files.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
