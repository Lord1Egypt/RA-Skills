## Description: <br>
Automatically backs up OpenClaw session conversations into an Obsidian vault, with incremental daily backups, multi-session merging, token monitoring, and optional QQ warning notifications. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ValueMoon2025](https://clawhub.ai/user/ValueMoon2025) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to preserve agent session history as Obsidian Markdown notes for review, continuity, and personal knowledge management. It is suited to private vault workflows where persistent conversation archives are intentionally maintained. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent backups can copy full OpenClaw conversation history, including sensitive content, into Obsidian Markdown files. <br>
Mitigation: Use a private, access-controlled vault, review generated notes before sharing or syncing, and install only when persistent conversation archives are intended. <br>
Risk: Cloud-synced vaults can propagate backed-up conversations outside the local machine. <br>
Mitigation: Disable or restrict cloud sync for the target vault unless the synced destination is approved for the conversation data. <br>
Risk: Optional QQ warning notifications can send token-alert metadata through an external channel. <br>
Mitigation: Leave QQ notification settings disabled unless that channel is approved, and remove those settings when external alerting is no longer needed. <br>
Risk: A cron job can keep copying new session content after the user no longer expects backups. <br>
Mitigation: Review scheduled jobs during installation and remove or disable the cron entry when backups are no longer required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ValueMoon2025/session-daily-backup-obsidian) <br>
- [Publisher profile](https://clawhub.ai/user/ValueMoon2025) <br>
- [Obsidian](https://obsidian.md) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown notes with Obsidian callouts, plus shell command output and configuration guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends daily, full, or hourly Markdown snapshot files and writes local tracking files for incremental backup state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
