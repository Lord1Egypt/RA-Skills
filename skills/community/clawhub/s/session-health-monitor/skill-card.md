## Description: <br>
Context window health monitoring for OpenClaw agents: threshold warnings via Telegram, pre-compaction snapshots, and memory rotation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assistantheinrich-prog](https://clawhub.ai/user/assistantheinrich-prog) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agent operators use this skill to monitor OpenClaw session context usage, warn users before compaction, snapshot important session facts, and rotate local memory files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local session facts may be written to memory files. <br>
Mitigation: Review facts before snapshotting secrets and set MEMORY_DIR deliberately. <br>
Risk: The setup script changes ~/.claude/settings.local.json to run a statusline script in future sessions. <br>
Mitigation: Run scripts/setup-statusline.sh only after accepting that settings change and keep the generated backup for rollback. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/assistantheinrich-prog/session-health-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash scripts and optional JSON status output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes local memory snapshots and session state files when its scripts are run.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
