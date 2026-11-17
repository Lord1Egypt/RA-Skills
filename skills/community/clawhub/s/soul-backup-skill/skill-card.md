## Description:

Backup and restore OpenClaw workspace SOUL files with versioning, validation, and sanitized openclaw.json handling.

This skill is ready for commercial/non-commercial use.

## Publisher:

[x-rayluan](https://clawhub.ai/user/x-rayluan)

### License/Terms of Use:

MIT

## Use Case:

Developers and OpenClaw workspace operators use this skill to create, list, validate, and restore backups of SOUL files and sanitized OpenClaw configuration so agent workspaces can recover from deletion, corruption, or bad configuration changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Backup and restore operations may escape intended paths, overwrite local workspace files, or restore unsafe backup contents.

Mitigation: Use validation and dry-run restore before applying changes, avoid path separators in --name, --timestamp, or --file values, and restore only trusted, unedited backups.

Risk: Backups may contain sensitive workspace information even when openclaw.json is saved as a sanitized copy.

Mitigation: Keep backup directories private, do not commit backups to public repositories, and manually refill redacted secrets only after restoring a trusted sanitized configuration.

Risk: The cron retention example includes a deletion command that security guidance says should not be enabled until fixed.

Mitigation: Do not enable the cron retention example as written; review and constrain any retention or deletion command before scheduling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/x-rayluan/skills/soul-backup-skill)
- [Project homepage](https://github.com/X-RayLuan/soul-backup-skill)
- [README.md](README.md)
- [RUNBOOK.md](RUNBOOK.md)
- [Node.js](https://nodejs.org/)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with shell command examples and configuration guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides local backup, restore, list, validation, and sanitized configuration recovery workflows.]

## Skill Version(s):

1.2.1 (source: server release metadata, package.json, CHANGELOG, released 2026-03-05)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
