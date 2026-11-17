## Description:

Fast backup and restore tool for OpenClaw workspace markdown files that preserves directory structure.

This skill is ready for commercial/non-commercial use.

## Publisher:

[roryyu](https://clawhub.ai/user/roryyu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to generate shell scripts and guidance for backing up markdown workspace content, migrating notes or skills between workspaces, and restoring selected archives.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Restore behavior can overwrite files in an unexpected location despite displaying a target directory.

Mitigation: Fix or avoid the restore script until extraction is constrained to the intended target directory and silent overwrites are prevented.

Risk: Workspace backup archives can contain sensitive notes, skill documentation, or memory files.

Mitigation: Treat backup archives as sensitive files, store them securely, and restore only from trusted archives.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/roryyu/skills/workspace-zip-backup)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with inline bash code blocks and command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces copyable backup and restore shell-script patterns for markdown-only workspace archives.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
