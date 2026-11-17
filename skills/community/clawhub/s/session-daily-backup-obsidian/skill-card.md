## Description:

Backs up OpenClaw session conversations to an Obsidian vault with incremental daily files, merged sessions, token monitoring, and optional QQ warnings.

This skill is ready for commercial/non-commercial use.

## Publisher:

[valuemoon2025](https://clawhub.ai/user/valuemoon2025)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to preserve session chat history in Obsidian as daily or ad hoc Markdown snapshots, with basic token usage monitoring for long-running sessions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: OpenClaw chat history may be copied into long-lived plaintext Obsidian files.

Mitigation: Use a private vault, avoid syncing sensitive backups, apply restrictive permissions such as umask 077, and define a retention practice for backup files.

Risk: A cron job can continue backing up sessions after the user no longer wants automatic copying.

Mitigation: Review the installed crontab after setup and remove or disable the scheduled command when automatic backups are no longer needed.

Risk: QQ warning notifications can disclose session status or usage details to an external channel.

Mitigation: Leave QQ notification credentials unset unless warnings are required, and verify the destination account before enabling them.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/valuemoon2025/skills/session-daily-backup-obsidian)
- [Obsidian](https://obsidian.md)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown files and shell command guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces plaintext Obsidian backups from local OpenClaw JSONL session files and may emit QQ token warnings when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
