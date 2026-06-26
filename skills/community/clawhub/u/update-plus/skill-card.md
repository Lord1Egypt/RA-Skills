## Description: <br>
Full backup, update, and restore for OpenClaw config, workspace, and skills with auto-rollback. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hopyky](https://clawhub.ai/user/hopyky) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to manage backups, check for updates, update installed skills, restore local environments, and configure optional unattended maintenance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can change installed agent code and may run unattended updates. <br>
Mitigation: Use check or dry-run before updates, review changes before applying them, and enable cron only when unattended updates are acceptable. <br>
Risk: Restore operations can overwrite or delete local files. <br>
Mitigation: Review restore targets carefully and keep known-good backups before restoring config, workspace, or skills. <br>
Risk: Backups and cloud sync can expose sensitive local environment data. <br>
Mitigation: Encrypt backups before enabling cloud sync and verify the configured remote storage destination. <br>
Risk: Untrusted configuration can direct backups, restores, or updates to unsafe paths. <br>
Mitigation: Use only trusted update-plus.json files and review configured backup paths, skill directories, excludes, and notification targets. <br>
Risk: The packaged artifact may be missing the advertised executable entrypoint. <br>
Mitigation: Verify the installed package contains the expected update-plus command before relying on automated backup or update workflows. <br>


## Reference(s): <br>
- [ClawHub listing](https://clawhub.ai/hopyky/update-plus) <br>
- [README](README.md) <br>
- [Skill definition](SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires git, jq, and rsync; optional features may require gpg, rclone, cron, or notification tooling.] <br>

## Skill Version(s): <br>
4.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
