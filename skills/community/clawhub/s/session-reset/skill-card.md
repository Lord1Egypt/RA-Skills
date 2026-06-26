## Description: <br>
Safely resets OpenClaw agent session files with backup, preview, restore, and batch cleanup support. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[traceless929](https://clawhub.ai/user/traceless929) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and OpenClaw operators use this skill to preview and reset stale or targeted agent sessions, apply updated agent configuration, manage backups, and restore accidentally removed session state. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad reset scopes can remove active or useful OpenClaw session context. <br>
Mitigation: Run with --dry-run first, review the listed sessions, and avoid --force unless the reset scope is intentional. <br>
Risk: Backups can retain private conversation context from session JSONL files. <br>
Mitigation: Protect access to ~/.openclaw/session-backups and periodically remove old backups with --cleanup. <br>
Risk: A restore operation can overwrite current session files. <br>
Mitigation: List backups first and confirm the timestamp before running --restore. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/traceless929/session-reset) <br>
- [OpenClaw official documentation](https://docs.openclaw.ai) <br>
- [OpenClaw Skill development guide](https://docs.openclaw.ai/skills) <br>
- [OpenClaw Session management](https://docs.openclaw.ai/sessions) <br>
- [Session Reset reference material](references/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands may operate on local OpenClaw session files and backups under ~/.openclaw when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: artifact/config.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
