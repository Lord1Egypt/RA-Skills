## Description:

File Writer helps an agent write or append text files in a scratch directory, create backups before overwrites, and reject unsafe paths or non-text content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[nagilem](https://clawhub.ai/user/nagilem)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent users use this skill to save notes, logs, JSON, Markdown, and other text artifacts in a scratch workspace while applying path checks, confirmations, and backups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Shell fallbacks and backup behavior could affect files outside the intended scratch boundary.

Mitigation: Use structured filesystem APIs, enforce canonical scratch-root containment, reject symlink traversal, and constrain backup operations to validated relative paths before deployment.

Risk: File write instructions can overwrite existing scratch files or capture sensitive content if confirmations are skipped.

Mitigation: Require explicit confirmation for overwrites or sensitive filenames, keep backups enabled, and reject content or paths that do not meet the documented text-file policy.

## Reference(s):

- [Safety Reference](references/safety.md)

## Skill Output:

**Output Type(s):** [Files, Text, Markdown, Code, Shell commands, Guidance]

**Output Format:** [Text files and Markdown guidance with shell command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes are intended to stay within the configured scratch directory, with backups before overwrites and confirmation for existing files.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
