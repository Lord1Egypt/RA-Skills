## Description: <br>
Never lose a conversation again. Auto-backup, smart recovery, and health monitoring for OpenClaw sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[1052326311](https://clawhub.ai/user/1052326311) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users, agent operators, and multi-agent teams use this skill to back up session files, monitor session health, recover conversations, and preserve task context after crashes, disconnects, or token overflow. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persistently read broad OpenClaw conversation data and produce backup or Knowledge archives that may contain sensitive session content. <br>
Mitigation: Install only where always-on local session access is intended; restrict filesystem access and treat backups, summaries, and Knowledge outputs as sensitive archives. <br>
Risk: Cron jobs and OpenClaw summary delivery can expose conversation summaries through configured delivery channels. <br>
Mitigation: Review scripts/config.sh and scripts/install.sh before enabling scheduled summaries; consider disabling delivery or avoiding last-channel announcements. <br>
Risk: Restore, health-check, and cleanup behavior may affect active session files if enabled without review. <br>
Mitigation: Review scripts/health-check.sh, scripts/restore.sh, and scripts/knowledge-extractor.sh before deployment; prefer quarantine or dry-run cleanup behavior where available. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/1052326311/session-guardian) <br>
- [Publisher profile](https://clawhub.ai/user/1052326311) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and generated local backup, status, summary, and recovery files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local session backups, health reports, collaboration records, and extracted knowledge when its scripts are installed and scheduled.] <br>

## Skill Version(s): <br>
3.1.0 (source: server evidence release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
