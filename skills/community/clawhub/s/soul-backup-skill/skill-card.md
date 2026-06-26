## Description: <br>
Backup and restore OpenClaw workspace SOUL files with versioning, validation, and sanitized openclaw.json handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[X-RayLuan](https://clawhub.ai/user/X-RayLuan) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to create, list, validate, and restore local backups of SOUL workspace files before migrations, deployment changes, or recovery from accidental deletion and configuration breakage. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Restores can replace existing SOUL workspace files and change agent behavior. <br>
Mitigation: Run restore with --dry-run first, review the selected backup, and keep or create a fresh pre-restore backup before applying changes. <br>
Risk: Backups can preserve sensitive workspace data from USER.md, TOOLS.md, and related SOUL files. <br>
Mitigation: Keep backup directories private, avoid publishing backup contents, and use restrictive filesystem permissions or encryption where sensitive data is present. <br>
Risk: Automated cron or hook examples create recurring local writes, logs, and backup retention obligations. <br>
Mitigation: Enable automation only where recurring writes and logs are acceptable, and monitor backup storage and pruning. <br>
Risk: openclaw.json backups are sanitized and may omit secrets needed for full recovery. <br>
Mitigation: After restoring openclaw.sanitized.json, manually refill redacted API keys, tokens, and secrets before restarting or validating the workspace. <br>


## Reference(s): <br>
- [SOUL Backup Skill on ClawHub](https://clawhub.ai/X-RayLuan/soul-backup-skill) <br>
- [Project homepage](https://github.com/X-RayLuan/soul-backup-skill) <br>
- [README.md](README.md) <br>
- [RUNBOOK.md](RUNBOOK.md) <br>
- [CHANGELOG.md](CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown guidance with shell commands and JSON backup manifests] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local backup directories, manifest.json metadata, validation summaries, dry-run restore previews, and sanitized openclaw.sanitized.json configuration copies when applicable.] <br>

## Skill Version(s): <br>
1.2.1 (source: package.json, CHANGELOG, release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
