## Description: <br>
Backs up OpenClaw workspace data and configuration to local tar.gz archives and, when configured, to a WebDAV endpoint with automatic local and remote retention cleanup. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caozeal](https://clawhub.ai/user/caozeal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and developers use this skill to create local and WebDAV backups of workspace files, configuration, cron data, and related settings, then list or restore those backups when needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backup archives may include OpenClaw workspace data, configuration, cron files, and sensitive values in openclaw.json before upload to WebDAV. <br>
Mitigation: Review the backup scope and openclaw.json before uploading; use a dedicated WebDAV folder and an application password. <br>
Risk: Old backups are automatically pruned, which can remove recovery points that a user expected to keep. <br>
Mitigation: Confirm the documented retention policy before relying on this skill for long-term archival backups. <br>
Risk: Restoring an untrusted or unchecked archive can place unwanted files into the target directory, and forced restores can overwrite existing files. <br>
Mitigation: Restore only trusted archives, extract to an isolated directory first, inspect backup-manifest.json, and use --force only after confirming the target path and overwrite intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caozeal/skills/webdav-backup) <br>
- [README](README.md) <br>
- [WebDAV backup configuration guide](references/config.md) <br>
- [Changelog](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance, shell commands, tar.gz backup archives, and JSON backup manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup archives by default and can upload to a user-configured WebDAV endpoint when credentials are provided.] <br>

## Skill Version(s): <br>
1.3.0 (source: frontmatter, changelog, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
