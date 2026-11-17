## Description:

WebDAV backup tool for OpenClaw that creates local and cloud backups and automatically retains the latest 7 local backups and 20 remote backups.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caozeal](https://clawhub.ai/user/caozeal)

### License/Terms of Use:

MIT-0

## Use Case:

OpenClaw users and developers use this skill to create tar.gz backups of an OpenClaw workspace, core configuration, cron files, or a selected source path, then store them locally or upload them to a configured WebDAV server. It also helps list backups, restore local archives, and clean up older local and remote backup files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backups may include unencrypted OpenClaw workspace and configuration data, including stored credentials.

Mitigation: Use a dedicated least-privilege WebDAV account, prefer HTTPS-only endpoints, restrict local backup directory permissions, and encrypt archives before uploading when sensitive data may be included.

Risk: Restore operations and --force can write to local filesystem paths and overwrite existing files.

Mitigation: Restore to a separate test directory first, inspect openclaw/backup-manifest.json, and use --force only after confirming the target path and overwrite intent.

## Reference(s):

- [WebDAV backup configuration guide](references/config.md)
- [ClawHub skill page](https://clawhub.ai/caozeal/skills/webdav-backup)
- [Publisher profile](https://clawhub.ai/user/caozeal)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown and terminal-oriented guidance with inline shell commands and configuration examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create tar.gz backup files locally, upload archives to a configured WebDAV endpoint, list backups, restore archives, and report status or errors.]

## Skill Version(s):

1.3.0 (source: frontmatter, changelog, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
