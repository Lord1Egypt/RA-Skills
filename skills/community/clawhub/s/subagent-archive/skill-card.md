## Description:

Provides a cross-platform OpenClaw workflow and PowerShell script for safely archiving and cleaning sub-agent sessions with workspace selection, dashboard session handling, soft deletion, and session index maintenance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[zhaoyongxiu](https://clawhub.ai/user/zhaoyongxiu)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect, archive, and clean OpenClaw sub-agent sessions while preserving main sessions, active cron tasks, and active dashboard sessions. It is intended for controlled maintenance of local OpenClaw workspaces, especially before reclaiming disk space or repairing stale session indexes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has authority to delete session files and rewrite the OpenClaw sessions index.

Mitigation: Run dry-run first, manually review the candidates, prefer soft mode for the first real cleanup, and use enforce mode only after confirming the workspace and targets.

Risk: Running cleanup from a live primary session or against the wrong workspace can remove useful session data.

Mitigation: Specify the workspace explicitly when more than one workspace exists, avoid enforce mode from a live primary session, and protect important keys with the active-key option when available.

Risk: Automatic trust is not appropriate because server security evidence marks the release suspicious and says archival behavior is not reliable enough for automatic trust.

Mitigation: Treat the tool as a high-impact maintenance utility, review generated archive candidates and logs, and verify backups before allowing hard deletion or sessions.json rewrites.

## Reference(s):

- [Subagent Archive ClawHub Listing](https://clawhub.ai/zhaoyongxiu/skills/subagent-archive)
- [OpenClaw](https://openclaw.io)
- [README](README.md)
- [Changelog](CHANGELOG.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, JSON, Guidance]

**Output Format:** [Markdown guidance with PowerShell commands, console status output, optional JSON summaries, and archive log files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can append archive records, create dashboard archive Markdown files, rename files in soft mode, delete files in enforce mode, and rewrite sessions.json after backup when stale keys are found.]

## Skill Version(s):

3.2.0 (source: frontmatter, server release metadata, changelog released 2026-06-06)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
