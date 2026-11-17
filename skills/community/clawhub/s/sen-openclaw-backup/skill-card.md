## Description:

Backup OpenClaw data to desktop - quick backup (without skills, ~100MB) or full backup (with skills, ~500MB+). Supports scheduled automatic backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sen-platotech](https://clawhub.ai/user/sen-platotech)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and operators use this skill to create portable backups of local OpenClaw data and restore that data during migration, recovery, or machine replacement.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A restore archive can overwrite files under the user's OpenClaw home data when extracted.

Mitigation: Restore only backups created by the user from trusted systems, and review the archive contents before extraction when provenance is uncertain.

Risk: Backup archives may contain sensitive OpenClaw data such as chat history, memory, identity data, configuration, and credential files.

Mitigation: Store backups on encrypted, access-controlled media and avoid placing them in shared or untrusted cloud locations.

Risk: The release has no server-resolved source provenance for this version.

Mitigation: Review the packaged files and publisher profile before installation, and do not infer external repository provenance from skill text.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/sen-platotech/skills/sen-openclaw-backup)
- [Publisher profile](https://clawhub.ai/user/sen-platotech)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and backup or restore guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May direct the agent to run local backup and restore scripts that create or extract gzip-compressed tar archives.]

## Skill Version(s):

1.1.2 (source: server release metadata; artifact frontmatter lists 1.1.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
