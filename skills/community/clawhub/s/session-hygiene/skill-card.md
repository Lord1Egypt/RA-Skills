## Description: <br>
Prevent sessions.json bloat from accumulating isolated sessions (hooks, crons, subagents). Sets up a cron to archive stale sessions to daily JSONL files and keep sessions.json lean. Use when sessions.json grows large, the gateway becomes slow or unresponsive, or as preventive maintenance on any OpenClaw instance with hooks or crons. Related to openclaw/openclaw#15225. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[halbotley](https://clawhub.ai/user/halbotley) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and operators use this skill to keep OpenClaw session storage from growing unbounded by archiving stale sessions and rotating older archives while preserving the main session. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The maintenance script rewrites sessions.json and appends archived session records to daily JSONL files. <br>
Mitigation: Run with --dry-run first and back up sessions.json before the first live cleanup. <br>
Risk: Archive rotation can delete older session archive files after the configured retention period. <br>
Mitigation: Set --archive-retention-days to match recovery, audit, and compliance requirements before scheduling the job. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/halbotley/session-hygiene) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with cron configuration examples and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces maintenance guidance and commands; the bundled script writes JSON and JSONL session files when executed.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
