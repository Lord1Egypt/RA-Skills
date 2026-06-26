## Description: <br>
Clean up stale OpenClaw session files. Keep the current main session and all group chat sessions; move everything else to a backup directory. Use when performing periodic maintenance, heartbeat cleanup, or when the user asks to clean up sessions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoqunabc](https://clawhub.ai/user/guoqunabc) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to archive stale OpenClaw session transcripts while preserving the current main session and group chat sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Running the cleanup without review may move session transcripts that are still needed for history or auditability. <br>
Mitigation: Run bash scripts/clean-sessions.sh --dry-run first, review the files that would move, and keep the backup directory when session history matters. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/guoqunabc/session-cleaner) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and terminal text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The bundled script supports a --dry-run mode before moving session files to backup.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
