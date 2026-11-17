## Description:

Restic-powered encrypted time machine for OpenClaw: hourly incremental snapshots, fast restore by time/snapshot/file, local-only privacy defaults, integrity checks, retention, and optional alerts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[marzliak](https://clawhub.ai/user/marzliak)

### License/Terms of Use:

MIT

## Use Case:

Developers and operators use this skill to add local encrypted backup, status, retention, and restore workflows for OpenClaw memory, sessions, configuration, and selected workspace paths.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Privileged scheduler setup can expose a root cron injection risk.

Mitigation: Review and fix cron fallback behavior before default installation, or use systemd-compatible schedules with trusted, root-controlled configuration.

Risk: Backup and restore operations may read sensitive OpenClaw state or overwrite live files.

Mitigation: Run setup.sh --dry-run first, protect configured backup paths and the restic password file, and restore to a temporary target before overwriting current OpenClaw state.

Risk: Optional alerts and update checks may create external network egress.

Mitigation: Keep privacy.local_only true unless external Telegram, healthcheck, or ClawHub update checks are intentionally configured.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/marzliak/skills/quick-backup-restore)
- [Project homepage](https://github.com/marzliak/quick-backup-restore)
- [Security policy](SECURITY.md)
- [Privacy notes](PRIVACY.md)
- [Setup guide](SETUP_GUIDE.md)

## Skill Output:

**Output Type(s):** [text, guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration edits]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose privileged local commands, dry-run checks, backup/restore targets, retention settings, and optional alert configuration.]

## Skill Version(s):

3.2.3 (source: skill.json and changelog, released 2026-06-01)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
