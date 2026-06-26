## Description: <br>
Restic-powered encrypted time machine for OpenClaw: hourly incremental snapshots, fast restore by time/snapshot/file, local-only privacy defaults, integrity checks, retention, and optional alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marzliak](https://clawhub.ai/user/marzliak) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to configure and run encrypted local snapshots of OpenClaw memory, sessions, configuration, and selected workspace paths, then restore by time, snapshot, or file when state is corrupted or overwritten. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Configured backup paths may include OpenClaw memory, sessions, configuration, or user-added files containing secrets. <br>
Mitigation: Review config.yaml and run setup.sh --dry-run before installation; avoid adding credential stores unless repository and password-file controls are appropriate. <br>
Risk: Restore, prune, and purge operations can overwrite current state or remove recovery points and backup data. <br>
Mitigation: Use restore previews and non-root targets first, require explicit confirmation for restore-to-root, and run prune or uninstall --purge only after confirming the data impact. <br>
Risk: Losing the restic password file makes encrypted snapshots unrecoverable. <br>
Mitigation: Back up the restic password file separately and protect it from disclosure alongside the backup repository. <br>
Risk: Optional Telegram, healthcheck, and update-check integrations can create network egress. <br>
Mitigation: Keep privacy.local_only enabled unless external integrations are intentionally configured and reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/marzliak/quick-backup-restore) <br>
- [Project homepage](https://github.com/marzliak/quick-backup-restore) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, Markdown] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operator-facing backup, restore, status, pruning, setup, and uninstall guidance for local OpenClaw recovery workflows.] <br>

## Skill Version(s): <br>
3.2.3 (source: skill.json and changelog, released 2026-06-01) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
