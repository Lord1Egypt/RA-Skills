## Description:

OpenClaw Smart Backup backs up OpenClaw configuration and workspace directories into a compressed tar.gz archive while skipping large, temporary, downloadable, generated, and symlinked files.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jijinbao-code](https://clawhub.ai/user/jijinbao-code)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preview and create compact backups of local OpenClaw configuration and workspace content, with configurable output location, retention count, and large-file handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local backups may include private workspace or configuration data.

Mitigation: Use dry-run before creating an archive, set an explicit output directory, review the generated file list, and protect generated archives.

Risk: Secret, key, or certificate files may not be excluded in every workspace layout.

Mitigation: Verify the exclusion report and generated file list before relying on the archive, and customize exclusions for local secret patterns.

Risk: Old archives can be deleted automatically when the retention limit is exceeded.

Mitigation: Review the output directory, filename prefix, and max_backups setting before running; set max_backups to 0 when automatic cleanup is not wanted.

Risk: Untrusted custom config or filename prefix values can redirect outputs or alter what gets retained.

Mitigation: Use trusted configuration files and explicit command-line values for output location, source directories, prefix, and retention.

## Reference(s):

- [OpenClaw Smart Backup ClawHub page](https://clawhub.ai/jijinbao-code/skills/smart-backup)
- [openclaw-backup prototype](https://github.com/JIRBOY/openclaw-backup)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, files]

**Output Format:** [Plain text status and report output plus a compressed tar.gz archive.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or update a backup configuration file and delete older matching archives according to the configured retention count.]

## Skill Version(s):

1.0.0 (source: release metadata and skill frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
