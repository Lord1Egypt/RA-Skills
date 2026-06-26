## Description: <br>
Backs up an OpenClaw workspace and related configuration to a local tar.gz archive, a WebDAV server, or both. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[caozeal](https://clawhub.ai/user/caozeal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and agents use this skill to create local or WebDAV backups of workspace files, base configuration, cron configuration, and selected custom sources. It also guides safer restore workflows by recommending manifest review before placing files back into target locations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Backups may include private OpenClaw prompts, workspace files, schedules, and credentials stored in openclaw.json. <br>
Mitigation: Use --source or --local-only when a narrower backup is sufficient, keep configuration file permissions tight, review backup-manifest.json before restore, and consider encrypting archives before remote upload. <br>
Risk: Remote WebDAV uploads place backup archives on a third-party destination and depend on endpoint trust. <br>
Mitigation: Use a trusted HTTPS WebDAV endpoint, prefer app-specific WebDAV passwords, and verify the destination before uploading. <br>
Risk: Restore operations can overwrite existing files when --force is used. <br>
Mitigation: Restore first into an independent directory, inspect the manifest and contents, then copy back only the needed files or use --force only after confirming the target path and overwrite intent. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/caozeal/webdav-backup) <br>
- [WebDAV backup configuration guide](references/config.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with bash commands; backup operations create tar.gz archives and a JSON backup manifest.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Remote backup requires WEBDAV_URL, WEBDAV_USERNAME, and WEBDAV_PASSWORD; local-only backup can run without WebDAV credentials.] <br>

## Skill Version(s): <br>
1.2.2 (source: server release metadata, SKILL.md frontmatter, CHANGELOG) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
